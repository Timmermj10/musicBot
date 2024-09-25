import discord
import config
from discord.ext import commands
from discord import app_commands

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Music cog loaded.')

    # Sync the '/' commands with the server
    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'Synced {len(fmt)} commands.')

    # Create a slash command '/play'
    @app_commands.command(name='play', description='Play a song')
    async def play(self, interaction: discord.Interaction):
        # Respond with 'Playing song'
        await interaction.response.send_message(f'Playing song')

async def setup(bot):
    # Pass the GUILD_ID (Server ID) to the question cog to be used in the ctx.guild parameter)
    await bot.add_cog(Music(bot), guilds=[discord.Object(id=config.GUILD_ID)])