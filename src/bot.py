import discord
import os

import requests
import mihomo.errors
from collections import defaultdict
from mihomo import Language, MihomoAPI
from mihomo.models import StarrailInfoParsed
from dotenv import load_dotenv

client = MihomoAPI(language=Language.EN)

load_dotenv()
config = os.getenv("DISCORD_TOKEN")
guild = os.getenv("GUILD_ID")

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        guild_count = guild_count + 1
    print(f"Bot is in {guild_count} guild/s.")
    print(f"Guilds: {guild.name} | ID: {guild.id}")


#HONKAI
async def get_user(uid):
    data: StarrailInfoParsed = await client.fetch_user(uid, replace_icon_name_with_url=True)
    return data


async def profile_embed(data):
    embed = discord.Embed(title=f"{data.player.name}", description=f"Signature: {data.player.signature}",
                          color=discord.Color.blurple())
    embed.add_field(name="Level", value=f"{data.player.level}", inline=True)
    embed.add_field(name="World Level", value=f"{data.player.world_level}", inline=True)
    embed.add_field(name="", value="", inline=True)
    embed.add_field(name="Achievements", value=f"{data.player.achievements}", inline=True)
    embed.add_field(name="Characters Collected", value=f"{data.player.characters}", inline=True)
    embed.add_field(name="Lightcones Collected", value=f"{data.player.light_cones}", inline=True)
    embed.set_thumbnail(url=f"{data.player.avatar.icon}")
    embed.set_footer(text="Stargale")
    return embed


def get_element_color(element):
    element_colors = defaultdict(lambda: discord.Color.blurple(),
                                 [("Physical", discord.Color.light_gray()),
                                  ("Fire", discord.Color.red()),
                                  ("Ice", discord.Color.blue()),
                                  ("Lightning", discord.Color.nitro_pink()),
                                  ("Wind", discord.Color.teal()),
                                  ("Quantum", discord.Color.dark_purple()),
                                  ("Imaginary", discord.Color.gold())
                                  ])
    return element_colors[element]


def clean_data(char):
    attributes = char.attributes
    additions = char.additions
    match = {}
    for i in attributes:
        for j in additions:
            if i.name == j.name:
                match[j.name] = (i, j)

    li = {}
    for k, v in match.items():
        if not v[1].is_percent:
            res = "{:.0f}".format(v[0].value + v[1].value)
        else:
            res = "{:.1f}".format((v[0].value + v[1].value) * 100) + "%"
        li.update({v[0].name: res})

    for i in additions:
        if i.name not in li:
            if not i.is_percent:
                res = "{:.0f}".format(i.value)
            else:
                res = "{:.1f}".format(i.value * 100) + "%"
            li.update({i.name: res})
    return li


async def character_embed(char):
    embed = discord.Embed(title=f"{char.name}",
                          description=f"Lv. {char.level} | Rarity: {"⭐" * char.rarity}  | E: {char.eidolon}",
                          color=get_element_color(char.element.name))
    embed.add_field(name=f"Lightcone: {char.light_cone.name}", value=f"Lv. {char.light_cone.level} | Rarity: {"⭐" * char.light_cone.rarity} | S: {char.light_cone.superimpose}", inline=False)
    # embed.add_field(name="Stats: ", value="", inline=False)

    for k, v in clean_data(char).items():
        embed.add_field(name=f"{k}:", value=f"{v}", inline=True)
    embed.set_image(url=f"{char.preview}")

    return embed
    

