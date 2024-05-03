import discord
import os
import requests
from dotenv import load_dotenv

load_dotenv()
config = os.getenv("DISCORD_TOKEN")
guild = os.getenv("GUILD_ID")

intents = discord.Intents.all()
bot = discord.Bot()


@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        guild_count = guild_count + 1
    print(f"Bot is in {guild_count} guild/s.")
    print(f"Guilds: {guild.name} | ID: {guild.id}")


@bot.command(description="Displays all available commands.", guild_ids=[guild])
async def pryd_help(ctx):
    embed = discord.Embed(color=discord.Color.blurple())
    embed.set_author(name="Help : list of commands available")
    embed.add_field(name="/pryd_help", value="Shows this message", inline=False)
    embed.add_field(name="/prydwen", value="Link to Prydwen", inline=False)
    embed.add_field(name="/prydchar [character name]", value="Link to specific character, on Prydwen.", inline=False)
    await ctx.respond(embed=embed)


@bot.command(description="Sends a link to Prydwen.", guild_ids=[guild])
async def prydwen(ctx):
    embed = discord.Embed(title="Prydwen | All characters.", url="https://www.prydwen.gg/star-rail/characters",
                          color=discord.Color.blue())
    await ctx.respond(embed=embed)


@bot.command(description="Sends a link to the specific characters profile, on Prydwen.", guild_ids=[guild])
async def prydchar(ctx, character: str):
    character_name = character.lower()
    response = requests.get("https://www.prydwen.gg/star-rail/characters/" + character_name)

    if response.status_code == 404:
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name="! Invalid Character name !")
        embed.add_field(name="If the character has a space between two names/words, please separate with a line",
                        value="(ex: black-swan)", inline=False)
    else:
        embed = discord.Embed(title="Prydwen | " + character_name,
                              url="https://www.prydwen.gg/star-rail/characters/" + character_name,
                              color=discord.Color.blue())

    await ctx.respond(embed=embed)


bot.run(config)
