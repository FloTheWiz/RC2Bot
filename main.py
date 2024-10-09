import logging
from bot import RoboBot
from utils import load_config

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    # Load configuration
    config = load_config()

    # Get bot token and prefix from the config
    token = config.get("token")  # .get() returns None if the key is not found
    prefix = config.get("prefix", "!")

    if not token:
        logger.error("Bot token not found in config.yaml")
        return

    # Create the bot instance
    bot = RoboBot(command_prefix=prefix, config=config)

    # Run the bot
    bot.run(token)


if __name__ == "__main__":  # always do this lol
    main()
