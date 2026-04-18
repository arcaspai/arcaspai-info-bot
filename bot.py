import discord
import tokenbox
from typing import Literal

# values
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

TOKEN = tokenbox.token

# start
@client.event
async def on_ready():
    await tree.sync()
    print("running now")


# running bot
client.run(TOKEN)
