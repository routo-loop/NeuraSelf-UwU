# This file is part of NeuraSelf-UwU.
# Copyright (c) 2025-Present Routo

# NeuraSelf-UwU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with NeuraSelf-UwU. If not, see <https://www.gnu.org/licenses/>.


from discord.ext import commands
import json
import os
import asyncio
import time
import random
import re

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.stats_file = 'config/stats_daily.json'
        self.last_run = self._load_last_run()
        self.cooldown = 86400
        self.loop_task = asyncio.create_task(self.loop())

    def _load_last_run(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    data = json.load(f)
                    return data.get(str(self.bot.user_id), 0)
            except:
                return 0
        return 0

    def _save_last_run(self, ts):
        data = {}
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    data = json.load(f)
            except:
                pass
        data[str(self.bot.user_id)] = ts
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(data, f, indent=4)
        except:
            pass

    async def loop(self):
        await asyncio.sleep(10)
        while self.active:
            if self.bot.paused:
                await asyncio.sleep(5)
                continue
            cfg = self.bot.config.get('commands', {}).get('daily', {})
            if not cfg.get('enabled', False):
                await asyncio.sleep(60)
                continue
            
            remaining = self.last_run + self.cooldown - time.time()
            if remaining <= 0:
                self.bot.log("INFO", "Sending daily command...")
                success = await self.bot.send_message("daily")
                if success:
                    self.last_run = time.time()
                    self.cooldown = 86400  # Default
                    self._save_last_run(self.last_run)
                else:
                    await asyncio.sleep(30)
                    continue
            else:
                h = int(remaining // 3600)
                m = int((remaining % 3600) // 60)
                self.bot.log("INFO", f"Daily on cooldown: {h}h {m}m remaining.")
                await asyncio.sleep(min(remaining, 3600))
                continue
                
            await asyncio.sleep(random.uniform(30, 90))

    @commands.Cog.listener()
    async def on_message(self, message):
        await self._process_response(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self._process_response(after)

    async def _process_response(self, message):
        monitor_id = str(self.bot.config.get('monitor_bot_id', '408785106942164992'))
        if str(message.author.id) != monitor_id: return
        if message.channel.id != self.bot.channel_id: return
        
        full_content = self.bot.get_full_content(message)
        if not self.bot.is_message_for_me(message): return
        
        if "wait" in full_content:
            # More robust H/M/S extraction
            h_match = re.search(r'(\d+)\s*[hH]', full_content)
            m_match = re.search(r'(\d+)\s*[mM]', full_content)
            s_match = re.search(r'(\d+)\s*[sS]', full_content)
            
            h = int(h_match.group(1)) if h_match else 0
            m = int(m_match.group(1)) if m_match else 0
            s = int(s_match.group(1)) if s_match else 0
            total_seconds = (h * 3600) + (m * 60) + s
            
            if total_seconds > 0:
                # Disambiguation: Must be for daily
                # Check 1: Explicit keyword in message
                # Check 2: Last sent command was daily within 6 seconds
                time_since_last = time.time() - getattr(self.bot, 'last_sent_time', 0)
                is_for_daily = "daily" in full_content or \
                               ("daily" in self.bot.last_sent_command.lower() and time_since_last < 6.0)
                
                if is_for_daily:
                    self.cooldown = total_seconds + 30
                    self.last_run = time.time()
                    self._save_last_run(self.last_run)
                    self.bot.log("COOLDOWN", f"Daily wait synced: {h}h {m}m {s}s remaining.")

async def setup(bot):
    await bot.add_cog(Daily(bot))
