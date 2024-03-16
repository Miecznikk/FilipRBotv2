import asyncio
import random

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context, errors
from discord.ext.commands._types import BotT
from dotenv import load_dotenv
import os
import queue
import argparse
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
    configurators = None

    def __init__(self, config):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents(members=True, voice_states=True, guilds=True,
                                                                        guild_messages=True, message_content=True))

        self.config = config
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
        self.get_configurators()
        self.check_members_on_voice_channels.start()
        if self.config['--rj']:
            self.decide_and_join_channel.start(int(os.getenv("JOIN_RATE")))

    def add_commands(self):
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
        @self.command(name="pokaz", aliases=['poka'])
        async def show_rank(ctx, rank=None):
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
                    await ctx.send(self.get_time_ranked_members_string())
                elif member_response.content.lower() == "punktow":
                    await ctx.send("JESZCZE NIE LICZE PUNKTOW BO MNIE DOMCIO NIE NAUCZYL")
                else:
                    await ctx.send("NIE MA TKAIEGO RANKINGU DEBILU")

        @channel_check(CHANNEL_NAME)
        @self.command(name="jaka", aliases=['jak'])
        async def check_weather(ctx, weather=None):
            if weather == "pogoda":
                await ctx.send("BARDZO LADNA POGODA")

    async def random_message(self, ctx):
        await ctx.send("random")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound) and ctx.channel.name == CHANNEL_NAME:
            await self.random_message(ctx)
        else:
            self.logger.info(f"Something went wrong: {error}")

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

    @tasks.loop(minutes=1)
    async def decide_and_join_channel(self, join_chance):
        voice_channels = self.guilds[0].voice_channels

        eligible_channels = [channel for channel in voice_channels if len(channel.members) >= 1]

        if not eligible_channels:
            return
        vc = self.guilds[0].voice_client
        if random.randint(1, 100) <= join_chance and not vc:
            random_channel = random.choice(eligible_channels)
            try:
                audio_path = self.restclient.get_random_connect_audio()
            except ValueError as e:
                self.logger.error(e)
                return
            audio_source = discord.FFmpegPCMAudio(audio_path)
            vc = await random_channel.connect()
            vc.play(audio_source, after=lambda e: self.disconnect_voice(vc))

    def get_time_ranked_members_string(self):
        ranking_message = "OTO NAJWIEKSZE NOLIFY NA TYM LEWACKIM DISCORDZIE: \n"
        members = [Member(**data) for data in self.restclient.get_time_ranking()]
        for i, member in enumerate(members):
            dc_member = discord.utils.get(self.guilds[0].members, name=member.name)
            if dc_member:
                ranking_message += f"{i + 1}. {get_member_nickname(dc_member)} ({dc_member.name}) - {convert_to_time(member.minutes_spent)}\n"
        return ranking_message

    def get_configurators(self):
        self.configurators = [Member(**member) for member in self.restclient.get_discord_members() if
                              member['configurator']]

    def disconnect_voice(self, vc):
        if vc:
            asyncio.run_coroutine_threadsafe(vc.disconnect(), vc.loop)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rj', type=int, default=1, help='Random joining 0-off 1-on')

    args = parser.parse_args()

    config = {
        "--rj": args.rj
    }

    bot = FilipRBot(config)
    try:
        bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired as error:
        return error


if __name__ == "__main__":
    main()
