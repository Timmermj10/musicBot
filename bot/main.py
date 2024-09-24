import discord
import config
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot is Online.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello friend!')

async def setup():
    print('Setting up...')

async def main():
    await setup()
    await client.start(config.TOKEN)

asyncio.run(main())