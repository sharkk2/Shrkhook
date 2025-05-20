import discord
from discord import app_commands
import pyautogui
from io import BytesIO
import config
from core.logger import logger

@app_commands.command(name="screenshot", description="Take a screenshot")
async def command(interaction: discord.Interaction):
    try:
      await interaction.response.defer(thinking=True)
      screenshot = pyautogui.screenshot()
      b = BytesIO()
      screenshot.save(b, format="PNG")
      b.seek(0)
      
      embed = discord.Embed(title="Screenshot", color=config.embedcolor)
      embed.set_image(url="attachment://screenshot.png")
      await interaction.followup.send(embed=embed, file=discord.File(b, "screenshot.png"))
    except Exception as e:
        logger.error(f"Failed to take screenshot: {e}")
        await Bot.error(interaction, Bot, e) # shit error handler fr
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    