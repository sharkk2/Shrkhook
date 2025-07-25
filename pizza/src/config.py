### REQUIRED DATA ###

import discord
from datetime import datetime
import os
import sys

cd = datetime.now().strftime('%Y-%m-%d %I.%M.%S')

### BOT CONFIG ###

intver = 1.6
version = 'v1.6.0b NOSOCKET'
attach_shortcut_name = "Win32Updater"
max_clipboard_size = 8

prefix = 's.'
mongouri = ''
connectDB = False
owner_ids = [1092548532180877415]
main_guild = 1339949261756043336
embedcolor = discord.Color.blurple()
embederrorcolor = discord.Color.red()
name = 'A1-DEV'
token = "MTM"
client_id = 1373300686346911885
log_channel = 1345766880308236389


### ENV CONFIG ###

directory = os.path.join(os.path.dirname(__file__), "commands")
edirectory = os.path.join(os.path.dirname(__file__), "core/events")
tdirectory = os.path.join(os.path.dirname(__file__), "core/loops")
base_dir = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
   
cdirectory = os.path.join(base_dir, "cache")

folder_blacklist = [
    "views",
    "functions",

]

file_blacklist = [
    'registry.py',
    '__init__.py'
]

### STARTUP SETTINGS ###

maintainance = False
INFO_COLOR = "blue"
ERROR_COLOR = "red"
DEBUG_COLOR = "green"
WARNING_COLOR = "peach"
FATAL_COLOR = "purple"

# EMOJIS

no = "<:no:1296811045444255755>"
error = "<:no:1296811045444255755>"
tick = "<:tick:1296811053119705118>"
yes = "<:tick:1296811053119705118>"
right = "<:right:1296811051488378930>"
left = "<:left:1296811043531784323>"
reply = "<:reply:1296811047419904091>"
replycont = "<:replycont:1296811049323860020>"
chat = "<:chat:1328091510784393356>"


# STATUSES

statuses = [
    {"text": "CPU: (c)% 💿", "type": "idle", "activity": "watching", "url": ""},
    {"text": "RAM: (r)% 💾", "type": "dnd", "activity": "watching", "url": ""},
]

