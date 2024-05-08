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
                          description=f"Level: {char.level} | Rarity: {rarity(char.rarity)}  ",
                          color=discord.Color.blurple())
    embed.set_image(url=f"{char.portrait}")
    return embed


async def rarity(stars: int):
    i: int = 0
    fin: str = ""
    while i < stars:
        i += 1
        fin += "⭐"
    return fin


class MyButton(discord.ui.View, StarrailInfoParsed):
    char_id: int = 0

    @discord.ui.button(label=f"{StarrailInfoParsed.player.name}", style=discord.ButtonStyle.primary,
                       emoji=f"{StarrailInfoParsed.player.avatar}")
    async def profile_button_callback(self, button, interaction):
        await interaction.response.edit_message(embed=profile_embed(self.StarrailInfoParsed))

    @discord.ui.button(label=f"{StarrailInfoParsed.characters[char_id].name}", style=discord.ButtonStyle.secondary,
                       emoji=f"{StarrailInfoParsed.characters[char_id].portrait}")
    async def button_one_callback(self, button, interaction):
        await interaction.response.edit_message(embed=character_embed(self.StarrailInfoParsed))

    # @discord.ui.button(label=f"{StarrailInfoParsed.characters[char_id].name}", style=discord.ButtonStyle.secondary,
    #                    emoji=f"{StarrailInfoParsed.characters[char_id].portrait}")
    # @discord.ui.button(label=f"{StarrailInfoParsed.characters[char_id].name}", style=discord.ButtonStyle.secondary,
    #                    emoji=f"{StarrailInfoParsed.characters[char_id].portrait}")
    # @discord.ui.button(label=f"{StarrailInfoParsed.characters[char_id].name}", style=discord.ButtonStyle.secondary,
    #                    emoji=f"{StarrailInfoParsed.characters[char_id].portrait}")
    # @discord.ui.button(label=f"{StarrailInfoParsed.characters[4].name}", style=discord.ButtonStyle.secondary,
    #                    emoji=f"{StarrailInfoParsed.characters[4].portrait}")
    # @discord.ui.button(label=f"{StarrailInfoParsed.characters[5].name}", style=discord.ButtonStyle.secondary,
    #                    emoji=f"{StarrailInfoParsed.characters[5].portrait}")


@bot.slash_command(description="Displays user Profile")  # Create a slash command
async def profile(ctx, uid: int):
    await ctx.defer(ephemeral=True)
    try:
        data: StarrailInfoParsed = await client.fetch_user(
            uid, replace_icon_name_with_url=True)
        embed = profile_embed(data)
        await ctx.respond(embed=embed, view=MyButton(ctx.view, data))

    except mihomo.errors.InvalidParams:
        await ctx.respond("Womp womp. Invalid UID. Please try again, with a different UID.")
        return None
    # except mihomo.errors.UserNotFound:
    # await ctx.respond(
    #     "Womp womp. User not found. "
    #     "\nThis could be because the wrapper is down. Did the game just update recently? "
    #     "\nPlease try again later.")
    # return None


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
