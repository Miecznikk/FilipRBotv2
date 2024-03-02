import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX") + " "

audio_queue = [discord.FFmpegPCMAudio(path) for path in ["audio/laszczyk.mp3", "audio/laszczyk2.mp3"]]


class FilipRBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents(voice_states=True, guilds=True,
                                                                        guild_messages=True, message_content=True))
        self.add_commands()

    async def on_ready(self):
        print(f"Logged in as {self.user}")

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


def main():
    bot = FilipRBot()
    try:
        bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired as error:
        return error


# @bot.command("join")
# async def join(ctx):
#     if ctx.author.voice is None or ctx.author.voice.channel is None:
#         await ctx.send("DAJ MI KURWA ADMINA NA TYM SERWERZE")
#         return
#
#     vc = ctx.author.voice.channel
#     if ctx.voice_client is None:
#         await vc.connect()
#     else:
#         await ctx.voice_client.move_to(vc)
#
#
# @bot.command("play")
# async def play(ctx):
#     if ctx.voice_client is None:
#         await ctx.send("NIE MA MNIE NA CHANNELU ZJEBIE")
#         return
#
#     if not ctx.voice_client.is_playing():
#         await play_next(ctx)

#
# async def play_next(ctx):
#     if not audio_queue:
#         return
#
#     audio_source = audio_queue.pop(0)
#
#     ctx.voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop))


if __name__ == "__main__":
    main()
