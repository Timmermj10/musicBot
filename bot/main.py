import discord
import config
import asyncio
import requests

# Importing the commands extension
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.command()
async def facts(ctx, number):
    response = requests.get(f"http://numbersapi.com/{number}")
    await ctx.channel.send(response.text)

@bot.event
async def on_ready():
    print('Bot is Online.')

@bot.event
async def on_message(message):
    # Process commands first
    await bot.process_commands(message)

    # If the message follows the command format, ignore it
    if message.content.startswith('.'):
        return
    
    # If the message was sent by the bot itself, ignore it
    if message.author == bot.user:
        return
    
    # If the message starts with 'hello', respond with a greeting
    if message.content.startswith('hello'):
        await message.channel.send('Hello friend!')

async def setup():
    print('Setting up...')

async def main():
    await setup()
    await bot.start(config.TOKEN)

asyncio.run(main())