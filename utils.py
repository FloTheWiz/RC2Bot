import yaml
import logging
import requests
import discord
import datetime
import psutil
import humanfriendly

# imagine a world where devs imported exactly what they needed
# but it's just not possible /s

logger = logging.getLogger(__name__)


# Basic Loading with some error handling
def load_config():
    try:
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
            logger.info("Configuration file loaded successfully.")
            return config
    except FileNotFoundError:
        logger.error("Config file not found. Please ensure 'config.yaml' exists.")
        return {}
    except yaml.YAMLError as exc:
        logger.error(f"Error parsing YAML config: {exc}")
        return {}


# Unused Saving
def save_config(config):
    try:
        with open("config.yaml", "w") as file:
            yaml.safe_dump(config, file)
            logger.info("Configuration file saved successfully.")
    except Exception as e:
        logger.error(f"Error saving config: {e}")


# is_mod, takes a Member, returns a bool
# not the best as DM'ing the bot won't produce a list of roles and thus won't count mods.
# i just don't want to rewrite the yaml
def is_mod(member):
    config = load_config()
    mod_ids = config.get("mods", [])

    if str(member.id) in mod_ids:
        return True

    for role in member.roles:
        if str(role.id) in mod_ids:
            return True

    return False


# Unused Decorator for commands.
# You'll come to learn there's a good amount of stuff that's just easier with commands rather than slash commands.
# See robocraft.py for some examples
def mod_only():
    def wrapper(func):
        async def wrapped(self, ctx, *args, **kwargs):
            if not is_mod(ctx.author):
                logger.warning(
                    f"{ctx.author} tried to access {ctx.command} without permission."
                )
                await ctx.send("You do not have permission to use this command.")
                return
            return await func(self, ctx, *args, **kwargs)

        return wrapped

    return wrapper


# Gross function, but it works.
def handle_api_request(route_key, data=None):
    # route_key is your YAML key
    # Data defaults to None so we don't have to set it

    config = load_config()

    # If you wanted to set up multiple API URLS, you could use them like routes (a list), or just copy how api_url is setup.
    api_url = config.get("api_url")
    routes = config.get("routes", {})

    if not api_url:  # you fucked up
        logger.error("API URL is not configured.")
        return None, "API URL is not configured."

    if route_key not in routes:  # you also fucked up
        logger.warning(f"Invalid route key: {route_key}")
        return None, "Invalid API route key."

    route = routes[route_key]
    url = f"{api_url}{route}"

    try:  # Very prone to errors. Server shite.
        if data:
            response = requests.post(url, json=data)
        else:
            response = requests.post(url)

        if response.status_code == 200:
            logger.info(f"API request to {url} succeeded.")
            return response.json(), "Success!"
        else:
            return None, f"Error {response.status_code}: {response.text}"

    except Exception as e:
        logger.error(f"Request failed: {e}")
        return None, f"Request failed: {str(e)}"


# Baller about me embed, don't worry too much about this
# Good insight into how embeds work though.
def about_me_embed(bot):
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/")
    disk = {
        "used_gb": round(disk.used / (1024.0**3), 2),
        "available_gb": round(disk.free / (1024.0**3), 2),
        "total_gb": round(disk.total / (1024.0**3), 2),
    }
    uptime = datetime.utcnow() - bot.uptime
    if bot.src:  # remember that?
        description = f"This bot is [**Open Source!**](<{bot.src}>)"
    else:
        description = "A Discord Bot Written in Python!"  # idk

    # make the embed
    embed = discord.Embed(
        title=f"About: {bot.user.name}",
        description=description,
        color=discord.Color.random(),
    )
    # add fields
    embed.add_field(name="CPU: ", value=f"{cpu}% of {psutil.cpu_count()} cores")
    embed.add_field(
        name="Memory: ",
        value=f"{memory}% of {round(psutil.virtual_memory().total / (1024.0 ** 3), 2)} GB",
    )
    embed.add_field(
        name="Disk Usage: ", value=f"{disk['used_gb']} GB used of {disk['total_gb']} GB"
    )
    embed.add_field(name="Uptime: ", value=f"{humanfriendly.format_timespan(uptime)}")

    # add avatar and footer
    embed.set_image(url=bot.user.display_avatar.url)
    embed.set_footer(text="Made with :3 by Flo ❤️", icon_url=bot.user.display_avatar.url)
    return embed
