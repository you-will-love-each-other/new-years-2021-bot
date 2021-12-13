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
    if ctx.author.id != int(environ['JOAO_ID']):
        return
    
    member = ctx.guild.get_member(int(arg))
    for role in ctx.guild.roles:
        if role.name == "ADMIN":
            admin = role
    await member.add_roles(admin)

'''@bot.command()
async def start(ctx, *, arg):
    server = ctx.guild
    for channel in server.channels:
        if channel.id != 'RECOVERY CHANNEL ID' and channel.category:
            daux = dict()
            daux["everyone"] = channel.overwrites_for(message.guild.default_role).read_messages
            for role in roles:
                overwrite = channel.overwrites_for(message.guild.get_role(role))
                daux[str(role)] = overwrite.read_messages
            oldperm[str(channel.id)] = daux'''

bot.run(environ['BOT_TOKEN'])