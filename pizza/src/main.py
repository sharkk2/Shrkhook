import discord
from datetime import datetime
from discord.ext import commands
import asyncio
import config
from core.functions.sync_db import sync_db
from core.logger import logger


prefix = config.prefix

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)
bot.remove_command('help')



@bot.event
async def on_ready():
   try:  
     if config.maintainance:
       logger.warning("Maintainance mode is on!")
     logger.info("Loading...")
     await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=f"Loading.."))
     bot.start_time = datetime.utcnow()
     
     from core.handlers import commands, events, task_handler      
     from core.functions.bot.error import error
     from core.functions.bot.check_perms import check_perms
     
     bot.error = error 
     bot.check_perms = check_perms
     
     await commands.register_commands(bot) 
     await events.register_events(bot)
     await task_handler.register_tasks(bot)
     if config.connectDB:
       logger.info(f"Syncing database")           
       try:
         await sync_db(bot)
         logger.info(f"Database synced successfully")     
       except Exception as e:
         logger.warning(f"Failed to sync database: {e}")
         
      
     try: 
       # bot.add_view(View())    
       ...
     except Exception as e:
       logger.warning(e)                         
                                                                                                 
     try:
       if bot.persistent_views:
         for view in bot.persistent_views:
           logger.info(f"Refreshed {view.__class__.__name__} '{len(view.children)} item(s)'")
       
       synced = await bot.tree.sync()  
       
       logger.info(f"Synced {len(synced)} command(s)") 
     except Exception as e:
       print(e)
     if config.maintainance == True:  
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Under Maintainance"))
     
   except Exception as e:
       logger.fatal(e)


@bot.command()
async def hey(ctx):
  await ctx.send("ayo wsup")

  

async def main():
    async with bot:      
       try:
         #if config.connectDB:
          # bot.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(config.mongouri)
         await bot.start(config.token)
       except Exception as e:   
         logger.fatal(e)

if __name__ == "__main__":  
  asyncio.run(main())              
  
