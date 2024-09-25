import discord
from discord.ext import commands

# Class for working with the Survey Modal
class SurveyModal(discord.ui.Modal, title='Survey'):
    # Display the TextInput components in the modal
    name = discord.ui.TextInput(label="Name", placeholder='Timi')
    answer = discord.ui.TextInput(label="Reason for joining", placeholder='I love team Blue!', style=discord.TextStyle.paragraph)

    # Wait for the user to submit the form and send confirmation message
    async def on_submit(self, interaction):
        await interaction.response.send_message(f'Submission recieved.', ephemeral=True)

# Class for selecting a role within the Select View
class Select(discord.ui.Select):
    # Initialize the Select class with the three role options
    def __init__(self):
        options = [
            discord.SelectOption(label='Blue', description='Blue role'),
            discord.SelectOption(label='Red', description='Red role'),
            discord.SelectOption(label='Green', description='Green role'),
        ]
        super().__init__(placeholder='Choose your team', max_values=1, min_values=1, options=options)

    # Create a callback method that assigns the role to the user when the user selects an option
    async def callback(self, interaction: discord.Interaction):
        # Get the user and guild from the interaction
        user = interaction.user
        guild = interaction.guild

        # Create the role on the fly based on the user's selection
        if self.values[0] == 'Blue':
            role = await guild.create_role(name='Blue', color=discord.Color.blue())
        elif self.values[0] == 'Red':
            role = await guild.create_role(name='Red', color=discord.Color.red())
        elif self.values[0] == 'Green':
            role = await guild.create_role(name='Green', color=discord.Color.green())

        # Set the user's role
        await user.edit(roles=[role])

        # Display the survey modal
        await interaction.response.send_modal(SurveyModal())

# Class for displaying the Select component in a view
class SelectView(discord.ui.View):
    # Initialize the view and set a timeout of 30 seconds
    def __init__(self, *, timeout=30):
        super().__init__(timeout=timeout)
        
        # Add the Select component to the view
        self.add_item(Select())

# Class for the role cog
class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Role cog loaded.')

    # Create a command that sends a select menu to choose a role (.role)
    @commands.command()
    async def role(self, ctx):
        await ctx.send('Select your team:', view=SelectView(), delete_after=10)

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Role(bot))