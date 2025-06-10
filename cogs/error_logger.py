import discord
from discord.ext import commands

class ErrorLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You are not authorized to run this command here.")
        else:
            print(f"Unhandled error: {error}")

def setup(bot):
    bot.add_cog(ErrorLogger(bot))
