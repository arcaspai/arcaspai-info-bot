import discord
import tokenbox
from discord import app_commands
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

# send introduction
@tree.command(name = "introduction", description = "About Arcaspai Project")
async def embed(interaction) :
    embed = discord.Embed(title="About Arcaspai", colour=discord.Colour.from_rgb(144, 136, 255))
    embed.set_author(name="Arcaspaio", url="https://arcaspai.github.io", icon_url="https://media.discordapp.net/attachments/1491315989428572171/1493217429692747826/arcaspaibanner08.png")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1491315989428572171/1493217429692747826/arcaspaibanner08.png")
    embed.add_field(name="Archived Space", value="A journey from fantasy to ideality.", inline=False)
    embed.add_field(name="Project Start", value="2021-08-29", inline=True)
    embed.add_field(name="Project Reboot", value="2026-01-27", inline=True)
    embed.add_field(name="Website", value="https://arcaspai.github.io", inline=False)
    embed.set_footer(text="Arcaspai Project © 2021-2026 Redder")

    await interaction.response.send_message(embed=embed)

# send websites link
@tree.command(name="website", description="send official web pages link of Arcaspai Project")
@app_commands.choices(site=[
    app_commands.Choice(name="website", value="https://arcaspai.github.io/"),
    app_commands.Choice(name="blog", value="https://arcaspai.blogspot.com/"),
    app_commands.Choice(name="lorebook", value="https://arcaspai.notion.site/ARCASPAI-Universe-Guidebook-2978e3302cae817fa3c9eb88d7c00ce8"),
    app_commands.Choice(name="youtube", value="https://www.youtube.com/@arcaspai"),
    app_commands.Choice(name="itch.io", value="https://discord.com/channels/1484901254583812269/1490580195286061146/1490626055952793682"),
    app_commands.Choice(name="discord", value="https://discord.gg/pvUKPcXq")
])
async def food_choice(interaction: discord.Interaction, site: app_commands.Choice[str]):
    await interaction.response.send_message(f"{site.value}")

# running bot
client.run(TOKEN)