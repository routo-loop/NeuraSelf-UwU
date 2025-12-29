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

class Gambling:
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.task = None
        
    async def start(self):
        self.task = asyncio.create_task(self._run_loops())
        
    async def _run_loops(self):
        await asyncio.sleep(5)
        asyncio.create_task(self.coinflip_loop())
        asyncio.create_task(self.slots_loop())
        
    async def coinflip_loop(self):
        await asyncio.sleep(15)
        while self.active:
            if self.bot.paused:
                await asyncio.sleep(5)
                continue
            
            cfg = self.bot.config.get('commands', {}).get('coinflip', {})
            if not cfg.get('enabled', False):
                await asyncio.sleep(60)
                continue
            
            amount = cfg.get('amount', 1)
            side = cfg.get('side', 'h')
            
            await self.bot.send_message(f"{self.bot.prefix}cf {side} {amount}")
            self.bot.log("CMD", f"Coinflip: {side} {amount}")
            state.stats['coinflip_count'] = state.stats.get('coinflip_count', 0) + 1
            
            await asyncio.sleep(random.uniform(30, 60))

    async def slots_loop(self):
        await asyncio.sleep(20)
        while self.active:
            if self.bot.paused:
                await asyncio.sleep(5)
                continue
            
            cfg = self.bot.config.get('commands', {}).get('slots', {})
            if not cfg.get('enabled', False):
                await asyncio.sleep(60)
                continue
            
            amount = cfg.get('amount', 1)
            
            await self.bot.send_message(f"{self.bot.prefix}slots {amount}")
            self.bot.log("CMD", f"Slots: {amount}")
            state.stats['slots_count'] = state.stats.get('slots_count', 0) + 1
            
            await asyncio.sleep(random.uniform(25, 50))

async def setup(bot):
    cog = Gambling(bot)
    await cog.start()