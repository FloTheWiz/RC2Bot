from discord.ext import commands
from utils import handle_api_request
import logging

from utils import about_me_embed

logger = logging.getLogger(__name__)


# Setup function for the cog
async def setup(bot):
    await bot.add_cog(Info(bot))


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="info_bot",
        description="Displays information about the bot.",
        aliases=["about", "bot_info"],
    )  # fun fact, commands can't start with cog_ or bot_
    async def info_bot(self, ctx):
        # see utils.py
        embed = about_me_embed(self.bot)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="server_status", description="Fetches the game server status"
    )
    async def server_status(self, ctx):
        result, message = handle_api_request("server_status")
        if result:
            status = result.get("status", "Unknown")
            await ctx.send(f"Server status: {status}")
        else:
            await ctx.send(f"Failed to retrieve server status: {message}")
