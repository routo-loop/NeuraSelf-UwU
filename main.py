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
import sys
import os
import json
import threading
import time
from rich.console import Console
from rich.align import Align

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.bot import NeuraBot
from dashboard.app import app as flask_app
import core.state as state

console = Console()

def show_banner():
    os.system('cls') 
    neura_ascii_art = [
        "[#ff0000]     ▄   ▄███▄     ▄   █▄▄▄▄ ██  [/#ff0000]",
        "[#ff0000]      █  █▀   ▀     █  █  ▄▀ █ █ [/#ff0000]",
        "[#ff0000]  ██   █ ██▄▄    █   █ █▀▀▌  █▄▄█[/#ff0000]",
        "[#ff0000]  █ █  █ █▄   ▄▀ █   █ █  █  █  █[/#ff0000]",
        "[#ff0000]  █  █ █ ▀███▀   █▄ ▄█   █      █[/#ff0000]",
        "[#ff0000]  █   ██          ▀▀▀   ▀      █ [/#ff0000]",
        "[#ff0000]                              ▀  [/#ff0000]",
        "[#ff0000]┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈[/#ff0000]",
        "[bold cyan] N E U R A   S E L F[/bold cyan]  [white]•[/white]  [bold cyan]Made by ROUTO[/bold cyan]",
        "[#ff0000]┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈[/#ff0000]",
    ]

    neura_ascii_art = "\n".join(neura_ascii_art)
    console.print(Align.center(neura_ascii_art))
    console.print("\n")
    console.print("\n")
    console.print("\n")






def select_account():
    try:
        with open('config/settings.json', 'r') as f:
            config = json.load(f)
    except:
        return None, None
    accounts = config.get('accounts', [])
    if not accounts: return None, None
    if len(accounts) == 1:
        acc = accounts[0]
        return acc.get('token'), acc.get('channels')
    console.print("\n[bold cyan]Available Accounts:[/bold cyan]")
    for i, acc in enumerate(accounts):
        name = acc.get('name', f'Account {i+1}')
        channels = len(acc.get('channels', []))
        console.print(f"  [yellow]{i+1}.[/yellow] {name} ([green]{channels}[/green] channels)")
    try:
        choice = console.input("\n[bold]Select account (number): [/bold]").strip()
        idx = int(choice) - 1
        if 0 <= idx < len(accounts):
            acc = accounts[idx]
            return acc.get('token'), acc.get('channels')
    except:
        pass
    return None, None

def run_dashboard():
    flask_app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)

async def main():
    show_banner()
    token, channels = select_account()
    if not token or not channels: return
    dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
    dashboard_thread.start()
    time.sleep(2)
    bot = NeuraBot(token=token, channels=channels)
    state.bot_instances.append(bot)
    await bot.run_bot()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass