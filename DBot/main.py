import asyncio
import datetime
import random

import discord
import yaml
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import queue
import argparse
from utils.utils import get_member_nickname, convert_to_time, channel_check, check_in_call
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
    commands_config = None
    julia_call = False

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
        self.load_commands_config()
        self.add_commands()

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user}")
        self.get_configurators()
        self.check_members_on_voice_channels.start()
        if self.config['--rj']:
            self.decide_and_join_channel.start(int(os.getenv("JOIN_RATE")))

    def add_commands(self):
        @check_in_call(self)
        @channel_check(CHANNEL_NAME)
        @self.command(name=self.commands_config['call_for_game']['command_name'])
        async def call_for_game(ctx, *args):
            if len(args) < 2:
                return
            try:
                game_role = GameRole(**self.restclient.get_game_role(args[-1])[0])
                role = discord.utils.get(self.guilds[0].roles, name=game_role.name)
            except ValueError:
                await ctx.send(random.choice(self.commands_config['call_for_game']['value_error']))
                return
            self.logger.info(f"Found following role: {game_role.name}")
            await ctx.send(
                f"{random.choice(self.commands_config['call_for_game']['calling'])} {game_role.game_assigned.upper()}")

            for member in self.guilds[0].members:
                if role in member.roles:
                    if member.voice is None:
                        self.logger.info(f"Sending message to {member.name}")
                        await member.send(
                            f"{random.choice(self.commands_config['call_for_game']['message'])} {game_role.game_assigned.upper()}")

        @check_in_call(self)
        @channel_check(CHANNEL_NAME)
        @self.command(name=self.commands_config['show_rank']['command_name'],
                      aliases=self.commands_config['show_rank']['aliases'])
        async def show_rank(ctx, rank=None):
            if rank == self.commands_config['show_rank']['argument_required']:
                class RankingView(discord.ui.View):
                    def __init__(self, time_method, points_method):
                        super().__init__()
                        self.time_method = time_method
                        self.points_method = points_method

                    @discord.ui.button(label="Czasu", custom_id="time_button", style=discord.ButtonStyle.secondary,
                                       emoji="⏱")
                    async def time_callback(self, interaction, button):
                        if ctx.author.id == interaction.user.id:
                            for child in self.children:
                                if isinstance(child, discord.ui.Button):
                                    child.disabled = True
                            await interaction.response.edit_message(embed=self.time_method(), view=self)

                    @discord.ui.button(label="Punktow", custom_id="points_button", style=discord.ButtonStyle.secondary,
                                       emoji="💯")
                    async def points_callback(self, interaction, button):
                        if ctx.author.id == interaction.user.id:
                            for child in self.children:
                                if isinstance(child, discord.ui.Button):
                                    child.disabled = True
                            await interaction.response.send_message(embed=self.points_method(), view=self)

                await ctx.send(random.choice(self.commands_config['show_rank']['types_response']),
                               view=RankingView(self.get_time_ranked_members_embed, None))

        @check_in_call(self)
        @channel_check(CHANNEL_NAME)
        @self.command(name="jaka", aliases=['jak'])
        async def check_weather(ctx, weather=None):
            if weather == "pogoda":
                await ctx.send("BARDZO LADNA POGODA")

        @channel_check(CHANNEL_NAME)
        @self.command(name="test")
        async def test(ctx):
            class MyView(discord.ui.View):
                @discord.ui.button(label="CLICK ME!", style=discord.ButtonStyle.primary)
                async def button_callback(self, interaction, button):
                    await interaction.response.send_message("You clicked me")

            await ctx.send("hejka", view=MyView())

    async def random_message(self, ctx):
        if not self.julia_call:
            if random.randint(1, 100) <= int(os.getenv("JULIA_CALL_RATE")):
                await ctx.send("JULIA DZWONI ZW")
                self.julia_call = True
                await asyncio.sleep(int(os.getenv("JULIA_CALL_TIMEOUT")))
                self.julia_call = False
                await ctx.send("DOBRA JUZ JESTEM")

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
                self.restclient.set_new_minutes_spent(member.name, 1)

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

    def get_time_ranked_members_embed(self):
        medals_emojis = {
            1: ":first_place:",
            2: ":second_place:",
            3: ":third_place:",
            4: "4.",
            5: "5."
        }
        embed = discord.Embed(title=random.choice(self.commands_config['show_rank']['ranking_starting_string']['time']),
                              color=discord.Color.yellow(),
                              timestamp=datetime.datetime.now())
        members = [Member(**data) for data in self.restclient.get_time_ranking()]
        for i, member in enumerate(members):
            dc_member = discord.utils.get(self.guilds[0].members, name=member.name)
            if dc_member:
                embed.add_field(name=medals_emojis[i + 1],
                                value=f"**```{get_member_nickname(dc_member)} ({dc_member.name})"
                                      f" - {convert_to_time(member.minutes_spent)}```**", inline=False)
        return embed

    def get_configurators(self):
        self.configurators = [Member(**member) for member in self.restclient.get_discord_members() if
                              member['configurator']]

    def disconnect_voice(self, vc):
        if vc:
            asyncio.run_coroutine_threadsafe(vc.disconnect(), vc.loop)

    def load_commands_config(self):
        with open('commands_config.yaml', 'r') as yaml_file:
            self.commands_config = yaml.safe_load(yaml_file)
        self.logger.info("Loaded commands config")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rj', type=int, default=1, help='Random joining 0-off 1-on')
    args = parser.parse_args()

    config = {
        "--rj": args.rj,
    }

    bot = FilipRBot(config)
    try:
        bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired as error:
        return error


if __name__ == "__main__":
    main()
