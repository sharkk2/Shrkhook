from discord.ext import tasks, commands
import config
from helpers.attach import *


class ReAttach(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task.start()

    @tasks.loop(seconds=15)
    async def task(self):
        if not isAttached():
            attach()

async def setup(bot):
    global Bot 
    Bot = bot
    await bot.add_cog(ReAttach(bot))      