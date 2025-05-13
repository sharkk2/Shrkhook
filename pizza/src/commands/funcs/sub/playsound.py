import discord
from discord import app_commands
import winsound
import config
import asyncio


@app_commands.command(name="playsound", description="Play a wav sound file")
async def command(interaction: discord.Interaction, sound: discord.Attachment):
    if sound.size > 10 * 1024 * 1024: 
      embed = discord.Embed(description="❌ | Sound is too big, maximum is `10MB`", color=config.embederrorcolor)
      await interaction.response.send_message(embed=embed, ephemeral=True)
      return
  
    if not sound.filename.endswith(".wav"):
        embed = discord.Embed(description="❌ | The file must be a `.wav` file.", color=config.embederrorcolor)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
  
    embed = discord.Embed(description=f"🎶 Playing sound...", color=config.embedcolor)
    await interaction.response.send_message(embed=embed)
    
    try:
        sBytes = await sound.read()
        await asyncio.to_thread(winsound.PlaySound, sBytes, winsound.SND_MEMORY)
    except Exception as e:
        embed = discord.Embed(description=f"❌ | Failed to play sound\n> Error: `{e}`", color=config.embederrorcolor)
        await interaction.edit_original_response(embed=embed)
        return
    
    embed = discord.Embed(title="Success", description="Sound played", color=config.embedcolor)
    await interaction.edit_original_response(embed=embed)
    
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    