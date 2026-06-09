import discord
import tokenbox
import json
from discord import app_commands

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


# Command Localization System
class CommandTranslator(app_commands.Translator):
    async def translate(self, string: app_commands.locale_str, locale: discord.Locale, context: app_commands.TranslationContext) -> str | None:
        translations = {
            discord.Locale.korean: {
                "introduction": "소개",
                "about Arcaspai Project": "아르카스페이 프로젝트에 대한 소개를 확인합니다.",
                "website": "웹사이트",
                "send official web pages link of Arcaspai Project": "아르카스페이 프로젝트의 공식 웹페이지 링크를 전송합니다.",
                "character": "캐릭터",
                "embed characters infomations (write only forenames please.)": "캐릭터 정보를 임베드로 확인합니다. (성 없이 이름만 입력해주세요.)",
                "image": "이미지",
                "embed character images (write only forenames please.)": "캐릭터 이미지를 임베드로 확인합니다. (성 없이 이름만 입력해주세요.)",
                "profile": "프로필",
                "embed character profiles (write only forenames please.)": "캐릭터 프로필을 임베드로 확인합니다. (성 없이 이름만 입력해주세요.)",
                "blog": "블로그",
                "universe": "세계관",
                "youtube": "유튜브",
                "discord": "디스코드",
                "soundtracks": "사운드트랙",
                "site": "사이트",
                "imagetype":"이미지유형"
            }
        }
        
        if locale == discord.Locale.korean:
            if string.message in translations[discord.Locale.korean]:
                return translations[discord.Locale.korean][string.message]
        
        return string.message


def find_character(search_input: str) -> tuple[str, dict] | tuple[None, None]:
    clean_input = search_input.lower().strip()
    
    if clean_input in char_list:
        return clean_input, char_list[clean_input]
        
    for char_key, char_info in char_list.items():
        if char_info.get("nameKo") == search_input.strip():
            return char_key, char_info
            
    return None, None

# start
@client.event
async def on_ready():
    await tree.set_translator(CommandTranslator())
    await tree.sync()
    print("running now")

# send introduction
@tree.command(name="introduction", description="about Arcaspai Project")
async def introduct_embed(interaction: discord.Interaction):
    lang = "ko" if interaction.locale == discord.Locale.korean else "en"

    embed = discord.Embed(title="About Arcaspai" if lang == "en" else "Arcaspai 소개", colour=discord.Colour.from_rgb(144, 136, 255))
    embed.set_author(name="Arcaspaio", url="https://arcaspai.github.io", icon_url=bot_icon)
    embed.set_thumbnail(url=bot_icon)
    embed.add_field(name="Archived Space", value="A journey from fantasy to ideality." if lang == "en" else "공상에서 이상으로의 여정.", inline=False)
    embed.add_field(name="Project Start" if lang == "en" else "프로젝트 시작", value="2021-08-29", inline=True)
    embed.add_field(name="Project Reboot" if lang == "en" else "프로젝트 리부트", value="2026-01-27", inline=True)
    embed.add_field(name="Website" if lang == "en" else "웹사이트", value="https://arcaspai.github.io", inline=False)
    embed.set_footer(text=embed_footer)

    await interaction.response.send_message(embed=embed)

# send websites link
@tree.command(name="website", description="send official web pages link of Arcaspai Project")
@app_commands.describe(site=app_commands.locale_str("site"))
@app_commands.choices(site=[
    app_commands.Choice(name="website", value="https://arcaspai.github.io/"),
    app_commands.Choice(name="blog", value="https://arcaspai.blogspot.com/"),
    app_commands.Choice(name="universe", value="https://arcaspai.github.io/universe"),
    app_commands.Choice(name="youtube", value="https://www.youtube.com/@arcaspai"),
    app_commands.Choice(name="itch.io", value="https://itch.io/arcaspai"),
    app_commands.Choice(name="discord", value="https://discord.gg/pvUKPcXq"),
    app_commands.Choice(name="soundtracks", value="https://bandlab.com/band/arcaspai")
])
async def link_choice(interaction: discord.Interaction, site: app_commands.Choice[str]):
    await interaction.response.send_message(f"{site.value}")

