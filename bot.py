import discord
from discord.ext import commands
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Greedily Grabs all Intents.
# Not the most secure, but the most bug free lol
intents = discord.Intents(
    voice_states=True,
    messages=True,
    reactions=True,
    message_content=True,
    guilds=True,
    members=True,
)


# Pretty Simple setup for Bot.
# https://github.com/Rapptz/discord.py/tree/master/examples
class RoboBot(commands.Bot):
    def __init__(self, command_prefix, config, **options):
        self.config = config
        self.uptime = datetime.utcnow()  # used for info :)
        self.src = config.get("github_url")
        # Set up the command prefix and intents from commands.Bot
        super().__init__(command_prefix=command_prefix, intents=intents, **options)

    async def setup_hook(self):  # Runs automatically
        # Load cogs from config. (/cogs/{cog})
        # https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
        for cog in self.config.get("cogs", []):
            try:
                await self.load_extension("cogs." + cog)  # f-strings better but.
                logger.info(f"Successfully loaded cog: {cog}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}: {e}")

    async def on_ready(self):  # also runs automatically, when bot is on discord
        logger.info(f"Logged in as {self.user.name} (ID: {self.user.id})")

        # Create bot invite link
        if self.user:
            invite_url = discord.utils.oauth_url(
                self.user.id, permissions=discord.Permissions(administrator=True)
            )
            logger.info(f"Invite the bot to your server: {invite_url}")

        logger.info("Bot is ready and operational.")
