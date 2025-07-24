import config
import discord
from discord import app_commands
import pyperclip
import core.clipdata as clipdata
from discord import ui

class entryAdder(ui.Modal, title='Add entry'): 
       def __init__(self):
          super().__init__()

       text = ui.TextInput(label='Text', max_length=1024, required=True, placeholder="lorem ipsum nig", style=discord.TextStyle.paragraph)
       async def on_submit(self, interaction: discord.Interaction):
           try:
             pyperclip.copy(self.text.value)
             clipdata.clipdata.append(self.text.value)
             
             clipStr = ""
             for e in clipdata.clipdata:
                 if e == "":
                     continue
             
                 e = e[:1024] + "..." if len(e) > 1021 else e
                 f = f"```{e}```"
                 if len(clipStr) + len(f) > 4096:
                     break
                 clipStr += f
     
                 if not clipStr:
                     clipStr = "*Clipboard is empty*"
         
                 embed = discord.Embed(
                     title="Clipboard Contents",
                     description=clipStr,
                     color=config.embedcolor
                 )
         
             await interaction.response.edit_message(embed=embed)
           except Exception as e:
               await self.bot.error(interaction, self.bot, e)  
           
class ClipPanel(discord.ui.View):
  def __init__(self):
      super().__init__(timeout=None)
      
  @discord.ui.button(label=f'Add entry', style=discord.ButtonStyle.primary, row=1, disabled=False)
  async def Add(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            await interaction.response.send_modal(entryAdder())
       except Exception as e:
          await Bot.error(interaction, Bot, e)      
         
  @discord.ui.button(label=f'Clear clipboard', style=discord.ButtonStyle.red, row=1, disabled=False)
  async def Clear(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            clipdata.clipdata.clear()
            pyperclip.copy("")
            embed = discord.Embed(title="Clipboard Contents", description="*Clipboard is empty*", color=config.embedcolor)
            await interaction.response.edit_message(embed=embed)
       except Exception as e:
          await Bot.error(interaction, Bot, e)  
          
  @discord.ui.button(label=f'Refresh', style=discord.ButtonStyle.gray, row=2, disabled=False)
  async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            clipStr = ""
            for e in clipdata.clipdata:
                if e == "":
                    continue
            
                e = e[:1024] + "..." if len(e) > 1021 else e
                f = f"```{e}```"
                if len(clipStr) + len(f) > 4096:
                    break
                clipStr += f
    
            if not clipStr:
                clipStr = "*Clipboard is empty*"
    
            embed = discord.Embed(
                title="Clipboard Contents",
                description=clipStr,
                color=config.embedcolor
            )
    
            await interaction.response.edit_message(embed=embed, view=ClipPanel())
       except Exception as e:
          await Bot.error(interaction, Bot, e)         


@app_commands.command(name="clipboard", description="Read the clipboard")
async def command(interaction: discord.Interaction):
    try:
        clipStr = ""
        for e in clipdata.clipdata:
            if e == "":
                continue
        
            e = e[:1024] + "..." if len(e) > 1021 else e
            f = f"```{e}```"
            if len(clipStr) + len(f) > 4096:
                break
            clipStr += f

        if not clipStr:
            clipStr = "*Clipboard is empty*"

        embed = discord.Embed(
            title="Clipboard Contents",
            description=clipStr,
            color=config.embedcolor
        )

        await interaction.response.send_message(embed=embed, view=ClipPanel())
    except Exception as e:
        await Bot.error(interaction, Bot, e)

async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    