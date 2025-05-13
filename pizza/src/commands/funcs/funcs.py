from discord import app_commands

COMMAND_GUILDS = []
COMMAND_NAME = "functions"
COMMAND_DESCRIPTION = "Functions"

class commandgroup(app_commands.Group):
  ...
  
  
async def setup(bot):
    global Bot 
    Bot = bot 
    bot.tree.add_command(commandgroup(
      name=COMMAND_NAME,
      description=COMMAND_DESCRIPTION, 
      guild_only=True if COMMAND_GUILDS else False,
      guild_ids=COMMAND_GUILDS if COMMAND_GUILDS else None
    ))            