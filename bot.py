import discord
from discord.ext import commands
from dotenv import dotenv_values


config = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)


@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        guild_count = guild_count + 1
    print("Bot is in " + str(guild_count) + " guilds.")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def notping(ctx):
    await ctx.send('log')
    # print("Logged in as", self.user.name)


@bot.command()
async def leave(ctx):
    await ctx.close()

bot.run(config["DISCORD_TOKEN"])