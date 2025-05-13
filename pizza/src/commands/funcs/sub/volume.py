import discord
from discord import app_commands
from helpers.volume import set_volume
import config

@app_commands.command(name="volume", description="Edit the windows media volume")
async def command(interaction: discord.Interaction, percent: int):
    if percent < 0 or percent > 100:
        embed = discord.Embed(description=f"❌ | Percentage must be a positive that is less than or equal to `100%`", color=config.embederrorcolor)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    set_volume(percent)
    
    embed = discord.Embed(title="Success", description=f"Volume editted to `{percent}%`", color=config.embedcolor)
    await interaction.response.send_message(embed=embed)
    
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    