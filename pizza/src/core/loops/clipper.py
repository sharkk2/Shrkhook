from discord.ext import tasks, commands
import pyperclip
from ..clipdata import clipdata
import config

class Clipper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clipboard.start()

    @tasks.loop(seconds=3)
    async def clipboard(self):
         c = pyperclip.paste()
         if c and c not in clipdata:
             clipdata.append(c)
             if len(clipdata) > config.max_clipboard_size:
                 clipdata.pop(0)
                
             
         
async def setup(bot):
    global Bot 
    Bot = bot
    await bot.add_cog(Clipper(bot))      