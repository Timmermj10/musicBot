import discord
from discord import app_commands
from discord.ext import commands
import config

class Questions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Questions cog loaded.')

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'Synced {len(fmt)} commands.')

    @app_commands.command(name='ping', description='Ask a question')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'pong')


async def setup(bot):
    await bot.add_cog(Questions(bot), guilds=[discord.Object(id=config.GUILD_ID)])