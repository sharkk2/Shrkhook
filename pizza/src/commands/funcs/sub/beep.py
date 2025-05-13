import discord
from discord import app_commands
import winsound
import config
import asyncio


@app_commands.command(name="beep", description="Play a beep sound")
async def command(interaction: discord.Interaction):
    embed = discord.Embed(description=f"🔊 Beeping..", color=config.embedcolor)
    await interaction.response.send_message(embed=embed)
    try:
        frequency = 1000  
        duration = 3500  
        await asyncio.to_thread(winsound.Beep, frequency, duration)
    except Exception as e:
        embed = discord.Embed(description=f"❌ | Failed beep\n> Error: `{e}`", color=config.embederrorcolor)
        await interaction.edit_original_response(embed=embed)
        return
    
    embed = discord.Embed(title="Success", description="Beeped!", color=config.embedcolor)
    await interaction.edit_original_response(embed=embed)
    
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    