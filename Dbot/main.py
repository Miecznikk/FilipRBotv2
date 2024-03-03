import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import queue
from utils.models.roles import GameRole
from rest_client import RestClient

load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX") + " "


class FilipRBot(commands.Bot):
    audio_queue = queue.Queue()
    game_roles = []

    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents(voice_states=True, guilds=True,
                                                                        guild_messages=True, message_content=True))
        self.restclient = RestClient()
        self.load_game_roles()
        self.add_commands()

    async def on_ready(self):
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

        @self.command(name="wolaj")
        async def call_for_game(ctx, *args):
            await ctx.send(f"{args}")

    def load_game_roles(self):
        for obj in self.restclient.get_game_roles():
            self.game_roles.append(GameRole(**obj))


def main():
    bot = FilipRBot()
    try:
        bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired as error:
        return error


if __name__ == "__main__":
    main()
