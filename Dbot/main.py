import asyncio
import datetime
import json

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import queue

from utils.utils import get_member_nickname, convert_to_time, channel_check
from utils.models.Member import Member
from utils.models.roles import GameRole
from rest_client import RestClient
import logging

load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX") + " "
CHANNEL_NAME = os.getenv("CHANNEL_NAME")


class FilipRBot(commands.Bot):
    audio_queue = queue.Queue()

    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents(members=True, voice_states=True, guilds=True,
                                                                        guild_messages=True, message_content=True))
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        self.active_members = {}

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] FilipRBot: %(message)s", "%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

        self.restclient = RestClient()
        self.add_commands()

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user}")
        self.check_members_on_voice_channels.start()
        print(CHANNEL_NAME)

    async def play_next(self, ctx):
        if self.audio_queue.empty():
            return

        audio_source = self.audio_queue.get()
        ctx.voice_client.play(audio_source,
                              after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.loop))

    def add_commands(self):
        @channel_check(CHANNEL_NAME)
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

        @channel_check(CHANNEL_NAME)
        @self.command(name="play")
        async def play(ctx):
            if ctx.voice_client is None:
                await ctx.send("NIE MA MNIE NA CHANNELU ZJEBIE")
                return

            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)

        @channel_check(CHANNEL_NAME)
        @self.command(name="add")
        async def add_to_queue(ctx, item):
            self.audio_queue.put(discord.FFmpegPCMAudio(item))
            await ctx.send(f"DODALEM TO {item} DO KOLEJKI")

        @channel_check(CHANNEL_NAME)
        @self.command(name="wolaj")
        async def call_for_game(ctx, *args):
            try:
                game_role = GameRole(**self.restclient.get_game_role(args[-1])[0])
                role = discord.utils.get(self.guilds[0].roles, name=game_role.name)
            except ValueError:
                await ctx.send("NA CO KURWA?")
                return
            self.logger.info(f"Found following role: {game_role.name}")
            await ctx.send("DOBRA WOLAM ICH KURWA NA " + game_role.game_assigned.upper())

            for member in self.guilds[0].members:
                if role in member.roles:
                    if member.voice is None:
                        self.logger.info(f"Sending message to {member.name}")
                        await member.send("SIEMA KURWO CHODZ GRAC NA SPOCONE RECZNIKI W "
                                          + game_role.game_assigned.upper())

        @channel_check(CHANNEL_NAME)
        @self.command(name="pokaz")
        async def show_rank(ctx, rank=None):
            self.logger.info(f"Executing show rank method")
            if rank == "ranking":
                await ctx.send("JAKI TY KURWA RANKING CHCESZ ZJEBIE? CZASU CZY PUNKTOW")
                try:
                    member_response = await self.wait_for("message", timeout=10.0,
                                                          check=lambda
                                                              m: m.author == ctx.author and m.channel == ctx.channel)
                except asyncio.TimeoutError:
                    await ctx.send("DOBRA NIE WIEM KURWA ILE TY SIE ZASTANAWIAC BEDZIESZ")
                    return
                if member_response.content.lower() == "czasu":
                    await ctx.send(self.get_time_ranked_members())
                elif member_response.content.lower() == "punktow":
                    await ctx.send("JESZCZE NIE LICZE PUNKTOW BO MNIE DOMCIO NIE NAUCZYL")
                else:
                    await ctx.send("NIE MA TKAIEGO RANKINGU DEBILU")

    @tasks.loop(minutes=1)
    async def check_members_on_voice_channels(self):
        self.logger.info("Checking channels for active users")
        for member in self.guilds[0].members:
            if member.voice:
                if member in self.active_members:
                    self.active_members[member] += 1
                    self.logger.info(
                        f"Member {member.name} has been active for {self.active_members[member]} minutes")
                else:
                    self.active_members[member] = 0
                    self.logger.info(f"Member {member.name} just joined the channel")
            else:
                if member in self.active_members:
                    self.logger.info(f"Member {member.name} just disconnected")
                    try:
                        self.restclient.set_new_minutes_spent(member.name, self.active_members[member])
                        del self.active_members[member]
                    except ValueError:
                        self.logger.info(f"Couldn't send request for member {member.name}")

    def get_time_ranked_members(self):
        ranking_message = "OTO NAJWIEKSZE NOLIFY NA TYM LEWACKIM DISCORDZIE: \n"
        members = [Member(**data) for data in self.restclient.get_time_ranking()]
        for i, member in enumerate(members):
            dc_member = discord.utils.get(self.guilds[0].members, name=member.name)
            if dc_member:
                ranking_message += f"{i + 1}. {get_member_nickname(dc_member)} - {convert_to_time(member.minutes_spent)}\n"
        return ranking_message


def main():
    bot = FilipRBot()
    try:
        bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired as error:
        return error


if __name__ == "__main__":
    main()
