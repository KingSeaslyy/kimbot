# kimbot

A simple Discord music bot using `discord.py` and `yt-dlp`.

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd kimbot
   ```
2. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```
   Ensure `ffmpeg` is installed on your system for audio playback.
   This bot has been tested with `discord.py==2.3.2` and `yt-dlp==2024.4.27`.
3. Copy `config.json.example` to `config.json` and edit it to include your
   Discord bot token. Alternatively set the token via the `DISCORD_TOKEN`
   environment variable:
   ```bash
   cp config.json.example config.json
   # then edit config.json and set the "token" value
   ```
   If `config.json` is missing or the `token` field is empty, `bot.py`
   will use the value of `DISCORD_TOKEN` if it is set.
4. Run the bot:
   ```bash
   python bot.py
   # or execute it directly
   ./bot.py
   ```

## Commands

- `!join` - Join the caller's voice channel.
- `!leave` - Leave the current voice channel.
- `!play <query>` - Search YouTube and queue the first result.
- `!pause` - Pause the current track.
- `!resume` - Resume playback.
- `!skip` - Skip the current track.

Tracks are queued and played in order.

## AMP integration

If you are using CubeCoders AMP, the repository includes `amp_module.py` which
registers the bot as a managed server. AMP will load this file automatically and
start `bot.py` as a Python application.

When AMP launches the bot it expects `config.json` to be in its working directory (usually alongside `bot.py` and `amp_module.py`). If the file is missing, the bot will not start. Check AMP's logs for an error about the missing config if this happens.

