#!/usr/bin/env python3
import discord
from discord.ext import commands
import yt_dlp
import json

bot = commands.Bot(command_prefix="!")

queue = []  # list of dicts with keys 'title' and 'url'

async def play_next(ctx):
    if not queue:
        await ctx.send("Queue is empty")
        return

    next_track = queue.pop(0)
    source = discord.FFmpegPCMAudio(
        next_track["url"],
        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    )
    ctx.voice_client.play(source, after=lambda e: bot.loop.create_task(play_next(ctx)))
    await ctx.send(f"Now playing: {next_track['title']}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I am not connected to a voice channel.")

@bot.command()
async def play(ctx, *, query: str):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Join a voice channel first or use !join")
            return
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
        track = {"title": info["title"], "url": info["url"]}
        queue.append(track)
    if not ctx.voice_client.is_playing():
        await play_next(ctx)
    await ctx.send(f"Queued: {info['title']}")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Paused")
    else:
        await ctx.send("Nothing is playing")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Resumed")
    else:
        await ctx.send("Nothing is paused")

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Skipped")
    else:
        await ctx.send("Nothing is playing")

if __name__ == "__main__":
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        token = config.get("token")
    except FileNotFoundError:
        raise RuntimeError(
            "config.json not found. Copy config.json.example and add your Discord token."
        )
    if not token:
        raise RuntimeError("Discord token not provided in config.json")
    bot.run(token)
