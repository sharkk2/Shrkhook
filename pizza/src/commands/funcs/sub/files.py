import discord
from discord import app_commands
from helpers.hardware import *
import typing
import config
from core.logger import logger

class Canopener(discord.ui.Modal, title='Open'): 
       def __init__(self, items, cpath):
          self.items = items
          self.cpath = cpath
          super().__init__()

       index = discord.ui.TextInput(label='Index number', max_length=3, required=True, placeholder="3, 6 or 14..")
      
       async def on_submit(self, interaction: discord.Interaction):
           index = self.index.value
           try:
               index = int(self.index.value.strip())
           except ValueError:
               await interaction.response.send_message("❌ | Invalid index", ephemeral=True)
               return
   
           if index < 0 or index >= len(self.items):
               await interaction.response.send_message("❌ | Index out of range", ephemeral=True)
               return
           
           selected = self.items[index]
           target = os.path.join(self.cpath, selected)        
           try:
               if os.path.isdir(target):
                   self.cpath = target
                   status, items, string = list_dir(self.cpath)
                   if status == False:
                       embed = discord.Embed(description=f"❌ | No permission", color=config.embederrorcolor)  
                       await interaction.response.send_message(embed=embed, ephemeral=True)
                       return
                   
                   embed = discord.Embed(
                       title="File Explorer",
                       description=f"Current path: `{self.cpath}`\nTotal items: **{len(items)}**\n```{string[:3900]}```",
                       color=config.embedcolor if status else config.embederrorcolor
                   )
                   await interaction.response.edit_message(embed=embed, view=Controller(self.cpath))
                   await interaction.followup.send("📂 | Opened directory", ephemeral=True)
               elif os.path.isfile(target):
                   size = os.path.getsize(target)
                   if size > 8 * 1024 * 1024:
                       await interaction.response.send_message("❌ | File is too large (max 8mb)", ephemeral=True)
                   else:
                       await interaction.response.send_message(file=discord.File(target), ephemeral=True)
               else:
                   await interaction.response.send_message("❌ | Not a valid file/directory", ephemeral=True)
           except Exception as e:
               logger.error(e)
               await interaction.response.send_message(f"❌ | Failed to open `{index}`", ephemeral=True)
           
           

class Controller(discord.ui.View):
  def __init__(self, cpath):
      self.cpath = cpath
      super().__init__(timeout=None)
      self.back.disabled = len(cpath) <= 3

      
      
  def render_view(self):
     status, items, string = list_dir(self.cpath)
     if status == False:
        embed = discord.Embed(description=f"❌ | No permission", color=config.embederrorcolor)  
        return embed, items
     embed = discord.Embed(
         title="File Explorer",
         description=f"Current path: `{self.cpath}`\nTotal items: **{len(items)}**\n```{string[:3900]}```",
         color=config.embedcolor if status else config.embederrorcolor
     )
     return embed, items    
    
         
  @discord.ui.button(label=f'Open', style=discord.ButtonStyle.primary, row=1, disabled=False)
  async def open(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
            status, items, string = list_dir(self.cpath)
            await interaction.response.send_modal(Canopener(items=items, cpath=self.cpath))
       except Exception as e:
          logger.error(e)
          
  @discord.ui.button(label=f'Back', style=discord.ButtonStyle.gray, row=1, disabled=False)
  async def back(self, interaction: discord.Interaction, button: discord.ui.Button):  
       try:
           self.cpath = os.path.dirname(self.cpath.rstrip("\\"))
           self.back.disabled = len(self.cpath.rstrip("\\").split("\\")) <= 1
           embed, _ = self.render_view()
           await interaction.response.edit_message(embed=embed, view=self)
       except Exception as e:
          logger.error(e)        

async def disks(interaction: discord.Interaction, current: str,) -> typing.List[app_commands.Choice[str]]:
    disks = Disk()
    diskids = []
    for disk in disks.disks:
        diskids.append(disk['name'])
    
    return [
        app_commands.Choice(name=fish, value=fish)
        for fish in diskids if current.lower() in fish.lower()
    ]
    
    
def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"    

def list_dir(path):
      try:
          items = os.listdir(path)
          string = ""
          for i, item in enumerate(items):
              full_path = os.path.join(path, item)
              size = ""
              if not os.path.isdir(full_path):
                  try:
                      size = f"({format_size(os.path.getsize(full_path))})"
                  except:
                      size = "??"
              string += f"{i:02d}: {'[DIR]' if os.path.isdir(full_path) else '     '} {item} {size}\n"
          return True, items, string
      except PermissionError:
          return False, [], string

@app_commands.command(name="files", description="File explorer")
@app_commands.autocomplete(disk=disks)
async def command(interaction: discord.Interaction, disk: str):
    disks = Disk()
    diskids = []
    for dis in disks.disks:
        diskids.append(dis['name'])
    
    if disk not in diskids:
        embed=discord.Embed(description=f"❌ | Invalid disk", color=config.embederrorcolor)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    cpath = f"{disk}\\"
    status, items, string = list_dir(cpath)  
    if status == False:
        embed = discord.Embed(description=f"❌ | No permission", color=config.embederrorcolor)  
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="File explorer", description=f"Current path: `{cpath}`\nTotal items: **{len(items)}**\n```{string[:3900]}```", color=config.embedcolor)
    await interaction.response.send_message(embed=embed, view=Controller(cpath))
      
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.get_command("functions").add_command(command)    