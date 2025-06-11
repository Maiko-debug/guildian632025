import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Load from .env
TOKEN = os.getenv('DISCORD_TOKEN')
DEV_GUILD_ID = int(os.getenv("DEV_GUILD_ID"))
OWNER_ID = int(os.getenv("OWNER_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

def is_dev_server(ctx):
    return ctx.guild and (ctx.guild.id == DEV_GUILD_ID or ctx.author.id == OWNER_ID)

@bot.check
async def global_check(ctx):
    print(f"Check run: {ctx.author} in guild {ctx.guild.id if ctx.guild else 'DM'}")
    return ctx.guild and (ctx.guild.id == DEV_GUILD_ID or ctx.author.id == OWNER_ID)

# Load cogs
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for ext in ["cogs.ping", "cogs.error_logger"]:
        try:
            await bot.load_extension(ext)
            print(f"Loaded {ext}")
        except Exception as e:
            print(f"Failed to load {ext}: {e}")

bot.run(TOKEN)
