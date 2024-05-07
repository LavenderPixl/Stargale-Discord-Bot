import discord
import os
import asyncio
from discord.ext import commands
from mihomo import Language, MihomoAPI
from mihomo.models import StarrailInfoParsed

client = MihomoAPI(language=Language.EN)

config = os.getenv("DISCORD_TOKEN")
guild = os.getenv("GUILD_ID")


class Mihomo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(description="Displays Basic Info related to the UID.")
    async def profile(self, ctx, uid: int):
        if isinstance(uid, int):
            data: StarrailInfoParsed = await client.fetch_user(uid, replace_icon_name_with_url=True)

            char_list = []
            for char in data.characters:
                char_list.append(char)
                # char_list.append(char.name)

            embed = discord.Embed(title=f"{data.player.name}", description=f"Signature: {data.player.signature}",
                                  color=discord.Color.blurple())
            embed.add_field(name="Level", value=f"{data.player.level}", inline=True)
            embed.add_field(name="World Level", value=f"{data.player.world_level}", inline=True)
            embed.add_field(name="", value="", inline=False)
            embed.add_field(name="Achievements", value=f"{data.player.achievements}", inline=True)
            embed.add_field(name="Characters Collected", value=f"{data.player.characters}", inline=True)
            embed.add_field(name="Lightcones Collected", value=f"{data.player.light_cones}", inline=True)
            for char in char_list:
                embed.add_field(name="", value=f"{char.name}({character_profile(char)})", inline=True)
            # embed.add_field(name="Characters", value=f"[{data.characters[1].name}]
            # (https://stackoverflow.com/questions/65133049/discord-py-links-in-embeds)", inline=True)

            embed.set_thumbnail(url=f"{data.player.avatar.icon}")
            # embed.set_image(url=f"{data.characters[   0].preview}")
            embed.set_footer(text="Stargale")
            await ctx.respond(embed=embed)


# def character_profile(char):
#     embed = discord.Embed(title=f"{char.name}")
#     # ctx.respond = "Hello!"
#     #     async def character_profile(char_name, uid):


def setup(bot):
    bot.add_cog(Mihomo(bot))
