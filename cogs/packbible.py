# This file is part of NeuraSelf-UwU.
# Copyright (c) 2025-Present Routo

# NeuraSelf-UwU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with NeuraSelf-UwU. If not, see <https://www.gnu.org/licenses/>.

import asyncio
import time
import random

class PackBible:
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.task = None
        self.last_run = 0
        self.command_availability = {"run": 0, "pup": 0, "piku": 0}
        
    async def start(self):
        self.task = asyncio.create_task(self.loop())

    async def loop(self):
        await asyncio.sleep(10)
        self.bot.log("SYS", "PackBible (RPP) module started.")
        
        while self.active:
            cfg = self.bot.config.get('automation', {}).get('rpp', {})
            if self.bot.paused or not cfg.get('enabled', False):
                await asyncio.sleep(5)
                continue
            
            interval = cfg.get('interval_s', 60)
            if time.time() - self.last_run > interval:
                commands = cfg.get('commands', ["run", "pup", "piku"])
                available = [c for c in commands if time.time() > self.command_availability.get(c, 0)]
                
                if available:
                    cmd = random.choice(available)
                    await self.bot.send_message(cmd)
                    self.bot.log("CMD", f"RPP: {cmd}")
                    
                self.last_run = time.time()
            
            await asyncio.sleep(2)

    async def on_message(self, message):
        monitor_id = str(self.bot.config.get('monitor_bot_id', '408785106942164992'))
        if str(message.author.id) != monitor_id:
            return
        if message.channel.id != self.bot.channel_id:
            return
        
        content = message.content.lower()
        
        for cmd in ["run", "pup", "piku"]:
            limit_hit = False
            if cmd in content and "tomorrow" in content:
                limit_hit = True
            
            if cmd == "piku" and "garden is out of carrots" in content:
                limit_hit = True
            if cmd == "pup" and "no puppies" in content:
                limit_hit = True
            
            if limit_hit:
                self.command_availability[cmd] = time.time() + 86400
                self.bot.log("COOLDOWN", f"RPP: {cmd} exhausted. Next available tomorrow (24h)")

async def setup(bot):
    cog = PackBible(bot)
    bot.add_listener(cog.on_message, 'on_message')
    await cog.start()