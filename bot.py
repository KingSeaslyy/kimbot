#!/usr/bin/env python3
"""Simple Discord music bot ready for AMP's Python App Runner."""

import asyncio
import json
import os
from typing import Tuple

import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

queue: asyncio.Queue[Tuple[str, str]] = asyncio.Queue()


def get_audio(query: str) -> Tuple[str, str]:
    """Return direct audio URL and title for the first YouTube search result."""
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)["entries"][0]
        return info["url"], info["title"]


async def play_next(ctx: commands.Context) -> None:
    if ctx.voice_client is None:
        return
    if queue.empty():
        await ctx.send("Queue is empty")
        return
    url, title = await queue.get()
    source = discord.FFmpegPCMAudio(url)
    ctx.voice_client.play(
        source,
        after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop),
    )
    await ctx.send(f"Now playing: {title}")


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")


@bot.command()
async def join(ctx: commands.Context) -> None:
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.send("You are not in a voice channel.")


@bot.command()
async def leave(ctx: commands.Context) -> None:
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I am not connected to a voice channel.")


@bot.command()
async def play(ctx: commands.Context, *, query: str) -> None:
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Join a voice channel first or use !join")
            return
    url, title = get_audio(query)
    await queue.put((url, title))
    await ctx.send(f"Queued: {title}")
    if not ctx.voice_client.is_playing():
        await play_next(ctx)


@bot.command()
async def pause(ctx: commands.Context) -> None:
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Paused")
    else:
        await ctx.send("Nothing is playing")


@bot.command()
async def resume(ctx: commands.Context) -> None:
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Resumed")
    else:
        await ctx.send("Nothing is paused")


@bot.command()
async def skip(ctx: commands.Context) -> None:
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Skipped")
    else:
        await ctx.send("Nothing is playing")


def load_token() -> str:
    token = os.getenv("DISCORD_TOKEN")
    if token:
        return token
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("token", "")
    except FileNotFoundError:
        pass
    raise RuntimeError(
        "Discord token not provided. Set DISCORD_TOKEN or create config.json"
    )


if __name__ == "__main__":
    bot.run(load_token())
