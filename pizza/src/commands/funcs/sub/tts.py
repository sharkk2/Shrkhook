import discord
from discord import app_commands
import time
import config
from helpers.tts import speak_tts

@app_commands.command(name="tts", description="Play a text to speech sound using windows tts engine")
async def command(interaction: discord.Interaction, text: str):
    embed = discord.Embed(description=f"🔊 TTS: `{text}`", color=config.embedcolor)
    await interaction.response.send_message(embed=embed)
    speak_tts(text)
    time.sleep(1.2)
    embed = discord.Embed(title="Success", description="TTS played!", color=config.embedcolor)
    await interaction.edit_original_response(embed=embed)
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    