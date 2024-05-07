# import discord
# import os
# import requests
# from dotenv import load_dotenv
# 
# load_dotenv()
# config = os.getenv("DISCORD_TOKEN")
# guild = os.getenv("GUILD_ID")
# 
# intents = discord.Intents.all()
# bot = discord.Bot()
# 
# 
# async def pryd_help(ctx):
#     embed = discord.Embed(title="Help : list of commands available", color=discord.Color.blurple())
#     embed.add_field(name="/sg help", value="Shows this message", inline=False)
#     embed.add_field(name="/sg prydwen", value="Link to Prydwen", inline=False)
#     embed.add_field(name="/sg character [character name]", value="Link to specific character, on Prydwen.", inline=False)
#     await ctx.respond(embed=embed)
# 
# 
# async def pryd_prydwen(ctx):
#     embed = discord.Embed(title="Prydwen | All characters.", url="https://www.prydwen.gg/star-rail/characters",
#                           color=discord.Color.blue())
#     await ctx.respond(embed=embed)
# 
# 
# async def pryd_character_profile(ctx, character: str):
#     character_name = character.lower()
#     titled_name = character.title()
#     response = requests.get("https://www.prydwen.gg/star-rail/characters/" + character_name)
# 
#     if response.status_code == 404:
#         embed = discord.Embed(color=discord.Color.red())
#         embed.set_author(name="! Invalid Character name !")
#         embed.add_field(name="If the character has a space between two names/words, please separate with a line",
#                         value="(ex: black-swan)", inline=False)
#     else:
#         embed = discord.Embed(title="Prydwen | " + titled_name,
#                               url="https://www.prydwen.gg/star-rail/characters/" + character_name,
#                               color=discord.Color.blue())
# 
#     await ctx.respond(embed=embed)