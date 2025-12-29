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
import random
import time

class TypingSimulator:
    @staticmethod
    async def send(bot, channel, content):
        config = bot.config.get('stealth', {}).get('typing', {})
        if not config.get('enabled', False):
            try:
                await channel.send(content)
                return True
            except:
                return False
        
        reaction_min = config.get('reaction_min', 0.5)
        reaction_max = config.get('reaction_max', 1.5)
        await asyncio.sleep(random.uniform(reaction_min, reaction_max))

        try:
            async with channel.typing():
                chars = list(content)
                i = 0
                while i < len(chars):
                    char = chars[i]
                    delay = random.uniform(0.04, 0.09)
                    if char in ".,!?;": delay += random.uniform(0.2, 0.4)
                    
                    if random.random() < 0.03 and i < len(chars) - 1:
                        wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                        await asyncio.sleep(delay)
                        # We don't actually send the wrong char yet, we simulate the "press" then backspace
                        await asyncio.sleep(random.uniform(0.1, 0.2))
                        await asyncio.sleep(random.uniform(0.2, 0.4))
                        
                    await asyncio.sleep(delay)
                    i += 1
                
                if random.random() < 0.1: await asyncio.sleep(random.uniform(0.3, 0.7))
                await channel.send(content)
                return True
        except:
            return False
    
    @staticmethod
    def calculate_typing_speed(text, wpm=50):
        return (len(text) / 5) / wpm * 60