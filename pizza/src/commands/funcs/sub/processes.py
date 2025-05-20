import discord
from discord import app_commands
import config
from core.logger import logger
from helpers.processes import *



class Terminator(discord.ui.View):
  def __init__(self, pro):
      self.pro = pro
      super().__init__(timeout=None)
         
  @discord.ui.button(label=f'Kill', style=discord.ButtonStyle.red, row=1, disabled=False)
  async def kill(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            self.pro.kill()
            embed = discord.Embed(description="✅ | Process killed", color=config.embedcolor)
            await interaction.response.edit_message(embed=embed, view=None)
            
       except Exception as e:
          embed = discord.Embed(description="❌ | Failed to kill process", color=config.embederrorcolor)
          logger.error(e)  
          await interaction.response.send_message(embed=embed, ephemeral=True)
            


class title(discord.ui.Modal, title='Process'): 
       def __init__(self):
          super().__init__()

       norpid = discord.ui.TextInput(label='Name or PID', max_length=100, required=True, placeholder="notepad.exe... or 1234...")
       async def on_submit(self, interaction: discord.Interaction):
           isName = False
           try:
               int(self.norpid.value)
           except:
               isName = True   
               
           pro = None    
           if isName:
               pro = getProcess(self.norpid.value)    
           else:
               pro = fetchProcess(int(self.norpid.value))    
           
           if not pro:
               embed = discord.Embed(description="❌ | Process not found", color=config.embederrorcolor)    
               await interaction.response.send_message(embed=embed, ephemeral=True)
               return
           
           await interaction.response.defer()
           embed = discord.Embed(title=pro.name(), description=f"{pro.name()} (`{pro.pid}`):\n> Started <t:{int(pro.create_time())}:R>\n> User: `{pro.username()}`\n> Running: {pro.is_running()}", color=config.embedcolor)
           await interaction.followup.send(embed=embed, view=Terminator(pro))

class Controller(discord.ui.View):
  def __init__(self):
      super().__init__(timeout=None)
         
  @discord.ui.button(label=f'All Processes', style=discord.ButtonStyle.primary, row=1, disabled=False)
  async def Name(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            pros = processes()
            bigahhstr = ""
            for pro in pros:
                bigahhstr += f"{pro.name()}: pid({pro.pid}) | "
            embed = discord.Embed(description=f"```{bigahhstr[:4087]}...```", color=config.embedcolor)
            await interaction.response.send_message(embed=embed, ephemeral=True)    
       except Exception as e:
          logger.error(e)
          
  @discord.ui.button(label=f'Get process', style=discord.ButtonStyle.primary, row=1, disabled=False)
  async def proc(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            await interaction.response.send_modal(title())
       except Exception as e:
          logger.error(e)        
  
  @discord.ui.button(label=f'Refresh', style=discord.ButtonStyle.gray, row=2, disabled=False)
  async def reff(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
          strr = ""
          pros = getFgs()
          apros = processes()
          for p in pros:
              if p.is_running():
                strr += f"> **{p.name()}**: `PID-{p.pid}` ({p.username()})\n"
          embed = discord.Embed(title="Process manager", description=f"Total foreground processes: **{len(pros)}**\nTotal background processes: **{len(apros) - len(pros)}** (total: `{len(apros)}`)\n**Foreground processes**:\n{strr}", color=config.embedcolor)
          embed.set_footer(text="Some processes aren't allowed to be accessed")
          await interaction.response.edit_message(embed=embed, view=Controller())    
       except Exception as e:
        logger.error(e)   

@app_commands.command(name="processes", description="Process manager")
async def command(interaction: discord.Interaction):
    try:
        strr = ""
        pros = getFgs()
        apros = processes()
        for p in pros:
            if p.is_running():
              strr += f"> **{p.name()}**: `PID-{p.pid}` ({p.username()})\n"
        embed = discord.Embed(title="Process manager", description=f"Total foreground processes: **{len(pros)}**\nTotal background processes: **{len(apros) - len(pros)}** (total: `{len(apros)}`)\n**Foreground processes**:\n{strr}", color=config.embedcolor)
        embed.set_footer(text="Some processes aren't allowed to be accessed")
        await interaction.response.send_message(embed=embed, view=Controller())    
    except Exception as e:
        logger.error(e)   
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    