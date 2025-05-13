import discord
from discord import app_commands
import config
from typing import Literal
from helpers.popup import show_notification

@app_commands.command(name="notification", description="Send a windows notification popup")
async def command(interaction: discord.Interaction, title: str, message: str, type: Literal['info', 'warning', 'question', 'error', 'none']):
    ntypes = {
        'info': 0,
        'warning': 1,
        'question': 2,
        'error': 3,
        'none': 4
    }
    
    try:
      ntype = ntypes[type]
      show_notification(title, message, ntype)
      embed = discord.Embed(title="Success", description=f"Showed a `{type}` notification with:\n> Title: **{title}**\n> Message: ```{message}```", color=config.embedcolor)
      await interaction.response.send_message(embed=embed)
    except Exception as e:
      embed = discord.Embed(title="Error", description=f"❌ | Failed to show notification\n> Error: `{e}`", color=config.embederrorcolor)
      await interaction.response.send_message(embed=embed, ephemeral=True)
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    