# send characters info
characters_info = app_commands.Group(name="character", description="embed characters infomations (write only forenames please.)")

@characters_info.command(name="image", description="embed character images (write only forenames please.)")
@app_commands.describe(imagetype=app_commands.locale_str("imagetype"))
@app_commands.choices(imagetype=[
    app_commands.Choice(name="portrait", value="portrait"),
    app_commands.Choice(name="icon", value="icon")
])
async def character_images(interaction: discord.Interaction, character: str, imagetype: app_commands.Choice[str]):
    char_key, char_info = find_character(character)
    lang = "ko" if interaction.locale == discord.Locale.korean else "en"
    
    if char_info:
        name_ko = char_info["nameKo"]
        name_en = char_info["nameEn"]
        
        display_type = imagetype.name
        if lang == "ko":
            type_translations = {
                "portrait": "전신 일러스트",
                "icon": "아이콘"
            }
            
            display_type = type_translations.get(imagetype.name, imagetype.name)
        
        embed = discord.Embed(title=f"{name_ko}의 {display_type}" if lang == "ko" else f"{name_en}'s {display_type}", colour=discord.Colour.from_rgb(144, 136, 255))
        embed.set_author(name="Arcaspaio", url="https://arcaspai.github.io", icon_url=bot_icon)
        embed.set_image(url=f"https://arcaspai.github.io/universe/assets/img/{imagetype.value}s/{char_key}_{imagetype.value}.png")
        embed.set_footer(text=embed_footer)

        await interaction.response.send_message(embed=embed, ephemeral=False)
    else:
        fail_msg = "캐릭터를 찾을 수 없습니다. 이름을 정확히 입력했는지 확인해주세요." if lang == "ko" else "Not founded. Please check that you entered the information correctly."
        await interaction.response.send_message(fail_msg, ephemeral=True)
    
@characters_info.command(name="profile", description="embed character profiles (write only forenames please.)")
async def character_profiles(interaction: discord.Interaction, character: str):
    char_name = character.lower().strip()
    char_key, char_info = find_character(character)
    lang = "ko" if interaction.locale == discord.Locale.korean else "en"
    
    if char_info:
        name_ko = char_info["nameKo"]
        name_en = char_info["nameEn"]
        universe = char_info['universe']
        
        quote = char_info["quote"].get(lang, char_info["quote"]["en"])
        description = char_info["description"].get(lang, char_info["description"]["en"])
        
        title = f"{name_ko}의 프로필" if lang == "ko" else f"{name_en}'s profile"
        
        embed = discord.Embed(title=title, colour=discord.Colour.from_rgb(144, 136, 255))
        embed.set_author(name="Arcaspaio", url="https://arcaspai.github.io", icon_url=bot_icon)
        embed.set_thumbnail(url=f"https://arcaspai.github.io/universe/assets/img/icons/{char_key}_icon.png")
        
        embed.add_field(name="name(KO)" if lang == "en" else "이름(한)", value=name_ko, inline=True)
        embed.add_field(name="name(EN)" if lang == "en" else "이름(영)", value=name_en, inline=True)
        
        embed.add_field(name="Quote" if lang == "en" else "한마디", value=f'"{quote}"', inline=False)
        embed.add_field(name="descriptions" if lang == "en" else "설명", value=description, inline=False)
        
        details_label = "details" if lang == "en" else "상세 정보"
        embed.add_field(name=details_label, value=f"[arcaspai.github.io/universe/characters/{universe}/{char_key}](https://arcaspai.github.io/universe/characters/{universe}/{char_key})", inline=False)
        embed.set_footer(text=embed_footer)

        await interaction.response.send_message(embed=embed, ephemeral=False)
    else:
        fail_msg = "캐릭터를 찾을 수 없습니다. 이름을 정확히 입력했는지 확인해주세요." if lang == "ko" else "Not found. Please check that you entered the information correctly."
        await interaction.response.send_message(fail_msg, ephemeral=True)

# making groups
tree.add_command(characters_info)

# running bot
client.run(TOKEN)