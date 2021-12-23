import discord
from discord.ext import commands
import variables
import random

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

oldperm = dict()
roles = [variables.eliteID,variables.nightmareID,variables.hurtID,variables.imtooID,variables.torquefestID,variables.killereliteID, variables.patron1, variables.patron2, variables.patron3,variables.adventurerID,variables.ndaID,variables.nda2ID]

@bot.event
async def on_ready():
    print('musik bot is online')

@bot.command()
async def ping(ctx):
    await ctx.message.reply("Pong!")

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
    await ctx.reply("channels hidden")

@bot.command()
async def stop(ctx):
    if ctx.author.id != variables.joao_id:
        return
    #   the rest of the roles
    for channel in ctx.guild.channels:
        for role_id in roles:
            if channel.category and channel.category.name != "MODERATOR CHAT":
                overwrite = oldperm[str(channel.id)][str(role_id)]
                if overwrite.read_messages != False:
                    await channel.set_permissions(ctx.guild.get_role(role_id), overwrite=overwrite)

    #   @everyone
    for channel in ctx.guild.channels:
        if channel.category and channel.category.name != "MODERATOR CHAT":
            overwrite = oldperm[str(channel.id)]["everyone"]
            if overwrite and overwrite.read_messages != False:
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply("channels are visible")

@bot.command()
async def makeloveto(ctx):
    everyone = "@everyone"
    sex1 = [f"Musik Bot called with {everyone} with its index finger to bed and bit its lip", "Musik Bot touched {everyone}'s crotch, looked at {everyone} in the eyes and kissed {everyone}'s ear {everyone} was standing in the hallway, {everyone} looked at the distance and {everyone} saw Musik Bot wearing nothing but a see through black lingerie"]
    sex2 = [f"Musik Bot held {everyone}'s hand and took {everyone} to bed violently", "Musik Bot started making out with {everyone}, {everyone} took each other's clothes off and laid in bed", "Musik Bot started teasing {everyone}, touching all of its body and persuading {everyone} to go to bed with it"]
    sex3 = [f"Thank you so much for tonight, daddy {everyone}. It felt great.", "When will we do this again, {everyone}? hehe", "You are so big, I couldn't handle it, {everyone} Hehe you shouldn't had came inside me, {everyone}"]
    option1 = random.choice(sex1)
    option2 = random.choice(sex2)
    option3 = random.choice(sex3)
    await ctx.send(f"""
    *{option1}*
    *{option2}*
    .
    ..
    ...
    {everyone} and Musik Bot had sex.
    Musik Bot turns to {everyone} and says: '*{option3}*'
    """)

@bot.event
async def on_message(message):
    if message.content.startswith("musik make love to "):
        message.content = "!makeloveto"
        await bot.process_commands(message)
    elif message.content.startswith("!"):
        await bot.process_commands(message)

bot.run(variables.bot3token)