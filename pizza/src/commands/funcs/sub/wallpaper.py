import discord
from discord import app_commands
import config
from helpers.wallpaper import set_wallpaper

@app_commands.command(name="wallpaper", description="Set a wallpaper")
async def command(interaction: discord.Interaction, wallpaper: discord.Attachment):
    if wallpaper.size > 12 * 1024 * 1024: 
      embed = discord.Embed(description="❌ | Wallpaper is too big, maximum is `12MB`", color=config.embederrorcolor)
      await interaction.response.send_message(embed=embed, ephemeral=True)
      return
  
    
    if not wallpaper.filename.endswith((".jpg", ".jpeg", ".png", ".bmp")):
        embed = discord.Embed(description="❌ | Wallpaper image type is not supported\n> Supported: `.jpg, .jpeg, .png, .bmp`", color=config.embederrorcolor)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
  
    embed = discord.Embed(description=f"🖼 Setting wallpaper", color=config.embedcolor)
    await interaction.response.send_message(embed=embed)
    
    try:
        extension = wallpaper.filename.split(".")[-1]
        wBytes = await wallpaper.read()
        
        set_wallpaper(wBytes, extension)
    except Exception as e:
        embed = discord.Embed(description=f"❌ | Failed to set wallpaper\n> Error: `{e}`", color=config.embederrorcolor)
        await interaction.edit_original_response(embed=embed)
        return
    
    embed = discord.Embed(title="Success", description="Wallpaper successfully set", color=config.embedcolor)
    embed.set_image(url=wallpaper.url)
    await interaction.edit_original_response(embed=embed)
    
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    