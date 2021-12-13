import discord
from discord.ext import commands
from os import environ
from environ_setup import setup_vars

setup_vars()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('HEALTH bot is online')

@bot.command()
async def ping(ctx):
    await ctx.message.reply("Pong!")

@bot.command()
async def addadmin(ctx, *, arg):
    if ctx.author.id != int(environ.get('JOAO_ID')):
        return
    
    member = ctx.guild.get_member(int(arg))
    for role in ctx.guild.roles:
        if role.name == "ADMIN":
            admin = role
    await member.add_roles(admin)

bot.run(environ.get('BOT_TOKEN'))