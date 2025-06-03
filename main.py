import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Load from .env
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.load_extension("cogs.ping")

bot.run(TOKEN)
