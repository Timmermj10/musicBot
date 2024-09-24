import requests
import discord
from discord.ext import commands

class Numbers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Numbers cog loaded.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def facts(self, ctx, number):
        # Request the API
        response = requests.get(f"http://numbersapi.com/{number}")

        # Create an embed with the response text
        embed = discord.Embed(description=response.text)

        # Send the embed
        await ctx.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Numbers(bot))