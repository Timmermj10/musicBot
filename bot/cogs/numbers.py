import requests
import discord
from discord.ext import commands

# Create a new class for the cog
class Numbers(commands.Cog):
    # Initialize the class
    def __init__(self, bot):
        self.bot = bot

    # Listen for the on_ready event
    @commands.Cog.listener()
    async def on_ready(self):
        print('Numbers cog loaded.')

    # Create a command that sends a random fact about a number
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def facts(self, ctx, number):
        # Request the API
        response = requests.get(f"http://numbersapi.com/{number}")

        # Create an embed with the response text
        embed = discord.Embed(description=response.text)

        # Send the embed
        await ctx.channel.send(embed=embed)

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Numbers(bot))