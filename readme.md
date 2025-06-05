# discord command and control

[![License](https://img.shields.io/github/license/Asko7779/discord-c-c)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)

> **Discord command-and-control script which can run multiple tasks on a target machine via use of webhooks and a Discord bot.**

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Security Disclaimer](#security-disclaimer)
- [Contributing](#contributing)

---

## Features

- 📡 Remote command execution via Discord
- 🤖 Easy setup with Discord bot and webhooks
- 📝 Multi-task support on target machine
- 🛡️ Lightweight and fully written in Python
- ⚡ Real-time communication between client and Discord

---

## Requirements

- Python 3.7 or higher
- Required Python packages (see [requirements.txt](requirements.txt))
- Discord account & server (with permission to add bots)

---

## Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/Asko7779/discord-c-c.git
    cd discord-c-c
    ```

2. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

---

## Configuration

1. **Create a Discord Bot**
    - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
    - Create a new application and add a bot to it
    - Copy the bot token for later use

2. **Set up Webhooks**
    - In your Discord server, create a new webhook in your desired channel
    - Copy the webhook URL

3. **Configure the script**
    - Edit the configuration section in the main script or create a `.env` file with your bot token and webhook URL:
      ```
      DISCORD_BOT_TOKEN=your_bot_token_here
      WEBHOOK_URL=your_webhook_url_here
      ```

---

## Usage

1. **Start the script**
    ```sh
    python3 main.py
    ```
2. **Control the target machine**
    - Use Discord commands (via bot or webhook) to send tasks or instructions
    - View responses directly in your Discord channel

---

## Security Disclaimer

> **This project is intended for educational, research, and authorized use only**
> 
> Unauthorized use of this tool on machines you do not own or without explicit permission is strictly prohibited and may violate laws or Discord's terms of service.

---

## Contributing

Contributions and suggestions are welcome!  
Feel free to open issues or pull requests

---

---

**Star** the repo if you found this useful! ⭐
