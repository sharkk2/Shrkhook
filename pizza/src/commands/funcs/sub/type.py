import discord
from discord import app_commands
from helpers.type import type
import config

@app_commands.command(name="type", description="Type text")
async def command(interaction: discord.Interaction, text: str, wpm: int = 100, enter: bool = False):
   embed = discord.Embed(title="Typer", description=f"Typing `{text}` with `{wpm}`wpm\n> Auto press enter: `{enter}`", color=config.embedcolor)
   await interaction.response.send_message(embed=embed)
   type(text, wpm, enter)
   from core.logger import logger

    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    