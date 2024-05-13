import discord
import os

import mihomo.errors
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


async def character_embed(char):
    embed = discord.Embed(title=f"{char.name}",
                          description=f"Level: {char.level} | Rarity: {await rarity(char.rarity)}  ",
                          color=discord.Color.blurple())
    embed.set_image(url=f"{char.preview}")
    return embed


async def rarity(stars: int):
    i: int = 0
    fin: str = ""
    while i < stars:
        i += 1
        fin += "⭐"
    return fin


async def get_user(uid):
    data: StarrailInfoParsed = await client.fetch_user(uid, replace_icon_name_with_url=True)
    return data


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
        await interaction.response.edit_message(embed=await character_embed(self.data.characters[self.idx+1]))

    @discord.ui.button(label=f"3", custom_id="char2", style=discord.ButtonStyle.secondary)
    async def button_3_callback(self, button, interaction):
        await interaction.response.edit_message(embed=await character_embed(self.data.characters[self.idx+2]))

    @discord.ui.button(label=f"4", custom_id="char3", style=discord.ButtonStyle.secondary)
    async def button_4_callback(self, button, interaction):
        await interaction.response.edit_message(embed=await character_embed(self.data.characters[self.idx+3]))

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


@bot.slash_command(description="Displays user Profile")  # Create a slash command
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


# @sg.command(description="Displays all available commands.", guild_ids=guild)
# async def help(ctx):
#     await prydwen.pryd_help(ctx)
# 
# 
# @sg.command(description="Sends a link to Prydwen.", guild_ids=guild)
# async def prydwen(ctx):
#     await prydwen.pryd_prydwen(ctx)
# 
# 
# @sg.command(description="Sends a link to the specific characters profile, on Prydwen.", guild_ids=guild)
# async def character(ctx, ch: str):
#     await prydwen.pryd_character_profile(ctx, ch)
#     

bot.run(config)
