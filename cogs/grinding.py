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
import asyncio
import random
import time
import re
import core.state as state

class Grinding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.cooldowns = {'hunt': 0, 'battle': 0, 'owo': 0}

    async def start_grinding(self):
        asyncio.create_task(self.hunt_loop())
        asyncio.create_task(self.battle_loop())
        asyncio.create_task(self.owo_loop())

    async def hunt_loop(self):
        await asyncio.sleep(5)
        while self.active:
            if self.bot.paused:
                await asyncio.sleep(1)
                continue
            cfg = self.bot.config.get('commands', {}).get('hunt', {})
            if not cfg.get('enabled', False):
                await asyncio.sleep(5)
                continue
            if time.time() >= self.cooldowns['hunt']:
                sent = await self.bot.send_message("hunt")
                if sent:
                    delay = random.uniform(cfg.get('cooldown', [15, 18])[0], cfg.get('cooldown', [15, 18])[1])
                    self.cooldowns['hunt'] = time.time() + delay
            await asyncio.sleep(1)

    async def battle_loop(self):
        await asyncio.sleep(10)
        while self.active:
            if self.bot.paused:
                await asyncio.sleep(1)
                continue
            cfg = self.bot.config.get('commands', {}).get('battle', {})
            if not cfg.get('enabled', False):
                await asyncio.sleep(5)
                continue
            if time.time() >= self.cooldowns['battle']:
                sent = await self.bot.send_message("battle")
                if sent:
                    delay = random.uniform(cfg.get('cooldown', [15, 18])[0], cfg.get('cooldown', [15, 18])[1])
                    self.cooldowns['battle'] = time.time() + delay
            await asyncio.sleep(1)

    async def owo_loop(self):
        await asyncio.sleep(15)
        while self.active:
            if self.bot.paused:
                await asyncio.sleep(1)
                continue
            cfg = self.bot.config.get('commands', {}).get('owo', {})
            if not cfg.get('enabled', False):
                await asyncio.sleep(5)
                continue
            if time.time() >= self.cooldowns['owo']:
                sent = await self.bot.send_message("owo")
                if sent:
                    delay = random.uniform(cfg.get('cooldown', [10, 13])[0], cfg.get('cooldown', [10, 13])[1])
                    self.cooldowns['owo'] = time.time() + delay
            await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != int(self.bot.owo_bot_id): return
        if message.channel.id != self.bot.channel_id: return
        content = message.content.lower()
        if not self.bot.is_message_for_me(message): return
        
        if "you found:" in content:
            self.cooldowns['hunt'] = time.time() + random.uniform(15, 17)
        elif "you won" in content or "you lost" in content or "streak:" in content:
            self.cooldowns['battle'] = time.time() + random.uniform(15, 17)
            
        if "slow down" in content and "try the command again in" in content:
            seconds_match = re.search(r'again in (\d+) second', content)
            if seconds_match:
                wait_time = int(seconds_match.group(1))
                if self.bot.last_sent_command:
                    last_cmd = self.bot.last_sent_command.lower()
                    if "hunt" in last_cmd:
                        self.cooldowns['hunt'] = time.time() + wait_time + 1
                        self.bot.log("COOLDOWN", f"Hunt Rate Limit: synced {wait_time}s")
                    elif "battle" in last_cmd:
                        self.cooldowns['battle'] = time.time() + wait_time + 1
                        self.bot.log("COOLDOWN", f"Battle Rate Limit: synced {wait_time}s")
                    elif last_cmd.strip() == "owo":
                        self.cooldowns['owo'] = time.time() + wait_time + 1
                        self.bot.log("COOLDOWN", f"OwO Rate Limit: synced {wait_time}s")

async def setup(bot):
    cog = Grinding(bot)
    await bot.add_cog(cog)
    await cog.start_grinding()