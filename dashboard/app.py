# This file is part of NeuraSelf-UwU.
# Copyright (c) 2025-Present Routo

# NeuraSelf-UwU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with NeuraSelf-UwU. If not, see <https://www.gnu.org/licenses/>.


from flask import Flask, render_template, jsonify, request
import threading
import time
import json
import logging
import core.state as state
import utils.utils as utils
import asyncio

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/stats')
def stats():
    uptime_start = state.stats['uptime_start']
    elapsed = time.time() - uptime_start
    total_cmds = len(state.full_session_history)
    mins = elapsed / 60
    cpm = round(total_cmds / mins, 1) if mins > 0.1 else 0
    
    cph = 0
    if len(state.stats['cowoncy_history']) > 1:
        first = state.stats['cowoncy_history'][0]
        last = state.stats['cowoncy_history'][-1]
        time_diff_hrs = (last[0] - first[0]) / 3600
        cash_diff = last[1] - first[1]
        if time_diff_hrs > 0.01:
            cph = round(cash_diff / time_diff_hrs)

    bot = state.bot_instances[0] if state.bot_instances else None
    
    response_data = {
        'uptime': utils.format_seconds(elapsed),
        'cash': state.stats['current_cash'],
        'logs': list(state.command_logs)[:500],
        'status': "PAUSED" if state.bot_paused else "ONLINE",
        'security': {
             'captchas': state.stats.get('captchas_solved', 0),
             'bans': state.stats.get('bans_detected', 0),
             'warnings': state.stats.get('warnings_detected', 0),
             'last_message': state.stats.get('last_captcha_msg', '')
        },
        'analytics': {
            'cph': cph,
            'gems_used': state.stats.get('gems_used', 0)
        },
        'bot': {
            'user_id': bot.user_id if bot else None,
            'username': getattr(bot, 'username', 'Bot') if bot else 'Bot',
            'channel_id': bot.channel_id if bot else None,
            'paused': state.bot_paused,
            'throttled': time.time() < getattr(bot, 'throttle_until', 0) if bot else False,
            'cooldown_remaining': max(0, int(getattr(bot, 'throttle_until', 0) - time.time())) if bot else 0,
            'cooldown_command': getattr(bot, 'last_sent_command', '') if bot else ''
        },
        'chart_data': {
            'hunt': state.stats.get('hunt_count', 0),
            'battle': state.stats.get('battle_count', 0),
            'total': total_cmds,
            'perf_bpm': cpm
        },
        'system': {
            'last_cash_update': state.stats.get('last_cash_update', 0),
            'pending_commands': len(state.stats.get('pending_commands', []))
        }
    }
    
    return jsonify(response_data)

@app.route('/api/debug')
def debug():
    return jsonify({
        'stats': state.stats,
        'bot_instances': len(state.bot_instances),
        'command_logs_count': len(state.command_logs),
        'full_history_count': len(state.full_session_history)
    })

@app.route('/api/history')
def get_history():
    return jsonify(list(reversed(state.full_session_history)))

@app.route('/api/history/analytics')
def get_analytics():
    try:
        from utils import history_tracker
        dat = history_tracker.load_history()
        return jsonify(dat)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        new_config = request.json
        try:
            with open('config/settings.json', 'w') as f:
                json.dump(new_config, f, indent=4)
            
            for bot in state.bot_instances:
                bot.config = new_config
                bot.prefix = new_config.get('prefix', 'owo ')
                
                accounts = new_config.get('accounts', [])
                if accounts:
                    primary = accounts[0]
                    bot.token = primary.get('token', bot.token)
                    if primary.get('channels'):
                        bot.channels = primary.get('channels')
                        bot.channel_id = int(primary.get('channels')[0])
                else:
                    if new_config.get('channels'):
                        bot.channels = new_config.get('channels')
                        bot.channel_id = int(new_config.get('channels')[0])

            state.log_command("SYS", "Settings updated and synchronized", "success")
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        try:
            with open('config/settings.json', 'r') as f:
                return jsonify(json.load(f))
        except:
            return jsonify({})

