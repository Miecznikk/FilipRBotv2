import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import queue
import requests


load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX") + " "


class FilipRBot(commands.Bot):
    audio_queue = queue.Queue()

    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents(voice_states=True, guilds=True,
                                                                        guild_messages=True, message_content=True))

        self.add_commands()

    async def on_ready(self):
        url = 'http://127.0.0.1:8000/authenticate/'
        credentials = {
            'username' : "apiuser",
            'password' : 'haslo23'
        }
        response = requests.post(url, data=credentials)
        if response.status_code == 200:
            token = response.json()['token']
            print(token)
        print(f"Logged in as {self.user}")

    async def play_next(self, ctx):
        if self.audio_queue.empty():
            return

        audio_source = self.audio_queue.get()
        ctx.voice_client.play(audio_source,
                              after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.loop))

    def add_commands(self):
        @self.command(name="hi")
        async def hi(ctx):
            await ctx.send("siema lubisz mnie troszke???")

            try:
                response = await self.wait_for("message", timeout=30.0,
                                               check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
            except asyncio.TimeoutError:
                await ctx.send("KURWA ODPOWIESZ KIEDYS?")
                return

            if response.content.lower() == "ta":
                await ctx.send("SLODZIAK")
            elif response.content.lower() == "no":
                await ctx.send("A TO SIE PIERDOL")
            else:
                await ctx.send("CO TY PIERDOLISZ?")

        @self.command(name="join")
        async def join(ctx):
            if ctx.author.voice is None or ctx.author.voice.channel is None:
                await ctx.send("GDZIE MAM KURWA WEJSC CYMBALE")
                return

            vc = ctx.author.voice.channel
            if ctx.voice_client is None:
                await vc.connect()
            else:
                await ctx.voice_client.move_to(vc)

        @self.command(name="play")
        async def play(ctx):
            if ctx.voice_client is None:
                await ctx.send("NIE MA MNIE NA CHANNELU ZJEBIE")
                return

            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)

        @self.command(name="add")
        async def add_to_queue(ctx, item):
            self.audio_queue.put(discord.FFmpegPCMAudio(item))
            await ctx.send(f"DODALEM TO {item} DO KOLEJKI")


def main():
    bot = FilipRBot()
    try:
        bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired as error:
        return error


if __name__ == "__main__":
    main()
