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
import core.state as state

class Stealth:
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.task = None
        
    async def start(self):
        self.task = asyncio.create_task(self.switcher_loop())

    async def switcher_loop(self):
        await asyncio.sleep(5)
        while self.active:
            cfg = self.bot.config.get('utilities', {}).get('channel_switcher', {})
            if cfg.get('enabled', False):
                interval_config = cfg.get('interval', 1500)
                
                if isinstance(interval_config, list) and len(interval_config) == 2:
                    interval = random.uniform(interval_config[0], interval_config[1])
                else:
                    interval = float(interval_config)
                
                await asyncio.sleep(interval)
                
                channels = cfg.get('channels', [])
                if len(channels) >= 2:
                    current = str(self.bot.channel_id)
                    next_chan = channels[1] if current == str(channels[0]) else channels[0]
                    
                    self.bot.channel_id = int(next_chan)
                    self.bot.log("SYS", f"Stealth: Rotated to channel {next_chan}")
                
                if isinstance(interval_config, list) and len(interval_config) == 2:
                    interval = random.uniform(interval_config[0], interval_config[1])
                else:
                    interval = float(interval_config)
                await asyncio.sleep(interval)
            else:
                await asyncio.sleep(60)

async def setup(bot):
    cog = Stealth(bot)
    await cog.start()