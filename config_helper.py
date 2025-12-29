# This file is part of NeuraSelf-UwU.
# Copyright (c) 2025-Present Routo

# NeuraSelf-UwU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with NeuraSelf-UwU. If not, see <https://www.gnu.org/licenses/>.

import json
import os
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def setup_config():
    config_path = 'config/settings.json'
    
    if not os.path.exists(config_path):
        console.print("[bold red]Error:[/] config/settings.json not found!")
        return

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            console.print("[bold red]Error:[/] Failed to parse settings.json")
            return

    modified = False
    
    if not config.get('accounts'):
        config['accounts'] = [{"token": "YOUR_TOKEN", "channels": ["CHANNEL_ID"], "enabled": True}]
        modified = True

    acc = config['accounts'][0]

    if acc.get('token') in ["YOUR_TOKEN", "", None]:
        console.print("\n[bold yellow]--- FIRST TIME SETUP: TOKEN ---[/]")
        token = Prompt.ask("[cyan]Please enter your Discord Token[/]").strip()
        if token:
            acc['token'] = token
            modified = True
        else:
            console.print("[bold red]Warning:[/] Token not provided.")

    if not acc.get('channels') or acc['channels'][0] in ["CHANNEL_ID", "", None]:
        console.print("\n[bold yellow]--- FIRST TIME SETUP: CHANNEL ID ---[/]")
        channel = Prompt.ask("[cyan]Please enter your Target Channel ID[/]").strip()
        if channel:
            acc['channels'] = [channel]
            if config.get('core'):
                config['core']['channel_id'] = channel
            modified = True
        else:
            console.print("[bold red]Warning:[/] Channel ID not provided.")

    if modified:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        console.print("\n[bold green]Configuration updated successfully![/]")
    else:
        console.print("\n[bold green]Configuration is already set. Skipping prompts.[/]")

if __name__ == "__main__":
    setup_config()
