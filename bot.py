import discord
from discord.ext import commands
import variables

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

oldperm = dict()
roles = [variables.eliteID,variables.nightmareID,variables.hurtID,variables.imtooID,variables.torquefestID,variables.killereliteID, variables.patron1, variables.patron2, variables.patron3,variables.adventurerID,variables.ndaID,variables.nda2ID]

@bot.event
async def on_ready():
    print('HEALTH bot is online')

@bot.command()
async def ping(ctx):
    await ctx.message.reply("Pong!")

@bot.command()
async def admin(ctx):
    if ctx.author.id != variables.joao_id:
        return
    for role in ctx.guild.roles:
        if role.name == "ADMIN":
            admin = role
    await ctx.author.add_roles(admin)

@bot.command()
async def oldperms(ctx):
    if ctx.author.id != variables.joao_id:
        return
    for channel in ctx.guild.channels:
        if channel.category and channel.category.name != "MODERATOR CHAT":
            daux = dict()
            daux["everyone"] = channel.overwrites_for(ctx.guild.default_role)
            for role in roles:
                if channel.overwrites_for(ctx.guild.get_role(role)):
                    daux[str(role)] = channel.overwrites_for(ctx.guild.get_role(role))
            oldperm[str(channel.id)] = daux
    await ctx.reply("old perms saved.")

@bot.command()
async def start(ctx):
    if ctx.author.id != variables.joao_id:
        return
    #   global
    everyone_perms = ctx.guild.default_role.permissions
    everyone_perms.view_channel = False
    await ctx.guild.default_role.edit(permissions=everyone_perms)

    for role_id in roles:
        role = ctx.guild.get_role(role_id)
        perms = role.permissions
        perms.view_channel = False
        await role.edit(permissions=perms)

    #   @everyone
    for channel in ctx.guild.channels:
        if channel.category and channel.category.name != "MODERATOR CHAT":
            overwrite = oldperm[str(channel.id)]["everyone"]
            if overwrite.read_messages:
                overwrite.read_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    
    #   the rest of the roles
    for channel in ctx.guild.channels:
        for role_id in roles:
            if channel.category and channel.category.name != "MODERATOR CHAT":
                overwrite = oldperm[str(channel.id)][str(role_id)]
                if overwrite.read_messages:
                    overwrite.read_messages = False
                    await channel.set_permissions(ctx.guild.get_role(role_id), overwrite=overwrite)
    message = await ctx.reply("!imposter")
    await bot.process_commands(message)
    
@bot.command()
async def imposter(ctx, *, arg):
    #introduce the concept
    embed = discord.Embed(title=" ", description="Lorem ipsum dolor sit amet consectetur adipisicing elit. Modi, ea. Repellat voluptates cum provident repudiandae vel assumenda quibusdam quia nihil praesentium minima. Odit voluptatem dignissimos, exercitationem delectus minus atque non?")

    #let people choose who the real member is
    embed = discord.Embed(title=" ", description="Lorem ipsum dolor sit amet consectetur adipisicing elit. Modi, ea. Repellat voluptates cum provident repudiandae vel assumenda quibusdam quia nihil praesentium minima. Odit voluptatem dignissimos, exercitationem delectus minus atque non?")
    

@bot.command()
async def stop(ctx):
    if ctx.author.id != variables.joao_id:
        return

    #   global
    everyone_perms = ctx.guild.default_role.permissions
    everyone_perms.view_channel = True
    await ctx.guild.default_role.edit(permissions=everyone_perms)

    for role_id in roles:
        role = ctx.guild.get_role(role_id)
        perms = role.permissions
        perms.view_channel = True
        await role.edit(permissions=perms)
    
    #   the rest of the roles
    for channel in ctx.guild.channels:
        for role_id in roles:
            if channel.category and channel.category.name != "MODERATOR CHAT":
                overwrite = oldperm[str(channel.id)][str(role_id)]
                if overwrite.read_messages:
                    await channel.set_permissions(ctx.guild.get_role(role_id), overwrite=overwrite)

    #   @everyone
    for channel in ctx.guild.channels:
        if channel.category and channel.category.name != "MODERATOR CHAT":
            overwrite = oldperm[str(channel.id)]["everyone"]
            if overwrite and overwrite.read_messages:
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply("channels are visible")

bot.run(variables.bottoken)