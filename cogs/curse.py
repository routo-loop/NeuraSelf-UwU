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
import random
import re
import json
import os

class Curse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.state_file = "config/curse_state.json"
        self.active = True
        self.curse_cmd = {"cmd_name": "curse", "prefix": True, "checks": True, "id": "curse"}
        self.last_run = self._load_last_run()
        self.loop_task = asyncio.create_task(self.loop())

    def _load_last_run(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    return data.get("curse_last_run", 0)
            except:
                pass
        return 0

    def _save_last_run(self):
        data = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
            except:
                pass
        data["curse_last_run"] = self.last_run
        with open(self.state_file, "w") as f:
            json.dump(data, f)

    async def loop(self):
        self.bot.log("SYS", "Curse module started.")
        await asyncio.sleep(10)
        while self.active:
            cfg = self.bot.config.get("commands", {}).get("curse", {})
            if self.bot.paused or not cfg.get("enabled", False):
                await asyncio.sleep(5)
                continue

            cooldown_range = cfg.get("cooldown", [305, 310])
            cur_cooldown = random.uniform(cooldown_range[0], cooldown_range[1])

            if time.time() - self.last_run > cur_cooldown:
                await self._execute()
                self.last_run = time.time()
                self._save_last_run()
            await asyncio.sleep(5)

    async def _execute(self):
        cfg = self.bot.config.get("commands", {}).get("curse", {})
        if not cfg.get("enabled", False):
            return
        targets = cfg.get("targets", [])
        if targets:
            target = random.choice(targets)
            full_cmd = f"curse <@{target}>"
        else:
            full_cmd = "curse"
        await self.bot.send_message(full_cmd)
        self.bot.log("CMD", f"Executed: {full_cmd}")

    @commands.Cog.listener()
    async def on_message(self, message):
        await self._process_response(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self._process_response(after)

    async def _process_response(self, message):
        monitor_id = str(self.bot.config.get("monitor_bot_id", "408785106942164992"))
        if str(message.author.id) != monitor_id:
            return
        if message.channel.id != self.bot.channel_id:
            return
        if not self.bot.is_message_for_me(message):
            return

        full_content = self.bot.get_full_content(message)
        if "puts a curse on" in full_content or "is cursed" in full_content:
            self.last_run = time.time()
            self._save_last_run()
            self.bot.log("SUCCESS", "Curse confirmed, cooldown reset.")

        if "slow down" in full_content and "curse" in full_content:
            mins_match = re.search(r"(\d+)\s*min", full_content)
            secs_match = re.search(r"(\d+)\s*sec", full_content)
            wait_time = 0
            if mins_match:
                wait_time = int(mins_match.group(1)) * 60
            elif secs_match:
                wait_time = int(secs_match.group(1))
            if wait_time:
                cfg = self.bot.config.get("commands", {}).get("curse", {})
                base_cd = cfg.get("cooldown", [305, 310])[0]
                self.last_run = time.time() - (base_cd - wait_time)
                self._save_last_run()
                self.bot.log("COOLDOWN", f"Curse rate limit: waiting {wait_time}s")

async def setup(bot):
    await bot.add_cog(Curse(bot))
