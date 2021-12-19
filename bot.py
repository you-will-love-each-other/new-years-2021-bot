import discord
from discord.ext import commands
import variables

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
oldperms = dict()
roles = [variables.killereliteID, variables.patron1, variables.patron2, variables.patron3,variables.eliteID,variables.nightmareID,variables.hurtID,variables.imtooID,variables.torquefestID,variables.adventurerID,variables.ndaID]

@bot.event
async def on_ready():
    print('HEALTH bot is online')

@bot.command()
async def ping(ctx):
    await ctx.message.reply("Pong!")

@bot.command()
async def start(ctx):
    for role_id in roles:
        role = ctx.guild.get_role(role_id)
        perms = role.permissions
        oldperms[str(role_id)] = perms
        perms.view_channel = False
        await role.edit(permissions= perms)

@bot.command()
async def stop(ctx):
    for role_id in roles:
        role = ctx.guild.get_role(role_id)
        perms = role.permissions
        perms.view_channel = oldperms[str(role.id)]
        await role.edit(permissions= perms)

bot.run(variables.bottoken)