class CharButtons(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data
        self.idx = 0
        for i in self.children:
            if f"char{self.idx}" in i.custom_id:
                i.label = f"{data.characters[self.idx].name}"
                self.idx += 1
        self.idx = 0

    @discord.ui.button(label="Profile", custom_id="profile_btn", style=discord.ButtonStyle.primary)
    async def profile_button_callback(self, button, interaction):
        await interaction.response.edit_message(embed=await profile_embed(self.data))

    @discord.ui.button(label=f"1", custom_id="char0", style=discord.ButtonStyle.secondary)
    async def button_1_callback(self, button, interaction):
        await interaction.response.edit_message(embed=await character_embed(self.data.characters[self.idx]))

    @discord.ui.button(label=f"2", custom_id="char1", style=discord.ButtonStyle.secondary)
    async def button_2_callback(self, button, interaction):
        await interaction.response.edit_message(embed=await character_embed(self.data.characters[self.idx + 1]))

    @discord.ui.button(label=f"3", custom_id="char2", style=discord.ButtonStyle.secondary)
    async def button_3_callback(self, button, interaction):
        await interaction.response.edit_message(embed=await character_embed(self.data.characters[self.idx + 2]))

    @discord.ui.button(label=f"4", custom_id="char3", style=discord.ButtonStyle.secondary)
    async def button_4_callback(self, button, interaction):
        await interaction.response.edit_message(embed=await character_embed(self.data.characters[self.idx + 3]))

    @discord.ui.button(label=">", custom_id="next_btn", style=discord.ButtonStyle.grey)
    async def display_next(self, button, interaction):
        if button.label == ">":
            button.label = "<"
            self.idx = 4
            i = 0
            char_id = 4
            for x in self.children:
                if f"char{i}" in x.custom_id:
                    x.label = f"{self.data.characters[char_id].name}"
                    i += 1
                    char_id += 1
        else:
            button.label = ">"
            self.idx = 0
            i = 0
            for x in self.children:
                if f"char{i}" in x.custom_id:
                    x.label = f"{self.data.characters[i].name}"
                    i += 1

        await interaction.response.edit_message(view=self)


@bot.slash_command(description="Displays user Profile")
async def profile(ctx, uid: int):
    await ctx.defer(ephemeral=True)
    try:
        user = await get_user(uid)
        embed = await profile_embed(user)
        await ctx.respond(embed=embed, view=CharButtons(user))

    except mihomo.errors.InvalidParams:
        await ctx.respond("Womp womp. Invalid UID. Please try again, with a different UID.")
        return None
    except mihomo.errors.UserNotFound:
        await ctx.respond(
            "Womp womp. User not found. "
            "\nThis could be because the wrapper is down or it took too long. Did the game just update recently? "
            "\nPlease try again later.")
        return None


# PRYDWEN
@bot.slash_command(description="Displays all available commands.")
async def help_sg(ctx):
    await ctx.defer(ephemeral=True)
    embed = discord.Embed(title="Help : list of commands available", color=discord.Color.brand_green())
    embed.add_field(name="/help_sg", value="Shows this message", inline=False)
    embed.add_field(name="/prydwen", value="Link to Prydwen", inline=False)
    embed.add_field(name="/character [character name]", value="Link to specific character, on Prydwen.", inline=False)
    await ctx.respond(embed=embed)


@bot.slash_command(description="Sends a link to Prydwen.")
async def prydwen(ctx):
    await ctx.defer(ephemeral=True)
    embed = discord.Embed(title="Prydwen | All characters.", url="https://www.prydwen.gg/star-rail/characters",
                          color=discord.Color.blue())
    await ctx.respond(embed=embed)


@bot.slash_command(description="Sends a link to the specific characters profile, on Prydwen.")
async def character(ctx, ch: str):
    await ctx.defer(ephemeral=True)
    character_name = ch.lower()
    titled_name = ch.title()
    response = requests.get("https://www.prydwen.gg/star-rail/characters/" + character_name)

    if response.status_code == 404:
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name="! Invalid Character name !")
        embed.add_field(name="If the character has a space between two names/words, please separate with a line",
                        value="(ex: black-swan)", inline=False)
    else:
        embed = discord.Embed(title="Prydwen | " + titled_name,
                              url="https://www.prydwen.gg/star-rail/characters/" + character_name,
                              color=discord.Color.blue())

    await ctx.respond(embed=embed)


bot.run(config)
