import discord
from discord import app_commands
import subprocess
import config


@app_commands.command(name="url", description="Open a URL")
async def command(interaction: discord.Interaction, url: str):
    try:
      if not url.startswith("http://") or not url.startswith("https://"):
          url = f"https://{url}"
          
      subprocess.Popen(
          ["cmd", "/c", "start", "", url],
          shell=True,
          creationflags=subprocess.CREATE_NO_WINDOW
      )
      embed = discord.Embed(description=f"✅ | Opened `{url}`", color=config.embedcolor)
      await interaction.response.send_message(embed=embed)
    except Exception as e:
      await Bot.error(interaction, Bot, e)    
      
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    