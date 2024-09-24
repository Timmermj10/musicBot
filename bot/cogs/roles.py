import discord
from discord.ext import commands

class SurveyModal(discord.ui.Modal, title='Survey'):
    name = discord.ui.TextInput(label="Name", placeholder='Timi')
    answer = discord.ui.TextInput(label="Reason for joining", placeholder='I love team Blue!', style=discord.TextStyle.paragraph)
    async def on_submit(self, interaction):
        await interaction.response.send_message(f'Submission recieved.', ephemeral=True)


class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Blue', description='Blue role'),
            discord.SelectOption(label='Red', description='Red role'),
            discord.SelectOption(label='Green', description='Green role'),
        ]
        super().__init__(placeholder='Choose your team', max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        if self.values[0] == 'Blue':
            role = await guild.create_role(name='Blue', color=discord.Color.blue())
        elif self.values[0] == 'Red':
            role = await guild.create_role(name='Red', color=discord.Color.red())
        elif self.values[0] == 'Green':
            role = await guild.create_role(name='Green', color=discord.Color.green())

        await user.edit(roles=[role])
        await interaction.response.send_modal(SurveyModal())

class SelectView(discord.ui.View):
    def __init__(self, *, timeout=30):
        super().__init__(timeout=timeout)
        self.add_item(Select())

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Role cog loaded.')

    @commands.command()
    async def role(self, ctx):
        await ctx.send('Select your team:', view=SelectView(), delete_after=10)

async def setup(bot):
    await bot.add_cog(Role(bot))