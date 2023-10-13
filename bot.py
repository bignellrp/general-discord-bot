import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('discord.http').setLevel(logging.WARNING)

# Load environment variables from .env
load_dotenv()  

# Set up the bot
intents = discord.Intents.default()
intents.members = True
command_prefix = os.getenv("COMMAND_PREFIX")
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Load extensions
bot.load_extension("cogs.login")
bot.load_extension("cogs.welcome")
bot.load_extension("cogs.commands")
bot.load_extension("cogs.cron")

# Run the bot
bot.run(TOKEN)