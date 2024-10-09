from discord.ext import commands
from utils import is_mod, handle_api_request
import logging

# didn't use discord apparently so i didn't import it.
logger = logging.getLogger(__name__)


# Setup function for the cog, necessary for every cog.
async def setup(bot):
    await bot.add_cog(Robocraft(bot))


# Scary looking but it's actually really simple.
# https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
class Robocraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # This is what tells Discord.py about your commands.
    # Every Command requires one of these decorators.
    # all parameters optional, name defaults to function name
    @commands.hybrid_command(
        name="start_server",
        description="Starts the game server",
        aliases=["start", "boot", "bootup"],
    )
    # @mod_only() for commands.command will do the same as the whole if not is_mod block.
    # Unfortunately doesn't work for slash commands or hybrid commands.

    async def start_server(self, ctx):
        # every command needs self and ctx (Context)
        # use ctx.send() to send a message
        # ctx.author for author (Member/User), ctx.guild for guild (Guild)
        # ctx.message for the command message (ctx.message.content for text of command ;) )

        # Check if the user is a mod
        if not is_mod(ctx.author):
            logger.warning(
                f"{ctx.author} tried to start the server without permission."
            )
            await ctx.send("You do not have permission to use this command.")
            return

        # Handle the API request
        result, message = handle_api_request("start_server")
        if result:
            logger.info(f"Server started by {ctx.author}.")
            await ctx.send("Server started successfully!")
        else:
            await ctx.send(f"Failed to start server: {message}")

    @commands.hybrid_command(
        name="stop_server",
        description="Stops the game server",
        aliases=["stop", "shutdown"],
    )
    async def stop_server(self, ctx):
        # Check if the user is a mod
        if not is_mod(ctx.author):
            logger.warning(f"{ctx.author} tried to stop the server without permission.")
            await ctx.send("You do not have permission to use this command.")
            return

        # Handle the API request
        result, message = handle_api_request("stop_server")
        if result:
            logger.info(f"Server stopped by {ctx.author}.")
            await ctx.send("Server stopped successfully!")
        else:
            await ctx.send(f"Failed to stop server: {message}")

    @commands.hybrid_command(
        name="change_map",
        description="Changes the game map",
        aliases=["map", "new_map"],
    )
    async def change_map(self, ctx, *, map_name: str):
        # takes a str, oooo
        # , *, means it greedily captures the rest of the string
        # str could also be int, discord.User, discord.Member, or really anything you want.
        # https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html#parameters
        # entire API docsis sacred god bless danny

        # Check if the user is a mod
        if not is_mod(ctx.author):
            logger.warning(f"{ctx.author} tried to change the map without permission.")
            await ctx.send("You do not have permission to use this command.")
            return

        # Handle the API request with the map name
        # You can put whatever else you need here, mapping to whatever else the user puts in
        # For here, it's just a basic dict with key map and value whatever the hell the user sends

        # Ideally, this should contain (or grab) a list of maps from the API in a way the backend understands
        # But i don't know how you have that set up.

        # To make it random,
        # from random import choice
        # map_name = choice(maps)
        # or whatever

        data = {"map": map_name}

        result, message = handle_api_request("change_map", data)
        if result:
            logger.info(f"Map changed to {map_name} by {ctx.author}.")
            await ctx.send(f"Map changed to {map_name}!")
        else:
            await ctx.send(f"Failed to change map: {message}")
