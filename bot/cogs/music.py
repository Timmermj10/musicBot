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
        # Get the user's voice state
        user_voice = interaction.user.voice

        # Check if the user is in a voice channel
        if not user_voice:
            # Respond with 'You need to be in a voice channel to play a song'
            await interaction.response.send_message(f'You need to be in a voice channel to play a song', ephemeral=True)
            return

        bot_voice = interaction.guild.voice_client

        # If the bot is already in a voice channel
        if bot_voice:
            # If the bot is in the same voice channel as the user
            if bot_voice.channel.id == user_voice.channel.id:
                # Respond with 'Bot is already playing a song'
                await interaction.response.send_message(f'Bot is in your voice channel', ephemeral=True)
                return
            # If the bot is in a different voice channel, move the bot to the user's voice channel
            await bot_voice.move_to(user_voice.channel)
            await interaction.response.send_message(f'Moved bot to your voice channel', ephemeral=True)
            return
        
        # If the bot is not in a voice channel, join the user's voice channel
        await user_voice.channel.connect()
        await interaction.response.send_message(f'Joined your voice channel', ephemeral=True)

async def setup(bot):
    # Pass the GUILD_ID (Server ID) to the question cog to be used in the ctx.guild parameter)
    await bot.add_cog(Music(bot), guilds=[discord.Object(id=config.GUILD_ID)])