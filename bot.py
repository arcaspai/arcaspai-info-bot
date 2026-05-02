import discord
import tokenbox
import json
from discord import app_commands
# from typing import Literal

# values
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

embed_footer = "Arcaspai Project © 2021-2026 Redder"
bot_icon = "https://media.discordapp.net/attachments/1491315989428572171/1493217429692747826/arcaspaibanner08.png"

TOKEN = tokenbox.token

# import JSON file
with open('data/charlist.json', 'r', encoding='utf-8') as f:
    char_list = json.load(f)

# start
@client.event
async def on_ready():
    await tree.sync()
    print("running now")

# send help
@tree.command(name = "help", description = "about Arcaspai.io bot")
async def introduct_embed(interaction) :
    embed = discord.Embed(title="About Arcaspai.io", colour=discord.Colour.from_rgb(144, 136, 255))
    embed.set_author(name="Arcaspaio", url="https://arcaspai.github.io", icon_url=bot_icon)
    embed.add_field(name="`/help`", value="send help", inline=False)
    embed.add_field(name="`/introduction`", value="send help", inline=False)
    embed.add_field(name="`/website`", value="send help", inline=False)
    embed.add_field(name="`/character`", value="send help", inline=False)
    embed.add_field(name="`image`", value="2021-08-29", inline=True)
    embed.add_field(name="`profile`", value="2026-01-27", inline=True)
    embed.add_field(name="`/help`", value="send help", inline=False)
    embed.add_field(name="Website", value="https://arcaspai.github.io", inline=False)
    embed.set_footer(text=embed_footer)

    await interaction.response.send_message(embed=embed)

# send introduction
@tree.command(name = "introduction", description = "about Arcaspai Project")
async def introduct_embed(interaction) :
    embed = discord.Embed(title="About Arcaspai", colour=discord.Colour.from_rgb(144, 136, 255))
    embed.set_author(name="Arcaspaio", url="https://arcaspai.github.io", icon_url=bot_icon)
    embed.set_thumbnail(url=bot_icon)
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
characters_info = app_commands.Group(name="character", description="embed characters infomations (write only forenames please.)")

@characters_info.command(name="image", description="embed character images (write only forenames please.)")
@app_commands.choices(imagetype=[
    app_commands.Choice(name="portrait", value="portrait"),
    app_commands.Choice(name="icon", value="icon")
])
async def character_images(interaction: discord.Interaction, character: str, imagetype: app_commands.Choice[str]) :
    char_name = character.lower().strip()
    char_info = char_list.get(char_name)
    if char_info:
        name_en = char_info["name"]
        
        embed = discord.Embed(title=f"{name_en}'s {imagetype.value}", colour=discord.Colour.from_rgb(144, 136, 255))
        embed.set_author(name="Arcaspaio", url="https://arcaspai.github.io", icon_url=bot_icon)
        embed.set_image(url=f"https://arcaspai.github.io/universe/assets/img/{imagetype.value}s/{char_name}_{imagetype.value}.png")
        embed.set_footer(text=embed_footer)

        await interaction.response.send_message(embed=embed, ephemeral=False)

    else:
        await interaction.response.send_message("Not founded. Please check that you entered the information correctly.", ephemeral=True)
    
@characters_info.command(name = "profile", description="embed character profiles (write only forenames please.)")
async def character_profiles(interaction: discord.Interaction, character: str):
    char_name = character.lower().strip()
    char_info = char_list.get(char_name)
    if char_info:
        name_ko = char_info["ireum"]
        name_en = char_info["name"]
        quote = char_info["quote"]
        description = char_info["description"]
        universe = char_info['universe']
        
        embed = discord.Embed(title=f"{name_en}'s profile", colour=discord.Colour.from_rgb(144, 136, 255))
        embed.set_author(name="Arcaspaio", url="https://arcaspai.github.io", icon_url=bot_icon)
        embed.set_thumbnail(url=f"https://arcaspai.github.io/universe/assets/img/icons/{char_name}_icon.png")
        embed.add_field(name="name(KO)", value=name_ko, inline=True)
        embed.add_field(name="name(EN)", value=name_en, inline=True)
        embed.add_field(name="quote", value=f'"{quote}"', inline=False)
        embed.add_field(name="descriptions", value=description, inline=False)
        embed.add_field(name="details", value=f"[arcaspai.github.io/universe/characters/{universe}/{char_name}](https://arcaspai.github.io/universe/characters/{universe}/{char_name})", inline=False)
        embed.set_footer(text=embed_footer)

        await interaction.response.send_message(embed=embed, ephemeral=False)
        
    else:
        await interaction.response.send_message("Not founded. Please check that you entered the information correctly.", ephemeral=True)



# making groups
tree.add_command(characters_info)

# running bot
client.run(TOKEN)