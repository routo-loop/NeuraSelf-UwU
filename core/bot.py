# This file is part of NeuraSelf-UwU.
# Copyright (c) 2025-Present Routo

# NeuraSelf-UwU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with NeuraSelf-UwU. If not, see <https://www.gnu.org/licenses/>.


import discord
from discord.ext import commands
import json
import os
import time
import random
import asyncio
import re
import ctypes
from rich.console import Console
from rich.text import Text
from modules.typing import TypingSimulator
import core.state as state

class NeuraBot(commands.Bot):
    def __init__(self, token=None, channels=None):
        self.console = Console()
        self.config = self._load_config()
        self.token = token
        self.channels = channels or []
        self._audio_count = 0
        if not self.token or not self.channels:
            accounts = self.config.get('accounts', [])
            if accounts:
                primary = accounts[0]
                self.token = self.token or primary.get('token')
                self.channels = self.channels or primary.get('channels', [])
        self.channel_id = int(self.channels[0]) if self.channels else None
        core_cfg = self.config.get('core', {})
        self.prefix = self.config.get('prefix') or core_cfg.get('prefix', 'owo ')
        self.user_id = self.config.get('user_id') or core_cfg.get('user_id')
        self.owo_bot_id = str(core_cfg.get('monitor_bot_id', '408785106942164992'))
        super().__init__(command_prefix=self.prefix, self_bot=True)
        self.username = "Bot"
        self.display_name = "Bot"
        self.nickname = None
        self.identifiers = []
        self.modules = {}
        self.active = True
        self.paused = False
        self.warmup_until = time.time() + 10
        self.last_sent_command = ""
        self.throttle_until = 0.0
        self.last_sent_time = 0
        self.command_lock = asyncio.Lock()
        self.min_command_interval = 4.2
        self.command_history = []
        self.is_ready = False
        self.log_colors = {
            'SYS': 'cyan',
            'CMD': 'green',
            'INFO': 'blue',
            'SUCCESS': 'bright_green',
            'COOLDOWN': 'bright_yellow',
            'ALARM': 'bright_red',
            'ERROR': 'red',
            'SECURITY': 'red',
            'AutoHunt': 'bright_cyan'
        }
        self.cmd_cooldowns = {}
    
    async def setup_hook(self):
        self.log("SYS", "Initializing systems...")
        asyncio.create_task(self._process_pending_commands())
        await self._load_modules()
    
    async def _process_pending_commands(self):
        await asyncio.sleep(5)
        while True:
            if not self.is_ready:
                await asyncio.sleep(1)
                continue
            if 'pending_commands' in state.stats and state.stats['pending_commands']:
                pending = state.stats['pending_commands'][:]
                for cmd_data in pending:
                    if time.time() - cmd_data['timestamp'] < 300:
                        success = await self.send_message(cmd_data['command'])
                        if success:
                            state.stats['pending_commands'] = [
                                c for c in state.stats['pending_commands'] 
                                if c['timestamp'] != cmd_data['timestamp']
                            ]
                    else:
                        state.stats['pending_commands'] = [
                            c for c in state.stats['pending_commands'] 
                            if c['timestamp'] != cmd_data['timestamp']
                        ]
            await asyncio.sleep(2)
    
    async def on_ready(self):
        self.is_ready = True
        self.user_id = self.user.id
        self.username = self.user.name
        self.display_name = self.user.display_name
        self.identifiers = [
            self.username.lower(),
            self.display_name.lower(),
            f"<@{self.user_id}>",
            f"<@!{self.user_id}>"
        ]
        self.log("SYS", f"Ready as {self.username} (Display: {self.display_name})")
        self.log("INFO", f"Channel: {self.channel_id}")
    
    async def _send_safe(self, content, skip_typing=False):
        if not content or not self.is_ready:
            return False
            
        content = self._fix_command(content)
        current_time = time.time()
        
        if current_time < self.warmup_until:
             await asyncio.sleep(max(0.1, self.warmup_until - current_time))
             

        if current_time < self.throttle_until:
            wait = self.throttle_until - current_time
            self.log("COOLDOWN", f"Throttled. Waiting {round(wait, 1)}s")
            await asyncio.sleep(wait + 0.5)
            
        channel = self.get_channel(self.channel_id) or await self.fetch_channel(self.channel_id)
        if not channel: return False
        
        try:
            stealth = self.config.get('stealth', {}).get('typing', {})
            if stealth.get('enabled', False) and not skip_typing:
                sent_ok = await TypingSimulator.send(self, channel, content)
                if not sent_ok: return False
            else:
                await channel.send(content)
                
            short_cmd = content[:30] + "..." if len(content) > 30 else content
            self.log("CMD", f"Sent: {short_cmd}")
            return True
        except Exception as e:
            self.log("ERROR", f"Send failed: {str(e)}")
            return False
    
    def _fix_command(self, command):
        cmd = command.strip()
        if cmd.lower() == "owo": return "owo"
        if cmd.lower().startswith("owo owo"): cmd = cmd[4:]
        known = ['hunt', 'battle', 'curse', 'huntbot', 'daily', 'cookie',
                'quest', 'checklist', 'cf', 'slots', 'autohunt', 'upgrade',
                'sacrifice', 'team', 'zoo', 'use', 'inv', 'sell', 'crate',
                'lootbox', 'run', 'pup', 'piku']
        first = cmd.lower().split()[0] if cmd else ""
        if first in known and not cmd.lower().startswith(self.prefix.lower()):
            return f"{self.prefix}{cmd}"
        return cmd
    
    async def send_message(self, content, skip_typing=False, priority=False):
        if not self.active: return False
        if self.paused and "autohunt" not in content.lower() and "check" not in content.lower():
            return False
        
        # 1. Calculate wait time to determine how long to wait outside the lock
        wait_limit = 1.2 if priority else self.min_command_interval
        
        # 2. Sequential Slot Reservation
        async with self.command_lock:
            now = time.time()
            elapsed = now - self.last_sent_time
            if elapsed < wait_limit:
                # Still wait the required time, but inside the lock it's fine
                # as the next command is already blocked.
                # However, for PRIORITY commands, we want to skip as much of it as possible.
                await asyncio.sleep(wait_limit - elapsed)
            
     
            self.last_sent_time = time.time()
            self.last_sent_command = content

      
        success = await self._send_safe(content, skip_typing=skip_typing)
        return success
    
    async def _load_modules(self):
        if not os.path.exists('cogs'):
            os.makedirs('cogs')
        files = os.listdir('cogs')
        for file in files:
            if file.endswith('.py'):
                try:
                    module_name = f'cogs.{file[:-3]}'
                    module = __import__(module_name, fromlist=[''])
                    if hasattr(module, 'setup'):
                        await module.setup(self)
                        self.modules[file] = module
                        self.log("SYS", f"Loaded {file}")
                except Exception as e:
                    self.log("ERROR", f"Failed to load {file}: {e}")
    
    def _load_config(self):
        try:
            with open('config/settings.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    async def run_bot(self):
        self.log("SYS", "Starting bot...")
        await self.start(self.token)

    def set_cooldown(self, cmd, seconds):
        self.cmd_cooldowns[cmd.lower()] = time.time() + seconds

    def get_cooldown(self, cmd):
        return max(0, self.cmd_cooldowns.get(cmd.lower(), 0) - time.time())

    def log(self, level, msg):
        ts = time.strftime("%H:%M:%S")
        color = self.log_colors.get(level, "white")
        bracket_level = f"[{level}]"
        self.console.print(f"[{color}][{ts}] {bracket_level:<10}[/{color}] [white]{msg}[/white]")
        state.log_command(level, msg, "info")

    def get_full_content(self, message):
        if not message: return ""
        content = message.content or ""
        embed_texts = []
        if message.embeds:
            for em in message.embeds:
                parts = [
                    em.title or "",
                    em.author.name if em.author else "",
                    em.description or "",
                    " ".join([f"{f.name} {f.value}" for f in em.fields])
                ]
                embed_texts.append(" ".join(parts))
        return (content + " " + " ".join(embed_texts)).lower()


    def is_message_for_me(self, message):
        if not message: return False
        if self.user.mentioned_in(message): return True
        

        idents = [self.user.name, self.display_name] + self.identifiers
        clean_idents = set()
        for i in idents:
            ci = re.sub(r'[^\w\s]', '', i.lower()).strip()
            if ci and len(ci) >= 2: clean_idents.add(ci)
            
        content = message.content.lower()
        nick = ""
        if message.guild:
            member = message.guild.get_member(self.user.id)
            if member and member.nick:
                nick = member.nick.lower()
                clean_nick = re.sub(r'[^\w\s]', '', nick).strip()
                if clean_nick: clean_idents.add(clean_nick)


        texts = [content]
        if message.embeds:
            for em in message.embeds:
                fields_text = " ".join([f"{f.name} {f.value}" for f in em.fields])
                texts.append(f"{em.title or ''} {em.author.name if em.author else ''} {em.description or ''} {fields_text}".lower())

        for text in texts:
            for ident in clean_idents:
                if re.search(rf"\b{re.escape(ident)}\b", text):
                    return True

        generic_patterns = [
            "beep boop", "i am back with", "i will be back in",
            "please include your password", "password will reset in",
            "confirm your identity", "link below", "here is your password",
            "wrong password", "incorrect password"
        ]
        
        full_visible_text = " ".join(texts)
        if any(pat in full_visible_text for pat in generic_patterns):
            # we trust it's ours if it's in the same channel 
            # (already filtered by channel_id in calling Cog)
            return True

        return False