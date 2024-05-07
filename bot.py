import discord
import os
from dotenv import load_dotenv

load_dotenv()
config = os.getenv("DISCORD_TOKEN")
guild = os.getenv("GUILD_ID")

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)


cogs_list = [
    # 'prydwen',
    'hsr'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        guild_count = guild_count + 1
    print(f"Bot is in {guild_count} guild/s.")
    print(f"Guilds: {guild.name} | ID: {guild.id}")


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
