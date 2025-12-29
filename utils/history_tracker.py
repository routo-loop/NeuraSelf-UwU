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
import time
from datetime import datetime

HISTORY_FILE = 'config/history.json'

def load_history():
    """Load persistent history from JSON"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return {
        "sessions": [],
        "cash_history": [],
        "totals": {
            "all_time_hunts": 0,
            "all_time_battles": 0,
            "all_time_commands": 0,
            "all_time_captchas": 0,
            "total_sessions": 0
        }
    }

def save_history(history_data):
    """Save history to JSON"""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history_data, f, indent=4)
    except Exception as e:
        print(f"Failed to save history: {e}")

def start_session(history_data):
    """Start a new session"""
    session = {
        "id": len(history_data['sessions']) + 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "end_time": None,
        "stats": {
            "hunts": 0,
            "battles": 0,
            "commands": 0,
            "captchas": 0
        }
    }
    history_data['sessions'].append(session)
    history_data['totals']['total_sessions'] += 1
    save_history(history_data)
    return session

def end_session(history_data):
    """End the current session"""
    if history_data['sessions']:
        current = history_data['sessions'][-1]
        current['end_time'] = datetime.now().strftime("%H:%M:%S")
        save_history(history_data)

def track_command(history_data, cmd_type):
    """Track a command in current session"""
    if not history_data['sessions']:
        start_session(history_data)
    
    current = history_data['sessions'][-1]
    current['stats']['commands'] += 1
    
    if cmd_type == 'hunt':
        current['stats']['hunts'] += 1
        history_data['totals']['all_time_hunts'] += 1
    elif cmd_type == 'battle':
        current['stats']['battles'] += 1
        history_data['totals']['all_time_battles'] += 1
    elif cmd_type == 'captcha':
        current['stats']['captchas'] += 1
        history_data['totals']['all_time_captchas'] += 1
    
    history_data['totals']['all_time_commands'] += 1
    
    save_history(history_data)

def track_cash(history_data, amount):
    """Track cash for history chart"""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount
    }
    history_data['cash_history'].append(entry)
    
    if len(history_data['cash_history']) > 100:
        history_data['cash_history'] = history_data['cash_history'][-100:]
    
    save_history(history_data)

def get_session_stats(history_data):
    """Get current session stats"""
    if history_data['sessions']:
        return history_data['sessions'][-1]['stats']
    return {"hunts": 0, "battles": 0, "commands": 0, "captchas": 0}

def get_all_time_stats(history_data):
    """Get all-time statistics"""
    return history_data['totals']
