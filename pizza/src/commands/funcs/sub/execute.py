import discord
from discord import app_commands
import subprocess
import config
from typing import Literal

@app_commands.command(name="execute", description="Run a windows command/script")
@app_commands.describe(script="The script to execute", script_type="Use powershell or cmd")
async def command(interaction: discord.Interaction, script: str, script_type: Literal["cmd", "powershell"]):
    try:
       startupinfo = subprocess.STARTUPINFO()
       startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

       if script_type == "powershell":
           result = subprocess.run(["powershell", "-Command", script], capture_output=True, text=True, startupinfo=startupinfo)
       else:
           result = subprocess.run(script, shell=True, capture_output=True, text=True, startupinfo=startupinfo)
       output = result.stdout
       error = False
       if len(output) == 0:
           output = result.stderr
           if len(output) == 0:
             output = "No output"
           else:
             error = True  
             
       ihatediscord = output[:1750] + "..." if len(output) > 1750 else output
             
       embed = discord.Embed(title="Script executed", description=f"\n> Error: `{error}`\n> Using: **{script_type}**\nOutput:\n```{ihatediscord}```", color=config.embedcolor if not error else config.embederrorcolor)
       await interaction.response.send_message(embed=embed)
    except Exception as e:
        embed = discord.Embed(description=f"❌ | Failed to execute script\n> Error: `{e}`", color=config.embederrorcolor)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    
    
    