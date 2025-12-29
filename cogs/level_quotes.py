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
import aiohttp
import core.state as state

class LevelQuotes:
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.quote_cache = []
        self.task = None
        
    async def start(self):
        self.task = asyncio.create_task(self.level_loop())

    async def fetch_quote(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://favqs.com/api/qotd", timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        quote_obj = data.get('quote', {})
                        return quote_obj.get('body', '')
        except:
            pass
        return None

    async def get_quote(self, min_len, max_len):
        for quote in self.quote_cache:
            if min_len <= len(quote) <= max_len:
                self.quote_cache.remove(quote)
                return quote
        
        for _ in range(5):
            quote = await self.fetch_quote()
            if quote and min_len <= len(quote) <= max_len:
                return quote
            elif quote:
                self.quote_cache.append(quote)
        
        return "owo " * random.randint(3, 8)

    async def level_loop(self):
        await asyncio.sleep(25)
        self.bot.log("SYS", "Level Quotes module started.")
        
        while self.active:
            if self.bot.paused:
                await asyncio.sleep(10)
                continue
            
            cfg = self.bot.config.get('automation', {}).get('level_grind', {})
            if not cfg.get('enabled', False):
                await asyncio.sleep(60)
                continue
            
            use_quotes = cfg.get('use_quotes', True)
            min_len = cfg.get('min_length', 10)
            max_len = cfg.get('max_length', 50)
            
            if use_quotes:
                message = await self.get_quote(min_len, max_len)
                sent = await self.bot.send_message(message)
                if sent:
                    self.bot.log("CMD", f"Level Quote: {len(message)} chars")
                    state.stats['level_quotes_sent'] = state.stats.get('level_quotes_sent', 0) + 1
            else:
                message = "owo " * random.randint(2, 5)
                sent = await self.bot.send_message(message)
                if sent:
                    self.bot.log("CMD", "Level Grind: owo spam")
                    state.stats['level_quotes_sent'] = state.stats.get('level_quotes_sent', 0) + 1
            
            await asyncio.sleep(random.uniform(40, 80))

async def setup(bot):
    cog = LevelQuotes(bot)
    await cog.start()