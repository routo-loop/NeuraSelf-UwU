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
 
class AutoOpen:
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        
        self.crate_cmd = {
            "cmd_name": "crate",
            "prefix": True,
            "id": "crate"
        }
        
        self.lootbox_cmd = {
            "cmd_name": "lootbox",
            "prefix": True,
            "id": "lootbox"
        }
        
        self.cooldowns = {
            'crate': 0.0,
            'lootbox': 0.0
        }
 
    async def _send_cmd(self, cmd):
        if time.time() < self.bot.throttle_until:
            return False
        
        name = cmd["cmd_name"]
        cfg = self.bot.config.get('auto_use', {})
        open_cfg = cfg.get('open', {})
        amt = open_cfg.get('crate' if name == 'crate' else 'lootbox', 'all')
        amt_str = str(amt).strip().lower()
        suffix = 'all' if amt_str in ['', 'all'] else str(amt)
        content = f"{cmd['cmd_name']} {suffix}"
        
        await self.bot.send_message(content)
        return True
 
    async def on_message(self, message):
        monitor_id = str(self.bot.config.get('monitor_bot_id', '408785106942164992'))
        if str(message.author.id) != monitor_id:
            return
        if message.channel.id != self.bot.channel_id:
            return
 
        cfg = self.bot.config.get('auto_use', {})
        use_crate = cfg.get('autoCrate', False)
        use_lootbox = cfg.get('autoLootbox', False)
 
        text = message.content
        lower = text.lower()
 
        if ("received a" in lower or "found a" in lower) and "weapon crate" in lower:
            if use_crate and time.time() >= self.cooldowns['crate']:
                await asyncio.sleep(1.2)
                await self._send_cmd(self.crate_cmd)
                self.cooldowns['crate'] = time.time() + 10
 
        if ("received a" in lower or "found a" in lower) and "lootbox" in lower:
            if use_lootbox and time.time() >= self.cooldowns['lootbox']:
                await asyncio.sleep(1.2)
                await self._send_cmd(self.lootbox_cmd)
                self.cooldowns['lootbox'] = time.time() + 10
 
        if "you don't have any lootboxes" in lower or "no lootboxes" in lower:
            self.cooldowns['lootbox'] = time.time() + 3600
            self.bot.log("COOLDOWN", "Lootbox not available. Pausing 1h.")
 
        if "you don't have any crates" in lower or "no weapon crates" in lower:
            self.cooldowns['crate'] = time.time() + 86400
            self.bot.log("COOLDOWN", "Crate not available. Pausing 24h.")
 
        if "resets in" in lower and "weapon crate" in lower:
            h = re.search(r'(\d+)\s*h', lower)
            m = re.search(r'(\d+)\s*m', lower)
            s = re.search(r'(\d+)\s*s', lower)
            total = 0
            if h: total += int(h.group(1)) * 3600
            if m: total += int(m.group(1)) * 60
            if s: total += int(s.group(1))
            if total > 0:
                self.cooldowns['crate'] = time.time() + total + 10
 
async def setup(bot):
    cog = AutoOpen(bot)
    bot.add_listener(cog.on_message, 'on_message')