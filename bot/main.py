import discord
import config
import asyncio
import os

# Importing the commands extension
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents, application_id=config.APPLICATION_ID)

@bot.event
async def on_ready():
    # On ready, print that the bot is online
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

async def load():
    # Load the cogs from the cogs folder
    for file in os.listdir('./cogs'):
        # Check if the file is a python file
        if file.endswith('.py'):
            # Load the cog
            await bot.load_extension(f'cogs.{file[:-3]}')

async def setup():
    # Perform any setup tasks here
    print('Setting up...')

    # Load the cogs
    print('Loading cogs...')
    await load()

async def main():
    # Call setup
    await setup()

    # Start the bot
    await bot.start(config.TOKEN)

# Initiate the main sequence
asyncio.run(main())