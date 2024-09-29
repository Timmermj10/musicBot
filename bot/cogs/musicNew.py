import discord
import config
import asyncio
import yt_dlp
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.queues = {}
        self.voice_clients = {}
        self.yt_dl_options = {"format": "bestaudio/best", "noplaylist": True, "verbose": True}
        self.ytdl = yt_dlp.YoutubeDL(self.yt_dl_options)

        self.ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}

    async def play_next(self, ctx):
        if self.queues[ctx.guild.id] != []:
            player, title = self.queues[ctx.guild.id].pop(0)
            
            await ctx.send(f'Playing {title}')
            await self.play_song(ctx, player)
    
    async def play_song(self, ctx, player):
        self.voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run(self.play_next(ctx)))
    
    async def find251(self, formats):
        for format in formats:
            # print(format['format_id'])
            if format['format_id'] == '251':
                return format

    async def search_yt(self, ctx, query):
        await ctx.send('Searching for song...')
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(f"ytsearch:{query} + official", download=False)['entries'][0])
        format_251 = await self.find251(data['formats'])

        song = format_251['url']

        player = discord.FFmpegOpusAudio(song, **self.ffmpeg_options)

        return player, data['title']

    async def connect_voice(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('You are not in a voice channel.')
            return False
        if not self.voice_clients or ctx.guild.id not in self.voice_clients:
            voice_client = await ctx.author.voice.channel.connect()
            self.voice_clients[voice_client.guild.id] = voice_client
            return True
        return True

    @commands.command(name='play', help='Plays a selected song from Youtube')
    async def play(self, ctx, *args):
        # Check if the user passed in any arguments
        if args == ():
            if ctx.guild.id in self.queues and len(self.queues[ctx.guild.id]) > 0:
                # Connect the bot to the voice channel
                connection = await self.connect_voice(ctx)
                if connection:
                    await self.play_next(ctx)
            else:
                await ctx.send('Please provide a song to play.')
            return

        try:
            # Connect the bot to the voice channel
            connection = await self.connect_voice(ctx)
            if not connection:
                return
            player, title = await self.search_yt(ctx, ' '.join(args))

            await ctx.send(f'Playing {title}')
        
            self.voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run(self.play_next(ctx)))
        except Exception as e:
            print(e)

    @commands.command(name='pause', help='Pauses the current song')
    async def pause(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].pause()
        except Exception as e:
            print(e)

    @commands.command(name='resume', help='Resumes the current song')
    async def resume(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].resume()
        except Exception as e:
            print(e)

    @commands.command(name='stop', help='Stops the current song and leaves the voice channel')
    async def stop(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].stop()
            await self.voice_clients[ctx.guild.id].disconnect()
            del self.voice_clients[ctx.guild.id]
        except Exception as e:
            print(e)

    @commands.command(name='queue', help='Displays the current queue')
    async def queue(self, ctx, *args):
        if ctx.guild.id not in self.queues:
            self.queues[ctx.guild.id] = []
        
        # Get the player and title of the song and add it to the queue
        player, title = await self.search_yt(ctx, ' '.join(args))
        self.queues[ctx.guild.id].append((player, title))
        await ctx.send(f'Added {title} to the queue.')

    @commands.command(name='skip', help='Skips the current song')
    async def skip(self, ctx):
        self.voice_clients[ctx.guild.id].stop()
        if ctx.guild.id in self.queues and len(self.queues[ctx.guild.id]) > 0:
            await self.play_next(ctx)
        else:
            await ctx.send('No more songs in queue.')

    @commands.command(name='clear', help='Clears the current queue')
    async def clear(self, ctx):
        if ctx.guild.id in self.queues:
            self.queues[ctx.guild.id].clear()
            await ctx.send('Queue cleared.')
        else:
            await ctx.send('Nothing in Queue.')


async def setup(bot):
    # Pass the GUILD_ID (Server ID) to the question cog to be used in the ctx.guild parameter)
    await bot.add_cog(Music(bot), guilds=[discord.Object(id=config.GUILD_ID)])