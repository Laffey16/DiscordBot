import os
import random

import discord
from discord.ext import bridge, commands, tasks
from dotenv import load_dotenv

load_dotenv()
BOT_API_KEY = os.environ["TOKEN"]

description = """
Fun bot with fun stuff.
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = bridge.Bot(
    command_prefix="!",
    description=description,
    intents=intents,
    debug_guilds=[436906751040946176],
)

status = ["Working well!"]


@client.event
async def on_ready():
    print("Bot is now online!!")
    change_status.start()


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        pass
    elif isinstance(error, commands.DisabledCommand):
        print(error)
    elif isinstance(error, commands.CommandNotFound):
        print(f"Command {error}")


@tasks.loop(hours=24)
async def change_status():
    randomstatus = random.choice(status)
    await client.change_presence(activity=discord.Game((randomstatus)))
    print(f"Changed status to {randomstatus}")


for filename in os.listdir("./cogs"):
    if filename.endswith("py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(BOT_API_KEY)
