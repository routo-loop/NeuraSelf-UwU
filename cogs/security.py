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
import requests
from playsound3 import playsound
from plyer import notification
import core.state as state

class Security:
    def __init__(self, bot):
        self.bot = bot
        cfg = bot.config.get('security', {})
        self.enabled = cfg.get('enabled', True)
        self.notifications_enabled = cfg.get('notifications', {}).get('enabled', True)
        self.notification_title = cfg.get('notifications', {}).get('desktop_title', "Neura Security Alert")
        self.webhook_url = cfg.get('webhook_url')
        self.monitor_id = str(bot.config.get('core', {}).get('monitor_bot_id', '408785106942164992'))
        self.channel_id = bot.channel_id
        self.beep_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "beeps", "security_beep.mp3")
        self.ban_keywords = ["**☠ |** You have been banned"]
        self.captcha_keywords = ["captcha", "human", "verify", "please complete"]

    def _show_desktop_notification(self, message):
        if not self.notifications_enabled:
            return
        try:
            notification.notify(title=self.notification_title, message=message, timeout=10)
        except:
            pass

    def _send_webhook(self, title, message):
        if not self.webhook_url:
            return
        payload = {
            "embeds": [{
                "title": title,
                "description": message,
                "color": 15158272,
                "footer": {"text": "Neura-Self Captcha Detection"}
            }]
        }
        try:
            requests.post(self.webhook_url, json=payload)
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
        if not text: return False
        text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text.lower())
        return any(kw.lower() in text for kw in keywords)

    def _has_verify_button(self, message):
        if message.components:
            for comp in message.components:
                if hasattr(comp, "children"):
                    for child in comp.children:
                        if hasattr(child, "label") and child.label.lower() == "verify":
                            return True
                        if hasattr(child, "url") and "owobot.com?login=" in str(child.url):
                            return True
        return False

    async def on_message(self, message):
        if not self.enabled:
            return
        if str(message.author.id) != self.monitor_id:
            return
        if self.bot.paused:
            return

        content = (message.content or '').lower()
        embed_text = ''
        if message.embeds:
            parts = []
            for e in message.embeds:
                if getattr(e, 'title', None): parts.append(e.title)
                if getattr(e, 'description', None): parts.append(e.description)
                if getattr(e, 'footer', None) and getattr(e.footer, 'text', None): parts.append(e.footer.text)
            embed_text = ' '.join(parts).lower()

        text_to_check = content + " " + embed_text

        if self._contains_keyword(text_to_check, self.ban_keywords):
            self.bot.paused = True
            state.bot_paused = True
            self.bot.log("ALARM", "BAN DETECTED! STOPPING BOT IMMEDIATELY.")
            await self.play_beep()
            self._show_desktop_notification("Bot stopped: Ban detected!")
            self._send_webhook("BAN DETECTED", f"The bot has been stopped due to a ban message.\n\nMessage: {message.content}")
            return

        captcha_detected = self._contains_keyword(text_to_check, self.captcha_keywords)
        verify_button = self._has_verify_button(message)
        if captcha_detected or verify_button:
            self.bot.paused = True
            state.bot_paused = True
            self.bot.throttle_until = time.time() + 3600
            state.stats['last_captcha_msg'] = message.content
            self.bot.log("ALARM", "CAPTCHA DETECTED! Bot paused, solve manually via dashboard.")
            await self.play_beep()
            self._show_desktop_notification("Captcha Detected! Solve and resume manually via dashboard.")
            self._send_webhook("⚠️ CAPTCHA DETECTED", f"Solve here: https://owobot.com/captcha\n\nMessage content: {message.content}")
