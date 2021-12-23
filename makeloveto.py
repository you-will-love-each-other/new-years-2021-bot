import discord
from discord.ext import commands
import random
import re
import variables

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
flag = True
he = she = they = None

@bot.event
async def on_ready():
    print('musik bot is online')

@bot.command()
async def ping(ctx):
    await ctx.message.reply("Pong!")

@bot.command()
async def makeloveto(ctx, *, arg):
    if ctx.message.mention_everyone:
        await ctx.send("I can't make love to everyone. <:help:736196814654668830>")
        return
    elif ctx.message.channel_mentions:
        await ctx.send("I can't make love to a channel. <:help:736196814654668830>")
        return
    elif ctx.message.role_mentions:
        await ctx.send("I can't make love to a role. <:help:736196814654668830>")
        return

    name = arg
    genders = list()
    if len(ctx.message.mentions) > 1 or they in ctx.message.mentions[0]:
        gender1 = "dommy"
        gender2 = "big"
    elif she in ctx.message.mentions[0]:
        gender1 = "mommy"
        gender2 = "hot"
    elif he in ctx.message.mentions[0]:
        gender1 = "daddy"
        gender2 = "big"


    sex1 = ["Musik Bot called with {name} with its index finger to bed and bit its lip", "Musik Bot touched {name}'s crotch, looked at {name} in the eyes and kissed {name}'s ear {name} was standing in the hallway, {name} looked at the distance and {name} saw Musik Bot wearing nothing but a see through black lingerie"]
    sex2 = ["Musik Bot held {name}'s hand and took {name} to bed violently", "Musik Bot started making out with {name}, {name} took each other's clothes off and laid in bed", "Musik Bot started teasing {name}, touching all of its body and persuading {name} to go to bed with it"]
    sex3 = ["Thank you so much for tonight, {gender1} {name}. It felt great.", "When will we do this again, {gender1} {name}? hehe", "You are so {gender2}, I couldn't handle it, {gender1} {name}", "Hehe you shouldn't had came inside me, {name}"]
    option1 = random.choice(sex1)
    option2 = random.choice(sex2)
    option3 = random.choice(sex3)
    await ctx.send("""
    *{option1}*
    *{option2}*
    .
    ..
    ...
    {name} and Musik Bot had sex.
    Musik Bot turns to {name} and says: '*{option3}*'
    """)


@bot.event
async def on_message(message):
    global flag, he, she, they
    if flag:
        first = False
        for role in message.guild.roles:
            if role.name == "he/him":
                he = role
            elif role.name == "she/her":
                she = role
            elif role.name == "they/them":
                they = role
            elif he and she and they:
                break

    if message.content.startswith("musik make love to "):
        message_list = message.content.split()
        message.content = "!makeloveto {message_list[4]}"
        await bot.process_commands(message)

bot.run(variables.bot3token)