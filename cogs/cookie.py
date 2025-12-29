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
import asyncio
import time
import json
import os
import re

class Cookie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.stats_file = 'config/stats_cookie.json'
        self.last_run = self._load_last_run()
        self.cooldown_until = 0
        self.loop_task = asyncio.create_task(self.run_loop())

    def _load_last_run(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    data = json.load(f)
                    return data.get(str(self.bot.user_id), 0)
            except:
                return 0
        return 0

    def _save_last_run(self, timestamp):
        data = {}
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    data = json.load(f)
            except:
                pass
        data[str(self.bot.user_id)] = timestamp
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(data, f, indent=4)
        except:
            pass

    async def run_loop(self):
        await asyncio.sleep(15)
        while self.active:
            cfg = self.bot.config.get('commands', {}).get('cookie', {})
            if self.bot.paused or not cfg.get('enabled', False):
                await asyncio.sleep(10)
                continue

            current_time = time.time()
            if current_time < getattr(self.bot, 'throttle_until', 0):
                await asyncio.sleep(5)
                continue
            if current_time < self.cooldown_until:
                remaining = self.cooldown_until - current_time
                h = int(remaining // 3600)
                m = int((remaining % 3600) // 60)
                self.bot.log("INFO", f"Cookie on cooldown: {h}h {m}m remaining.")
                await asyncio.sleep(min(remaining, 3600))
                continue
            
            cookie_cooldown = 86400
            elapsed = current_time - self.last_run
            if elapsed >= cookie_cooldown:
                user_to_cookie = cfg.get('userid')
                if user_to_cookie:
                    self.bot.log("INFO", f"Sending cookie command to {user_to_cookie}...")
                    cmd = f"cookie {user_to_cookie}"
                    success = await self.bot.send_message(cmd)
                    if success:
                        self.last_run = time.time()
                        self.cooldown_until = self.last_run + cookie_cooldown
                        self._save_last_run(self.last_run)
                    else:
                        await asyncio.sleep(30)
                        continue
            await asyncio.sleep(60)

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
            # look for "🚫" emoji (for difference between cookie and daily cooldown)
            if "🚫" in message.content:

                self._sync_cooldown(full_content, "cookie")
        
        if "sent a cookie to" in full_content:
            self.last_run = time.time()
            self._save_last_run(self.last_run)
            self.cooldown_until = self.last_run + 86400  
            self.bot.log("SUCCESS", "Cookie successfully sent.")

    def _sync_cooldown(self, message, command_type):
      
        h_match = re.search(r'(\d+)\s*[hH]', message)
        m_match = re.search(r'(\d+)\s*[mM]', message)
        s_match = re.search(r'(\d+)\s*[sS]', message)
        
        h = int(h_match.group(1)) if h_match else 0
        m = int(m_match.group(1)) if m_match else 0
        s = int(s_match.group(1)) if s_match else 0
        total_seconds = (h * 3600) + (m * 60) + s
        
   
        if command_type == "cookie":
            self.bot.log("COOLDOWN", f"Cookie cooldown synced: {h}h {m}m {s}s remaining.")
            self.cooldown_until = time.time() + total_seconds + 30  
        

        self.last_run = time.time() - (86400 - (total_seconds + 30))  
        self._save_last_run(self.last_run)

async def setup(bot):
    await bot.add_cog(Cookie(bot))