@app.route('/api/control', methods=['POST'])
def control():
    data = request.json
    action = data.get('action')
    
    if action == 'stop':
        state.bot_paused = True
        for bot in state.bot_instances:
            bot.paused = True
            bot.log("SYS", "Bot STOPPED via Dashboard")
            
    elif action == 'start':
        state.bot_paused = False
        for bot in state.bot_instances:
            bot.paused = False
            bot.throttle_until = 0
            bot.log("SYS", "Bot RESUMED via Dashboard")
            
    elif action == 'cash':
        if state.bot_instances: 
            bot = state.bot_instances[0]
            asyncio.run_coroutine_threadsafe(
                bot.send_message(f"{bot.prefix}cash", skip_typing=True, priority=True),
                bot.loop
            )
            state.log_command("CMD", "Manual Cash Check Sent", "info")
        
    return jsonify({'success': True})

@app.route('/api/security', methods=['POST'])
def security():
    data = request.json
    action = data.get('action')
    if action == 'resume':
        state.bot_paused = False
        for bot in state.bot_instances:
            bot.paused = False
            bot.throttle_until = 0
        state.log_command("SEC", "User Resumed Bot from Security Alert", "success")
            
    return jsonify({'success': True})

@app.route('/api/captcha/current')
def captcha_current():
    captcha_data = state.stats.get('current_captcha')
    
    if captcha_data and captcha_data.get('image_url'):
        timestamp = captcha_data.get('timestamp', 0)
        if time.time() - timestamp < 600:
            return jsonify({
                'success': True,
                'url': captcha_data['image_url'],
                'cash': captcha_data.get('cash', 16000),
                'command': captcha_data.get('command_template', 'owo autohunt {cash} {password}'),
                'age_seconds': int(time.time() - timestamp)
            })
        else:
            if 'current_captcha' in state.stats:
                del state.stats['current_captcha']
    
    return jsonify({'success': False, 'message': 'No active captcha'})

@app.route('/api/captcha/submit', methods=['POST'])
def captcha_submit():
    data = request.json
    code = data.get('code', '').strip()
    
    if not code:
        return jsonify({'success': False, 'error': 'No password provided'})
    
    captcha_data = state.stats.get('current_captcha')
    if not captcha_data:
        return jsonify({'success': False, 'error': 'No active captcha'})
    
    cash = captcha_data.get('cash', 16000)
    command_template = captcha_data.get('command_template', f"owo autohunt {cash} {{password}}")
    full_command = command_template.replace('{password}', code)
    
    if state.bot_instances:
        bot = state.bot_instances[0]
        asyncio.run_coroutine_threadsafe(
            bot.send_message(full_command, skip_typing=True, priority=True), 
            bot.loop
        )
    
    if 'current_captcha' in state.stats:
        del state.stats['current_captcha']
    
    state.stats['captchas_solved_today'] = state.stats.get('captchas_solved_today', 0) + 1
    state.stats['captcha_success_count'] = state.stats.get('captcha_success_count', 0) + 1
    state.log_command("CMD", f"Captcha solution sent: {full_command}")
    
    return jsonify({'success': True, 'message': f'Captcha solution sent: {full_command}'})

@app.route('/api/captcha/stats')
def captcha_stats():
    solved = state.stats.get('captchas_solved_today', 0)
    success = state.stats.get('captcha_success_count', 0)
    success_rate = 100 if solved == 0 else round((success / max(solved, 1)) * 100)
    
    return jsonify({
        'solved': solved,
        'success_rate': success_rate
    })

@app.route('/api/bot/command', methods=['POST'])
def bot_command():
    data = request.json
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({'success': False, 'error': 'No command provided'})
    
    if state.bot_instances:
        bot = state.bot_instances[0]
        asyncio.run_coroutine_threadsafe(
            bot.send_message(command, skip_typing=True, priority=True), 
            bot.loop
        )
        state.log_command("CMD", f"Manual command sent: {command}")
        return jsonify({'success': True, 'message': f'Command sent: {command}'})
    
    return jsonify({'success': False, 'error': 'No bot instances available'})
