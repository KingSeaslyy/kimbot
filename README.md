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
3. Provide your Discord bot token via a `.env` file or a config file. To use a
   config file, copy `config.json.example` to `config.json` and edit the token
   value:
   ```bash
   cp config.json.example config.json
   # then edit config.json and set the "token" value
   ```
   Alternatively, copy `.env.example` to `.env` and set the `DISCORD_TOKEN`
   variable or export `DISCORD_TOKEN` in your environment. AMP's Python App
   Runner will automatically read the `.env` file.
   Ensure the "Message Content Intent" is enabled for your bot in the Discord
   Developer Portal.
4. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

- `!join` - Join the caller's voice channel.
- `!leave` - Leave the current voice channel.
- `!play <query>` - Search YouTube and queue the first result.
- `!pause` - Pause the current track.
- `!resume` - Resume playback.
- `!skip` - Skip the current track.

Tracks are queued and played in order.
