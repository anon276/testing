import discord
from discord.ext import commands
from random import randint
from random import choice
import random
import aiohttp
import asyncio
import os.path
import os
import __main__
from .utils import checks
from PIL import Image, ImageFont, ImageDraw

main_path = os.path.dirname(os.path.realpath(__main__.__file__))

class Chgk:
    """Chgk commands."""
	
    def __init__(self, bot):
        self.bot = bot
        self.audio = self.bot.get_cog('Audio')
            #VAPE       158683939764961281
            #GENERAL    101868866996547584
        self.voice_channel = discord.Object(id="101868866996547584")
        self.channel = discord.Object(id="101868866954604544")

    @commands.command(aliases="s", pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def score(self, ctx, value:str):
        if len(value) == 2:
            left = value[0]; right = value[1]
            if left.isdigit() and right.isdigit():
                fnt = ImageFont.truetype(main_path + '/resources/OpenSans-Bold.ttf', 225)
                img = Image.new('RGB', (300, 300))
                line = ImageDraw.Draw(img)
                line.line((0, 0) + (0, 300), fill=(15, 100, 250), width=300)
                line.line((300, 0) + (300, 300), fill=(255, 255, 255), width=300)
                imgDrawer = ImageDraw.Draw(img)
                imgDrawer.text((10, 0), left, font=fnt)
                imgDrawer.text((162, 0), right, font=fnt, fill=(15, 100, 250))
                img.save(main_path + "/resources/score.png")
                await self.bot.send_file(self.channel, main_path + '/resources/score.png')
                mus = random.choice(os.listdir(main_path + "/resources/chgk/music"))
                if not self.bot.is_voice_connected():
                    await self.bot.join_voice_channel(self.voice_channel)
                self.audio.music_player.stop()
                self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/music/" + mus, options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
                self.audio.music_player.paused = False
                self.audio.music_player.start()

    @commands.command(pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def start(self, ctx):
        if not self.bot.is_voice_connected():
            await self.bot.join_voice_channel(self.voice_channel)
        await self.bot.send_file(self.channel, main_path + '/resources/chgk/WhatWhereWhen.png')
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/nachalo.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.start()
        while True:
            if not self.audio.music_player.is_playing():
                self.audio.music_player.stop()
                self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Thus_Sprach_Zarathustra.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
                self.audio.music_player.paused = False
                self.audio.music_player.start()
                break
            await asyncio.sleep(1)

    @commands.command(aliases="1", pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def volchok(self, ctx):
        if not self.bot.is_voice_connected():
            await self.bot.join_voice_channel(self.voice_channel)
        await self.bot.send_file(self.channel, main_path + '/resources/chgk/ruletka.jpg')
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Volchok.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def blackbox(self, ctx):
        if not self.bot.is_voice_connected():
            await self.bot.join_voice_channel(self.voice_channel)
        await self.bot.send_file(self.channel, main_path + '/resources/chgk/BlackBox.jpg')
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Ra-ta-ta.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(aliases="2", pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def gong(self, ctx):
        if not self.bot.is_voice_connected():
            await self.bot.join_voice_channel(self.voice_channel)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/gong.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(aliases="3", pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def timer(self, ctx):
        if not self.bot.is_voice_connected():
            await self.bot.join_voice_channel(self.voice_channel)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Signal_2.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()
        await asyncio.sleep(80)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Signal_1.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()
        await asyncio.sleep(10)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Signal_2.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def sich(self, ctx):
        if not self.bot.is_voice_connected():
            await self.bot.join_voice_channel(self.voice_channel)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Homage_To_The_Mountain.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(aliases="w",pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def win(self, ctx, left:str, right:str):
        await self.bot.say("**Победила команда знатоков со счетом {}:{}!**".format(left, right))
        fnt = ImageFont.truetype(main_path + '/resources/OpenSans-Bold.ttf', 225)
        img = Image.new('RGB', (300, 300))
        line = ImageDraw.Draw(img)
        line.line((0, 0) + (0, 300), fill=(15, 100, 250), width=300)
        line.line((300, 0) + (300, 300), fill=(255, 255, 255), width=300)
        imgDrawer = ImageDraw.Draw(img)
        imgDrawer.text((10, 0), left, font=fnt)
        imgDrawer.text((162, 0), right, font=fnt, fill=(15, 100, 250))
        img.save(main_path + "/resources/score.png")
        await self.bot.send_file(self.channel, main_path + '/resources/score.png')

        if not self.bot.is_voice_connected():
            await self.bot.join_voice_channel(self.voice_channel)
        img = random.choice(os.listdir(main_path + "/resources/chgk/win"))
        await self.bot.send_file(ctx.message.channel, main_path + '/resources/chgk/win/' + img)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Dance_Macabre.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(aliases="l", pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def lose(self, ctx, left:str, right:str):
        await self.bot.send_message(self.channel, "**Победила команда телезрителей со счетом {}:{}!**".format(left, right))
        fnt = ImageFont.truetype(main_path + '/resources/OpenSans-Bold.ttf', 225)
        img = Image.new('RGB', (300, 300))
        line = ImageDraw.Draw(img)
        line.line((0, 0) + (0, 300), fill=(15, 100, 250), width=300)
        line.line((300, 0) + (300, 300), fill=(255, 255, 255), width=300)
        imgDrawer = ImageDraw.Draw(img)
        imgDrawer.text((10, 0), left, font=fnt)
        imgDrawer.text((162, 0), right, font=fnt, fill=(15, 100, 250))
        img.save(main_path + "/resources/score.png")
        await self.bot.send_file(self.channel, main_path + '/resources/score.png')

        if not self.bot.is_voice_connected():
            await self.bot.join_voice_channel(self.voice_channel)
        img = random.choice(os.listdir(main_path + "/resources/chgk/lose"))
        await self.bot.send_file(self.channel, main_path + '/resources/chgk/lose/' + img)
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Dance_Macabre.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def muzika(self, ctx):
        if not self.bot.is_voice_connected():
            await self.bot.join_voice_channel(self.voice_channel)
        await self.bot.send_file(self.channel, main_path + '/resources/chgk/music.png')
        mus = random.choice(os.listdir(main_path + "/resources/chgk/blues"))
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/blues/" + mus, options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

    @commands.command(pass_context=True, no_pm=False)
    #@checks.is_owner()
    async def endgame(self, ctx):
        if not self.bot.is_voice_connected():
            await self.bot.join_voice_channel(self.voice_channel)
        await self.bot.send_file(self.channel, main_path + '/resources/chgk/WhatWhereWhen.png')
        self.audio.music_player.stop()
        self.audio.music_player = self.audio.bot.voice.create_ffmpeg_player(main_path + "/resources/chgk/Max_Greger__Orchestra_-_Serenade_In_Blue.mp3", options='''-filter:a "volume={}"'''.format(self.audio.settings["VOLUME"]))
        self.audio.music_player.paused = False
        self.audio.music_player.start()

def setup(bot):
    bot.add_cog(Chgk(bot))
