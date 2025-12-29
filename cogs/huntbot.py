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
import time
import re
import os
from playsound3 import playsound
import core.state as state

class HuntBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.last_check = 0
        self.check_interval = 900
        self.task = None
        self.password_reset_regex = r"(?<=Password will reset in )(\d+)"
        self.huntbot_time_regex = r"(\d+)([DHM])"

    async def start_task(self):
        self.task = asyncio.create_task(self.run_loop())

    async def run_loop(self):
        await asyncio.sleep(20)
        while self.active:
            if self.bot.paused:
                await asyncio.sleep(5)
                continue
            cfg = self.bot.config.get('commands', {}).get('huntbot', {})
            if not cfg.get('enabled', False):
                await asyncio.sleep(60)
                continue
            now = time.time()
            if now - self.last_check > self.check_interval:
                amount = cfg.get('cash_to_spend', 16000)
                await self.bot.send_message(f"huntbot {amount}")
                self.last_check = now
            await asyncio.sleep(20)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self._process_message(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self._process_message(after)

    async def _process_message(self, message):
        if message.author.id != int(self.bot.owo_bot_id): return
        if message.channel.id != self.bot.channel_id: return
        content = message.content or ""
        if message.embeds:
            content += " " + self.bot.get_full_content(message)
        content_lower = content.lower()
        if not self.bot.is_message_for_me(message): return

        if "i will be back in" in content_lower:
            total_seconds = 0
            found = False
            for amount, unit in re.findall(self.huntbot_time_regex, content.upper()):
                found = True
                if unit == "M": total_seconds += int(amount) * 60
                elif unit == "H": total_seconds += int(amount) * 3600
                elif unit == "D": total_seconds += int(amount) * 86400
            if found:
                self.check_interval = total_seconds + 30
                self.last_check = time.time()
                self.bot.log("AutoHunt", f"HuntBot busy. Resyncing for {round(total_seconds/60)}m")

        elif "i am back with" in content_lower or "beep boop. i am back with" in content_lower:
            rewards = content.split('back with')[-1].strip().upper() if 'back with' in content_lower else "UNKNOWN REWARDS"
            self.bot.log("AutoHunt", f"HuntBot returned! Rewards: {rewards[:100]}")
            self.check_interval = 900
            self.last_check = time.time() - 20

        elif "please include your password" in content_lower:
            reset_match = re.search(self.password_reset_regex, content)
            minutes = int(reset_match.group(1)) if reset_match else 10
            wait_s = minutes * 60
            self.bot.log("AutoHunt", f"HuntBot stuck (password required). Reset in {minutes}m.")
            self.check_interval = wait_s + 30
            self.last_check = time.time()

        elif "here is your password" in content_lower or "confirm your identity" in content_lower or "link below" in content_lower:
            img_url = None
            if message.attachments:
                img_url = message.attachments[0].url
            elif message.embeds:
                for em in message.embeds:
                    if em.image:
                        img_url = em.image.url
                        break
            state.stats['current_captcha'] = {
                'type': 'huntbot',
                'time': time.time(),
                'timestamp': time.time(),
                'image_url': img_url
            }
            self.bot.log("AutoHunt", "HuntBot Captcha! CHECK DASHBOARD & SOLVE.")
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(base, "beeps", "huntbot_image_beep.mp3")
            if os.path.exists(path):
                asyncio.create_task(self._play_beep_async(path))

        elif "wrong password" in content_lower or "incorrect password" in content_lower:
            self.bot.log("AutoHunt", "Wrong password provided. Waiting for reset.")
            self.check_interval = 630
            self.last_check = time.time()

    async def _play_beep_async(self, path):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: playsound(path, block=False))

async def setup(bot):
    cog = HuntBot(bot)
    await bot.add_cog(cog)
    await cog.start_task()
