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
import os
import threading
import unicodedata
import requests
from discord.ext import commands
from playsound3 import playsound
from plyer import notification
import core.state as state

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        cfg = bot.config.get('security', {})
        self.enabled = cfg.get('enabled', True)
        self.notifications_enabled = cfg.get('notifications', {}).get('enabled', True)
        self.notification_title = cfg.get('notifications', {}).get('desktop_title', "Neura Security Alert")
        self.webhook_url = cfg.get('webhook_url')
        self.monitor_id = str(bot.config.get('core', {}).get('monitor_bot_id', '408785106942164992'))
        self.beep_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "beeps", "security_beep.mp3")
        self.ban_keywords = ["youhavebeenbanned"]
        self.captcha_keywords = [
            "areyouarealhuman",
            "verifythatyouarehuman",
            "pleasecompletethiswithin",
            "pleaseusethelinkbelow",
            "completeyourcaptcha"
        ]

    def _normalize(self, text):
        if not text:
            return ""
        text = unicodedata.normalize("NFKD", text)
        return re.sub(r'[^a-zA-Z0-9]', '', text.lower())

    def _show_desktop_notification(self, message):
        if not self.notifications_enabled:
            return
        plat = self.bot.config.get('platform_settings', {})
        if not plat.get('desktop_notifications', True):
            if plat.get('mobile_notifications', True):
                try:
                    os.system(f'termux-notification --title "{self.notification_title}" --content "{message}"')
                    os.system('termux-vibrate -d 500')
                except:
                    pass
            return
        try:
            notification.notify(title=self.notification_title, message=message, timeout=10)
        except:
            pass
    def _send_webhook(self, title, message):
        if not self.webhook_url:
            return

        payload = {
            "embeds": [
                {
                    "title": title,
                    "description": message,
                    "color": 0xFF3B3B,
                    "author": {
                        "name": "NeuraSelf Security",
                        "icon_url": "https://cdn.discordapp.com/attachments/1450161614375620802/1456632606002118657/neuralogo.png"
                    },
                    "image": {
                        "url": "https://cdn.discordapp.com/emojis/1390248515170734111.gif"
                    },
                    "footer": {
                        "text": "NeuraSelf • Captcha & Ban Protection"
                    },
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S')
                }
            ]
        }

        try:
            requests.post(self.webhook_url, json=payload, timeout=5)
        except:
            pass


    async def play_beep(self):
        def _play():
            if os.path.exists(self.beep_file):
                try:
                    playsound(self.beep_file, block=False)
                except:
                    pass
        threading.Thread(target=_play, daemon=True).start()

    def _contains_keyword(self, text, keywords):
        cleaned = self._normalize(text)
        return any(k in cleaned for k in keywords)

    def _has_verify_button(self, message):
        if not message.components:
            return False
        for comp in message.components:
            if not hasattr(comp, "children"):
                continue
            for child in comp.children:
                label = getattr(child, "label", None)
                url = str(getattr(child, "url", "") or "")
                if label and label.lower() == "verify":
                    return True
                if "owobot.com/captcha" in url:
                    return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.enabled:
            return
        if str(message.author.id) != self.monitor_id:
            return
        if self.bot.paused:
            return
        if message.channel.id != self.bot.channel_id:
            return

        content = message.content or ""
        embed_text = ""
        if message.embeds:
            parts = []
            for e in message.embeds:
                if e.title: parts.append(e.title)
                if e.description: parts.append(e.description)
                if e.footer and e.footer.text: parts.append(e.footer.text)
            embed_text = " ".join(parts)

        text_to_check = f"{content} {embed_text}"

        is_for_me = (
            str(self.bot.user.id) in content
            or self.bot.user.mentioned_in(message)
        )

        if not is_for_me:
            names = {self.bot.user.name.lower(), self.bot.user.display_name.lower()}
            if self.bot.nickname:
                names.add(self.bot.nickname.lower())
            norm = self._normalize(text_to_check)
            is_for_me = any(self._normalize(n) in norm for n in names)

        if not is_for_me:
            return

        if self._contains_keyword(text_to_check, self.ban_keywords):
            self.bot.paused = True
            state.bot_paused = True
            self.bot.log("ALARM", "BAN DETECTED! STOPPING BOT.")
            await self.play_beep()
            self._show_desktop_notification("Bot stopped: Ban detected!")
            self._send_webhook("BAN DETECTED", f"Message:\n{content}")
            return

        captcha_keywords_hit = self._contains_keyword(text_to_check, self.captcha_keywords)
        verify_button = self._has_verify_button(message)

        if verify_button or (captcha_keywords_hit and message.components):
            self.bot.paused = True
            state.bot_paused = True
            self.bot.throttle_until = time.time() + 3600
            state.stats['last_captcha_msg'] = text_to_check[:200]
            self.bot.log("ALARM", "CAPTCHA DETECTED!")
            await self.play_beep()
            self._show_desktop_notification("Captcha detected! Solve and resume manually.")
            self._send_webhook(
                "CAPTCHA DETECTED",
                "Solve here: https://owobot.com/captcha"
            )

async def setup(bot):
    await bot.add_cog(Security(bot))
