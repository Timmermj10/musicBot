import discord
import config
import asyncio
import yt_dlp
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # All music related data structures
        self.isPlaying = False

        # 2D array [song, channel]
        self.queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        
        self.vc = None

    # Search the song on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    # Play next song
    def play_next(self):
        # If we have a song in the queue
        if len(self.queue) > 0:
            # Mark the bot as playing
            self.isPlaying = True

            # Get the url of the song
            url = self.queue[0][0]['source']

            # Pop the song from the queue
            self.queue.pop(0)

            # Play the song
            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.isPlaying = False

    # Infinite loop checker
    async def check_queue(self):
        if len(self.queue) > 0:
            # Mark the bot as playing
            self.isPlaying = True

            # Get the url of the song
            url = self.queue[0][0]['source']

            # Try to connect to the voice channel if the bot is not already connected
            if not self.vc or not self.vc.is_connected():
                self.vc = await self.queue[0][1].connect()
            else:
                await self.vc.move_to(self.queue[0][1])

            print(self.music_queue)
            #  Pop the song from the queue
            self.queue.pop(0)

            # Play the song
            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.isPlaying = False

    @commands.command(name='play', help='Plays a selected song from Youtube')
    async def p(self, ctx, *args):
        query = ' '.join(args)

        voice_channel = discord.utils.get(ctx.guild.voice_channels, name='general')
        if not voice_channel:
            await ctx.send('You need to be in a voice channel.')
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send(f'Added {song["title"]} to the queue')
                self.queue.append([song, voice_channel])

                if self.isPlaying == False:
                    await self.check_queue()

    @commands.command(name='queue', help='Displays the current music queue')
    async def q(self, ctx):
        if len(self.queue) == 0:
            await ctx.send('No music in queue')
        else:
            queue_list = ''
            for i in range(len(self.queue)):
                queue_list += self.queue[i][0]['title'] + '\n'
            await ctx.send(queue_list)

    @commands.command(name='skip', help='Skips the current song')
    async def skip(self, ctx):
        if self.vc:
            # Stop the current song
            self.vc.stop()

            # Try and play the next song in the queue
            await self.check_queue()

    @commands.command(name='leave', help='Leaves the voice channel')
    async def leave(self, ctx):
        if self.vc:
            # Disconnect from the voice channel
            await self.vc.disconnect()

            # Update the vc variable
            self.vc = None

    @commands.command(name='pause', help='Pauses the current song')
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("No audio is playing right now.")

    @commands.command(name='resume', help='Resumes the current song')
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")

async def setup(bot):
    # Pass the GUILD_ID (Server ID) to the question cog to be used in the ctx.guild parameter)
    await bot.add_cog(Music(bot), guilds=[discord.Object(id=config.GUILD_ID)])