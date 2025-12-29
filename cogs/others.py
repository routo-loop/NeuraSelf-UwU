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
import re
import json
import random
import core.state as state

class Others:
    def __init__(self, bot):
        self.bot = bot
        self.zoo = False
        self.emoji_dict = {}
        
        try:
            with open("utils/emojis.json", 'r', encoding="utf-8") as file:
                self.emoji_dict = json.load(file)
        except:
            pass

    def get_emoji_names(self, text):
        pattern = re.compile(r"<a:[a-zA-Z0-9_]+:[0-9]+>|:[a-zA-Z0-9_]+:|[\U0001F300-\U0001F6FF\U0001F700-\U0001F77F]")
        emojis = pattern.findall(text)
        return [self.emoji_dict[char]["name"] for char in emojis if char in self.emoji_dict]

    async def on_message(self, message):
        monitor_id = str(self.bot.config.get('monitor_bot_id', '408785106942164992'))
        if str(message.author.id) != monitor_id:
            return
        
        if message.channel.id != self.bot.channel_id:
            return

        content = message.content.lower()
        
        if "you currently have" in content and "cowoncy" in content:
            try:
                cash_match = re.search(r'you currently have[^\d]*(\d{1,3}(?:,\d{3})*)', message.content)
                if cash_match:
                    cash_str = cash_match.group(1).replace(',', '')
                    state.stats['current_cash'] = int(cash_str)
                    state.stats['last_cash_update'] = time.time()
                    state.record_snapshot()
                    self.bot.log("INFO", f"Cash Updated: {cash_str} cowoncy")
            except:
                pass


        elif "create a team with the command" in content:
            self.zoo = True
            await self.bot.send_message(f"{self.bot.prefix}zoo")
            self.bot.log("SYS", "Zoo triggered")

        elif "'s zoo! **" in content and self.zoo:
            animals = self.get_emoji_names(message.content)
            animals.reverse()
            self.zoo = False
            
            for i in range(min(len(animals), 3)):
                await asyncio.sleep(1.5)
                await self.bot.send_message(f"{self.bot.prefix}team add {animals[i]}")
                self.bot.log("CMD", f"Added animal: {animals[i]}")

async def setup(bot):
    cog = Others(bot)
    bot.add_listener(cog.on_message, 'on_message')
