import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import queue
from rest_client import RestClient
import logging

load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX") + " "

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)


class FilipRBot(commands.Bot):
    audio_queue = queue.Queue()
    game_roles = []

    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents(members=True, voice_states=True, guilds=True,
                                                                        guild_messages=True, message_content=True))
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] FilipRBot: %(message)s", "%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

        self.restclient = RestClient()
        self.add_commands()

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user}")

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
            try:
                game_role = self.restclient.get_game_role(args[-1])[0]
                role = discord.utils.get(self.guilds[0].roles, name=game_role['name'])
            except ValueError:
                await ctx.send("NA CO KURWA?")
                return
            self.logger.info(f"Found following role: {game_role['name']}")
            await ctx.send("DOBRA WOLAM ICH KURWA NA " + game_role['game_assigned'].upper())

            for member in self.guilds[0].members:
                if role in member.roles:
                    if member.voice is None:
                        self.logger.info(f"Sending message to {member.name}")
                        await member.send("SIEMA KURWO CHODZ GRAC NA SPOCONE RECZNIKI W "
                                          + game_role['game_assigned'].upper())


def main():
    bot = FilipRBot()
    try:
        bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired as error:
        return error


if __name__ == "__main__":
    main()
