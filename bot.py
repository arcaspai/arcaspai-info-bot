import discord
import tokenbox
from discord import app_commands
# from typing import Literal

# values
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

embed_footer = "Arcaspai Project © 2021-2026 Redder"

TOKEN = tokenbox.token

# start
@client.event
async def on_ready():
    await tree.sync()
    print("running now")

# send introduction
@tree.command(name = "introduction", description = "about Arcaspai Project")
async def introduct_embed(interaction) :
    embed = discord.Embed(title="About Arcaspai", colour=discord.Colour.from_rgb(144, 136, 255))
    embed.set_author(name="Arcaspaio", url="https://arcaspai.github.io", icon_url="https://media.discordapp.net/attachments/1491315989428572171/1493217429692747826/arcaspaibanner08.png")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1491315989428572171/1493217429692747826/arcaspaibanner08.png")
    embed.add_field(name="Archived Space", value="A journey from fantasy to ideality.", inline=False)
    embed.add_field(name="Project Start", value="2021-08-29", inline=True)
    embed.add_field(name="Project Reboot", value="2026-01-27", inline=True)
    embed.add_field(name="Website", value="https://arcaspai.github.io", inline=False)
    embed.set_footer(text=embed_footer)

    await interaction.response.send_message(embed=embed)

# send websites link
@tree.command(name="website", description="send official web pages link of Arcaspai Project")
@app_commands.choices(site=[
    app_commands.Choice(name="website", value="https://arcaspai.github.io/"),
    #app_commands.Choice(name="blog", value="https://arcaspai.blogspot.com/"),
    #app_commands.Choice(name="universe", value="https://arcaspai.notion.site/ARCASPAI-Universe-Guidebook-2978e3302cae817fa3c9eb88d7c00ce8"),
    app_commands.Choice(name="youtube", value="https://www.youtube.com/@arcaspai"),
    app_commands.Choice(name="itch.io", value="https://discord.com/channels/1484901254583812269/1490580195286061146/1490626055952793682"),
    app_commands.Choice(name="discord", value="https://discord.gg/pvUKPcXq")
])
async def link_choice(interaction: discord.Interaction, site: app_commands.Choice[str]):
    await interaction.response.send_message(f"{site.value}")

# send characters info
characters_info = app_commands.Group(name="character", description="embed characters infomations (Input only family names please.)")

@characters_info.command(name="image", description="embed character images(Input only family names please.)")
@app_commands.choices(imagetype=[
    app_commands.Choice(name="portrait", value="portrait"),
    app_commands.Choice(name="icon", value="icon")
])
async def character_images(interaction: discord.Interaction, character: str, imagetype: app_commands.Choice[str]) :
    char_name = character.lower().strip()
    embed = discord.Embed(title=f"{character}'s {imagetype.value}", colour=discord.Colour.from_rgb(144, 136, 255))
    embed.set_author(name="Arcaspaio", url="https://arcaspai.github.io", icon_url="https://media.discordapp.net/attachments/1491315989428572171/1493217429692747826/arcaspaibanner08.png")
    embed.set_image(url=f"https://arcaspai.github.io/universe/images/{imagetype.value}s/{char_name}_{imagetype.value}.png")
    embed.set_footer(text=embed_footer)

    await interaction.response.send_message(embed=embed)

@characters_info.command(name = "profile", description="embed character profiles (Input only family names please.)")
async def character_profiles(interaction: discord.Interaction, character: str):
    await interaction.response.send_message(f"Hello, {character}!")

# making groups
tree.add_command(characters_info)

# running bot
client.run(TOKEN)