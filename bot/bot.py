import discord
import asyncio
import config
from discord.ext import commands

from elevenlabs import save
from elevenlabs.client import AsyncElevenLabs

eleven_client = AsyncElevenLabs(
    api_key=config.ELEVEN_LABS_API_KEY,
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents, application_id=config.APPLICATION_ID)

@bot.event
async def on_ready():
    # On ready, print that the bot is online
    print('Bot is Online.')

async def play_audio_in_channel(channel, audio):
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=f"audio/{audio}"))

    # Sleep while the bot is playing audio
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()

@bot.command()
async def hello(ctx):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send('You need to be in a voice channel.')
        return
    
    await play_audio_in_channel(voice_channel, 'nickelgoat.mp3')

    await ctx.message.delete()

@bot.command()
async def say(ctx, *, text):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send('You need to be in a voice channel.')
        return
    
    await ctx.message.delete()

    audio = await eleven_client.generate(
        text=text,
        voice='Callum',
        model='eleven_multilingual_v2'
    )
    out = b''
    async for value in audio:
        out += value

    save(out, 'audio.mp3')

    await play_audio_in_channel(voice_channel, 'audio.mp3')

async def main():
    # Start the bot
    await bot.start(config.TOKEN)

asyncio.run(main())