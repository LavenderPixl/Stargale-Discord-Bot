# import os
# import discord
# from discord.ext import commands
# from mihomo import Language, MihomoAPI
# from mihomo.models import StarrailInfoParsed
# 
# client = MihomoAPI(language=Language.EN)
# 
# config = os.getenv("DISCORD_TOKEN")
# guild = os.getenv("GUILD_ID")
# 
# 
# class Mihomo(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
# 
#     @discord.command(description="Displays Basic Info related to the UID.")
#     async def profile(self, ctx, uid: int):
#         if isinstance(uid, int):
#             data: StarrailInfoParsed = await client.fetch_user(uid, replace_icon_name_with_url=True)
# 
#             embed = discord.Embed(title=f"{data.player.name}", description=f"Signature: {data.player.signature}",
#                                   color=discord.Color.blurple())
#             embed.add_field(name="Level", value=f"{data.player.level}", inline=True)
#             embed.add_field(name="World Level", value=f"{data.player.world_level}", inline=True)
#             embed.add_field(name="", value="", inline=True)
#             embed.add_field(name="Achievements", value=f"{data.player.achievements}", inline=True)
#             embed.add_field(name="Characters Collected", value=f"{data.player.characters}", inline=True)
#             embed.add_field(name="Lightcones Collected", value=f"{data.player.light_cones}", inline=True)
# 
#             # options = []
#             # for char in data.characters:
#             #     # options.append(discord.SelectOption(label=char.name, emoji=char.portrait))
#             #     embed.add_field(name="", value=f"{char.name}({await character_profile(ctx, char)})", inline=True)
# 
#             embed.set_thumbnail(url=f"{data.player.avatar.icon}")
#             embed.set_footer(text="Stargale")
#             await ctx.respond(embed=embed, view=await button(ctx))
# 
# 
# class MyButton(discord.ui.View):
#     @discord.ui.button(label="Character Name", style=discord.ButtonStyle.secondary)
#     async def button_callback(self, interaction):
#         await interaction.response.send_message("Character Name")
# 
# 
# async def button(ctx):
#     await ctx.respond(view=MyButton())
# 
# 
# async def character_profile(ctx, char):
#     embed = discord.Embed(title=f"{char.name}",
#                           description=f"Level: {char.level} | Rarity: {rarity(char.rarity)}  ",
#                           color=discord.Color.blurple())
#     embed.set_image(url=f"{char.portrait}")
#     await ctx.respond(embed=embed)
# 
# 
# def rarity(stars: int):
#     i: int = 0
#     fin: str = ""
#     while i < stars:
#         i += 1
#         fin += "⭐"
#     return fin
# 
# 
# def setup(bot):
#     bot.add_cog(Mihomo(bot))
# 
# # class Dropdown(discord.ui.Select):
# #     def __init__(self, bot: discord.Bot):
# #         self.bot = bot
# #         options = [
# #             discord.SelectOption(emoji="Icon here", label="Name here"),
# #         ]
# # 
# #         super().__init__(
# #             placeholder="Pick a Character",
# #             options=options
# #         )
# # 
# #     async def callback(self, interaction: discord.Interaction):
# #         await interaction.response.send_message(
# #             f"Picked Character: {self.values[0]}", ephemeral=True
# #         )
# # 
# # 
# # class DropdownView(discord.ui.View):
# #     def __init__(self, bot: discord.Bot):
# #         self.bot = bot
# #         super().__init__()
# #         self.add_item(Dropdown(bot))
# # 
# # 
# # bot = discord.Bot()
# # 
# # 
# # @discord.command()
# # async def c(ctx: discord.ApplicationContext):
# #     view = DropdownView(bot)
# #     await ctx.respond("Pick the character, ig", view=view)