import discord
from discord.ext import commands
import os
import traceback

class ErrorLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = int(os.getenv("LOG_CHANNEL_ID"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("⚠️ You are not authorized to run this command here.")
            return

        # Log error to console
        print("Unhandled command error:")
        traceback.print_exception(type(error), error, error.__traceback__)

        # Build traceback string
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))

        # Send embed to log channel
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            embed = discord.Embed(
                title="❌ Command Error",
                description=f"```{str(error)}```",
                color=discord.Color.red()
            )
            embed.add_field(name="User", value=f"{ctx.author} (`{ctx.author.id}`)", inline=False)
            embed.add_field(name="Command", value=ctx.command, inline=False)
            embed.set_footer(text=f"In: #{ctx.channel} | Guild: {ctx.guild}")

            await channel.send(embed=embed)

            # Send traceback in code block, split if too long
            for chunk in split_text(tb, 1900):
                await channel.send(f"```py\n{chunk}\n```")

def split_text(text, limit):
    # Split large text into smaller chunks
    lines = text.splitlines()
    chunks = []
    chunk = ""
    for line in lines:
        if len(chunk) + len(line) + 1 > limit:
            chunks.append(chunk)
            chunk = ""
        chunk += line + "\n"
    if chunk:
        chunks.append(chunk)
    return chunks

async def setup(bot):
    await bot.add_cog(ErrorLogger(bot))
