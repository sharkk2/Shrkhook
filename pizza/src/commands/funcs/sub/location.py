import discord
from discord import app_commands
from helpers.location import get_location
from helpers.locgen import genMap
import config
from core.logger import logger

@app_commands.command(name="location", description="Get the exact physical location of the computer")
async def command(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
      location = get_location()
      lat = location["latitude"]
      lon = location['longitude']
      
      mapb = genMap(lat, lon)
      
      embed = discord.Embed(title="Location", description=f"Latitdue: `{lat}`\nLongitude: `{lon}`", color=config.embedcolor)
      embed.set_image(url="attachment://map.png")
      await interaction.followup.send(embed=embed, file=discord.File(mapb, "map.png"))
    except Exception as e:
      embed = discord.Embed(description=f"Failed to get location: `{e}`", color=config.embederrorcolor)
      await interaction.followup.send(embed=embed)
      logger.error(e)    
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    