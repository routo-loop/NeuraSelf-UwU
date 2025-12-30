# 🧠 NeuraSelf - Complete Beginner's Guide

Welcome to NeuraSelf! This guide will walk you through everything you need to get started, even if you've never used Python before.

---

## 📋 Table of Contents

1. [Installing Python](#-step-1-installing-python)
2. [Getting Your Discord Token](#-step-2-getting-your-discord-token)
3. [Finding Channel IDs](#-step-3-finding-channel-ids)
4. [Setting Up NeuraSelf](#-step-4-setting-up-neuraself)
5. [Configuring settings.json](#-step-5-configuring-settingsjson)
6. [Running the Bot](#-step-6-running-the-bot)
7. [Using the Dashboard](#-step-7-using-the-dashboard)
8. [Troubleshooting](#-troubleshooting)

---

## 🐍 Step 1: Installing Python

NeuraSelf requires **Python 3.10**. Here's how to install it on your system:

### 🪟 Windows

1. **Download Python**
   - Go to: <https://www.python.org/downloads/>
   - Click the big yellow button that says "Download Python 3.10.x"
   - Make sure you get version 3.10 or higher!

2. **Install Python**
   - Run the downloaded installer
   - ⚠️ **IMPORTANT**: Check the box that says "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**
   - Open Command Prompt (search for "cmd" in Start menu)
   - Type this command and press Enter:

   ```bash
   python --version
   ```

   - You should see something like: `Python 3.10.x`

### 🍎 macOS

1. **Download Python**
   - Go to: <https://www.python.org/downloads/>
   - Download the macOS installer for Python 3.10 or newer

2. **Install Python**
   - Open the downloaded `.pkg` file
   - Follow the installation wizard
   - Click through all the steps and install

3. **Verify Installation**
   - Open Terminal (search for "Terminal" in Spotlight)
   - Type this command and press Enter:

   ```bash
   python3 --version
   ```

   - You should see: `Python 3.10.x` or higher

### 🐧 Linux (Ubuntu/Debian)

1. **Update Package List**

   ```bash
   sudo apt update
   ```

2. **Install Python 3.10**

   ```bash
   sudo apt install python3.10 python3.10-venv python3-pip
   ```

3. **Verify Installation**

   ```bash
   python3.10 --version
   ```

### 🐧 Linux (Fedora/RHEL)

1. **Install Python 3.10**

   ```bash
   sudo dnf install python3.10
   ```

2. **Verify Installation**

   ```bash
   python3.10 --version
   ```

---

## 🔑 Step 2: Getting Your Discord Token

Your Discord token is like a password that lets the bot log in as you. Here's how to get it:

### Method 1: Using Browser Developer Tools (Recommended)

1. **Open Discord in Your Browser**
   - Go to: <https://discord.com/app>
   - Log in to your account

2. **Open Developer Tools**
   - Press `F12` on your keyboard (or `Ctrl + Shift + I`)
   - Click on the "Application" tab at the top

3. **Find Your Token**
   - Click on Local storage little dropdown arrow
   - You saw a url of discord 
   - Click on it
   - In Right Scroll down to "token" not tokens
   - Copy the long text  that's your token!


⚠️ **IMPORTANT WARNINGS:**

- Never share your token with anyone!
- Don't post it in Discord servers or online
- If someone gets your token, they can control your account
- If your token gets leaked, change your Discord password immediately (this will reset your token)

---

## 📍 Step 3: Finding Channel IDs

You need to know which Discord channels you want the bot to work in. Here's how to find channel IDs:

### Enable Developer Mode

1. **Open Discord Settings**
   - Click the gear icon ⚙️ at the bottom left

2. **Go to Advanced Settings**
   - Scroll down to "Advanced" in the left sidebar
   - Click on it

3. **Enable Developer Mode**
   - Turn on the "Developer Mode" toggle
   - Close settings

### Copy Channel IDs

1. **Right-Click on a Channel**
   - In the channel list on the left, right-click any channel name

2. **Click "Copy ID"**
   - At the bottom of the menu, click "Copy ID"
   - The channel ID is now copied to your clipboard!

3. **Save the ID**
   - Paste it somewhere safe (like Notepad)
   - It will look like this: `1335308898566934628`

4. **Repeat for All Channels**
   - Copy IDs for all channels you want to use
   - You need at least 1 channel, but 2+ is better for stealth

💡 **Tips:**

- Use channels where you have permission to send messages
- Private channels or DMs work great
- Having 2+ channels lets the bot rotate between them (looks more human!)

---

## 📦 Step 4: Setting Up NeuraSelf

Now let's get NeuraSelf ready to run!

### Download NeuraSelf

1. **Get the Files**
   - Download the NeuraSelf folder
   - Extract it somewhere easy to find (like your Desktop or Documents)

2. **Open the Folder**
   - Navigate to the `NeuraSelf-UwU` folder

### Install Dependencies

#### 🪟 Windows

1. **Open Command Prompt in the Folder**
   - Hold `Shift` and right-click inside the NeuraSelf-UwU folder
   - Click "Open PowerShell window here" or "Open Command Prompt here"

2. **Install Required Libraries**

   ```bash
   pip install -r requirements.txt
   ```

   - Wait for all packages to install (this might take a few minutes)

#### 🍎 macOS / 🐧 Linux

1. **Open Terminal in the Folder**

   ```bash
   cd /path/to/NeuraSelf-UwU
   ```

   - Replace `/path/to/` with the actual path to your folder

2. **Install Required Libraries**

   ```bash
   pip3 install -r requirements.txt
   ```

   - Wait for installation to complete

---

## ⚙️ Step 5: Configuring settings.json

This is the most important step! Let's set up your bot configuration.

### Open settings.json

1. **Navigate to the config folder**
   - Inside NeuraSelf-UwU, open the `config` folder

2. **Open settings.json**
   - Right-click `settings.json`
   - Choose "Open with" → "Notepad" (Windows) or "TextEdit" (macOS)
   - Or use any text editor you like (VS Code, Sublime Text, etc.)

### Understanding the Structure

The settings file has several sections. Let's go through the important ones:

---

### 🔐 Adding Your Token and Channels

Find the `"accounts"` section at the top. It looks like this:

```json
"accounts": [
  {
    "token": "YOUR_TOKEN_HERE",
    "channels": ["CHANNEL_ID_1", "CHANNEL_ID_2"],
    "enabled": true
  }
]
```

**Here's what to do:**

1. **Replace `YOUR_TOKEN_HERE`** with your Discord token from Step 2
   - Keep the quotes around it!
   - Example: `"token": "MYDISCORDTOKEN"`

2. **Replace the channel IDs** with your channel IDs from Step 3
   - This is your **master channel list** - the bot can only work in these channels
   - Add as many as you want, separated by commas
   - Keep the quotes around each ID!
   - Example: `"channels": ["123456789012345678", "987654321098765432", "111222333444555666"]`

3. **Keep `"enabled": true`** - this means the account is active

**Example of a properly configured account:**

```json
"accounts": [
  {
    "token": "YOURUSERTOKENADDHERE",
    "channels": ["123456789012345678", "987654321098765432"],
    "enabled": true
  }
]
```

---

### 🔄 Setting Up Channel Rotation (Stealth Feature)

Scroll down to the `"utilities"` section and find `"channel_switcher"`:

```json
"utilities": {
  "channel_switcher": {
    "channels": ["CHANNEL_ID_1", "CHANNEL_ID_2"],
    "enabled": true,
    "interval": [300, 350]
  }
}
```

**Here's what to do:**

1. **Copy channel IDs from your master list** (the accounts section)
   - You need at least 2 channels for rotation to work
   - Example: `"channels": ["123456789012345678", "987654321098765432"]`

2. **Set `"enabled": true`** if you want channel rotation (recommended for stealth!)
   - Set to `false` if you only want to use one channel

3. **Adjust the interval** (optional)
   - `[300, 350]` means the bot will switch channels every 5-6 minutes
   - The numbers are in seconds
   - You can change these if you want

**Example:**

```json
"utilities": {
  "channel_switcher": {
    "channels": ["123456789012345678", "987654321098765432"],
    "enabled": true,
    "interval": [300, 350]
  }
}
```

💡 **Important Notes:**

- The channels in `channel_switcher` MUST also be in your master `accounts.channels` list
- If you only have 1 channel, set `"enabled": false` for channel_switcher
- More channels = better stealth (looks more human!)

---

### 🎯 Enabling/Disabling Features

You can turn features on or off in the `"commands"` section:

```json
"commands": {
  "hunt": {
    "enabled": true,
    "cooldown": [18, 20]
  },
  "battle": {
    "enabled": true,
    "cooldown": [18, 20]
  },
  "daily": {
    "enabled": true
  },
  "cookie": {
    "enabled": true,
    "userid": "USER_ID_TO_SEND_COOKIE"
  }
}
```

**What each setting means:**

- `"enabled": true` - Feature is ON
- `"enabled": false` - Feature is OFF
- `"cooldown": [18, 20]` - Random delay between 18-20 seconds
- `"userid"` - For cookie command, the user ID to send cookies to

**To find a user ID for cookies:**

1. Enable Developer Mode in Discord (see Step 3)
2. Right-click on the user's name
3. Click "Copy ID"
4. Paste it in the `"userid"` field

---

### 🎭 Typing Simulation Settings

In the `"stealth"` section, you can configure human-like typing:

```json
"stealth": {
  "typing": {
    "enabled": true,
    "min": 0.5,
    "max": 2.5,
    "typos": true,
    "mistake_rate": 0.1,
    "reaction_min": 0.8,
    "reaction_max": 2
  }
}
```

**What these mean:**

- `"enabled": true` - Typing simulation is ON (recommended!)
- `"min": 0.5` - Minimum typing speed (0.5 seconds per character)
- `"max": 2.5` - Maximum typing speed (2.5 seconds per character)
- `"typos": true` - Bot will make realistic typos and correct them
- `"mistake_rate": 0.1` - 10% chance of making a typo
- `"reaction_min/max"` - Delay before starting to type (looks human!)

💡 **Tip:** Keep typing simulation enabled for better stealth!

---

### 💾 Save Your Changes

1. **Save the file**
   - Press `Ctrl + S` (Windows/Linux) or `Cmd + S` (macOS)
   - Close the text editor

2. **Double-check your JSON**
   - Make sure all quotes are closed
   - Make sure all commas are in the right places
   - If you're not sure, you can use an online JSON validator: <https://jsonlint.com/>

---

## 🚀 Step 6: Running the Bot

You're ready to start NeuraSelf!

### 🪟 Windows

#### Option 1: Using the Setup Script (Easiest)

1. **Double-click `neura_setup.bat`**
   - This will check everything and start the bot
   - Follow any prompts that appear

#### Option 2: Manual Start

1. **Open Command Prompt in the folder**
   - Hold Shift + Right-click → "Open PowerShell window here"

2. **Run the bot**

   ```bash
   python main.py
   ```

### 🍎 macOS / 🐧 Linux

1. **Open Terminal in the folder**

   ```bash
   cd /path/to/NeuraSelf-UwU
   ```

2. **Run the bot**

   ```bash
   python3 main.py
   ```

### What You Should See

If everything is set up correctly, you'll see:

```
     ▄   ▄███▄     ▄   █▄▄▄▄ ██  
      █  █▀   ▀     █  █  ▄▀ █ █ 
  ██   █ ██▄▄    █   █ █▀▀▌  █▄▄█
  █ █  █ █▄   ▄▀ █   █ █  █  █  █
  █  █ █ ▀███▀   █▄ ▄█   █      █
  █   ██          ▀▀▀   ▀      █ 
                              ▀  
┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
 N E U R A   S E L F  •  Made by ROUTO
┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

[16:22:45] [SYS]      Ready as YourUsername
[16:22:45] [INFO]     Channel: 123456789012345678
[16:22:46] [SYS]      Loaded grinding.py
[16:22:46] [SYS]      Loaded huntbot.py
...
```

🎉 **Congratulations! Your bot is running!**

---

## 📊 Step 7: Using the Dashboard

NeuraSelf includes a web dashboard for easy control and monitoring!

### Accessing the Dashboard

1. **Open your web browser**
   - Chrome, Firefox, Edge, Safari - any browser works!

2. **Go to this address**

   ```
   http://localhost:8000
   ```

3. **You should see the dashboard!**

### Dashboard Tabs Explained

#### 🏠 Dashboard Tab

- **Real-time stats**: See how many commands have been sent
- **Uptime**: How long the bot has been running
- **Current status**: Is the bot active or paused?
- **Cash tracking**: Monitor your OwO cash growth

#### ⚙️ Configuration Tab

- **Edit all settings** without stopping the bot
- Change cooldowns, enable/disable features
- Changes apply instantly!

#### 🛡️ Security Tab

- **Solve captchas** when they appear
- View security event history
- See when the bot detected bans or captchas

#### 📈 History Tab

- **Charts and graphs** showing your progress
- Cash growth over time
- Command usage statistics
- Session history

#### 💻 System Terminal Tab

- **Live log feed** - see what the bot is doing in real-time
- Color-coded messages (green = success, red = error, etc.)
- Useful for troubleshooting

### Dashboard Controls

**Pause/Resume Button:**

- Click to pause the bot temporarily
- Click again to resume automation
- Useful when you want to use Discord manually

**Send Command:**

- Type any OwO command and send it manually
- The bot will send it for you
- Useful for quick checks like `owo cash` or `owo inv`

---

## 🔧 Troubleshooting

### Problem: "Python is not recognized"

**Solution:**

- You didn't check "Add Python to PATH" during installation
- Reinstall Python and make sure to check that box!
- Or manually add Python to PATH (Google: "add python to path [your OS]")

### Problem: "No module named discord"

**Solution:**

- You didn't install the requirements
- Run: `pip install -r requirements.txt`
- Make sure you're in the NeuraSelf-UwU folder when you run this

### Problem: Bot says "Invalid token"

**Solution:**

- Your token is wrong or expired
- Get a new token (see Step 2)
- Make sure you copied the ENTIRE token
- Check that there are no extra spaces in settings.json

### Problem: Bot doesn't send commands

**Solution:**

- Check that features are enabled in settings.json
- Make sure the channel ID is correct
- Verify you have permission to send messages in that channel
- Check the System Terminal in the dashboard for error messages

### Problem: "Channel not found"

**Solution:**

- Your channel ID is wrong
- Make sure you copied the ID correctly (it's a long number)
- The channel must be accessible by your Discord account
- Try using a different channel

### Problem: Bot gets captcha immediately

**Solution:**

- This is normal if you've been using other bots
- Solve the captcha in the Dashboard → Security tab
- Enable typing simulation for better stealth
- Use channel rotation with 2+ channels

### Problem: Dashboard won't open

**Solution:**

- Make sure the bot is running first
- Try: `http://127.0.0.1:8000` instead
- Check if another program is using port 8000
- Look for error messages in the terminal

### Problem: JSON syntax error

**Solution:**

- You have a typo in settings.json
- Common mistakes:
  - Missing comma between items
  - Missing quote mark
  - Extra comma at the end of a list
- Use <https://jsonlint.com/> to find the error
- Compare your file with the example in this guide

---

## 📚 Additional Resources

### Understanding Channel Configuration

**Master Channel List** (`accounts.channels`):

- This is the list of ALL channels the bot is allowed to use
- The bot will ONLY work in channels listed here
- Add every channel you might want to use

**Channel Switcher** (`utilities.channel_switcher.channels`):

- This is a subset of your master list
- The bot will rotate between these channels
- Must have at least 2 channels for rotation
- All channels here MUST also be in the master list

**Example Setup:**

```json
"accounts": [
  {
    "channels": ["111111", "222222", "333333"]  // Master list: 3 channels
  }
],
"utilities": {
  "channel_switcher": {
    "channels": ["111111", "222222"],  // Rotation: only 2 of the 3
    "enabled": true
  }
}
```

In this example:

- Bot can work in channels 111111, 222222, or 333333
- Bot will rotate between 111111 and 222222
- Channel 333333 is available but not used for rotation

---

## 🎯 Quick Reference

### Essential Settings Locations

| Setting | Location in settings.json |
|---------|---------------------------|
| Discord Token | `accounts[0].token` |
| Master Channel List | `accounts[0].channels` |
| Channel Rotation | `utilities.channel_switcher.channels` |
| Enable Hunt | `commands.hunt.enabled` |
| Enable Battle | `commands.battle.enabled` |
| Enable Daily | `commands.daily.enabled` |
| Cookie User ID | `commands.cookie.userid` |
| Typing Simulation | `stealth.typing.enabled` |

### Common Commands

| Platform | Command |
|----------|---------|
| Windows | `python main.py` |
| macOS/Linux | `python3 main.py` |
| Install packages | `pip install -r requirements.txt` |
| Check Python version | `python --version` |

---

## 💡 Tips for Best Results

1. **Use 2+ channels** for channel rotation - looks more human!
2. **Enable typing simulation** - makes the bot harder to detect
3. **Don't set cooldowns too low** - stick to the defaults (18-20 seconds)
4. **Check the dashboard regularly** - monitor for captchas and errors
5. **Start with basic features** - enable hunt/battle first, add more later
6. **Keep your token secret** - never share it with anyone!
7. **Use the dashboard** - it's easier than editing JSON files
8. **Read error messages** - they usually tell you what's wrong

---

## 🆘 Need More Help?

- **Check features.md** - See all available features and what they do
- **Join our Discord** - Get help from the community: <https://discord.gg/mHU4bESA4p>
- **Read the terminal** - Error messages often explain the problem
- **Check the dashboard** - System Terminal tab shows detailed logs

---

<div align="center">

**🧠 NeuraSelf** • Made by ROUTO • Happy Grinding! 🎮

</div>
