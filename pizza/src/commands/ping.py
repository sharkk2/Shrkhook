import discord
from discord import app_commands
from core.functions.bot.check_perms import check_perms




@app_commands.command(name="ping", description="Ping the bot")
async def ping(interaction: discord.Interaction):
 #   if await check_perms(interaction, ["kick_members"], Bot) == False:
 #      return
    latency = Bot.latency * 1000
    await interaction.response.send_message(f"Pong! `{round(latency)}`ms")
    
    
    
    
async def setup(bot):
    global Bot 
    Bot = bot
    bot.tree.add_command(ping)    