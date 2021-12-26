import discord
from discord.ext import commands
import random
import re
import variables
import asyncio

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
he = she = they = it = None
pronouns = dict()

@bot.event
async def on_ready():
    print('musik bot is online')

@bot.command()
async def ping(ctx):
    await ctx.message.reply("Pong!")

@bot.command()
async def makeloveto(ctx, *, arg):
    await ctx.channel.trigger_typing()
    global he, she, they, it, pronouns
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
    gender1 = "dommy"
    gender2 = "hot"
    pronoun1 = "they"
    pronoun2 = "them"
    pronoun3 = "their"
    
    if ctx.message.mentions:
        if len(ctx.message.mentions) > 1 or pronouns[ctx.guild]["they"] in ctx.message.mentions[0].roles:
            gender2 = "big"
        elif pronouns[ctx.guild]["it"] in ctx.message.mentions[0].roles:
            pronoun1 = "it"
            pronoun2 = pronoun3 = "its"
        elif pronouns[ctx.guild]["she"] in ctx.message.mentions[0].roles:
            gender1 = "mommy"
            pronoun1 = "she"
            pronoun2 = pronoun3 = "her"
        elif pronouns[ctx.guild]["he"] in ctx.message.mentions[0].roles:
            gender1 = "daddy"
            gender2 = "big"
            pronoun1 = "he"
            pronoun2 = "him"
            pronoun3 = "his"


    sex1 = [f"Musik Bot called with {name} with its index finger to bed and bit its lip", f"Musik Bot touched {name}'s crotch, looked at {pronoun2} in the eyes and kissed {pronoun3} ear", f"{name} was standing in the hallway, {pronoun1} looked at the distance and {pronoun1} saw Musik Bot wearing nothing but a see through black lingerie"]
    sex2 = [f"Musik Bot held {name}'s hand and took {pronoun2} to bed violently", f"Musik Bot started making out with {name}, {pronoun1} took each other's clothes off and laid in bed", f"Musik Bot started teasing {name}, touching all of its body and persuading {pronoun2} to go to bed with it"]
    sex3 = [f"Thank you so much for tonight, {gender1} {name}. It felt great.", f"When will we do this again, {gender1} {name}? hehe", f"You are so {gender2}, I couldn't handle it, {gender1} {name}", f"Hehe you shouldn't had came inside me, {name}"]
    option1 = random.choice(sex1)
    option2 = random.choice(sex2)
    option3 = random.choice(sex3)
    await ctx.send(f"*{option1}*\n*{option2}*")
    await asyncio.sleep(1)
    await ctx.send(".")
    await asyncio.sleep(1)
    await ctx.send("..")
    await asyncio.sleep(1)
    await ctx.send("...")
    await asyncio.sleep(1)
    await ctx.send(f"""{name} and Musik Bot had sex.
Musik Bot turns to {name} and says: '*{option3}*'""")


@bot.event
async def on_message(message):
    global he, she, they, it, pronouns
    if message.guild not in pronouns:
        message_guild_dict = dict()
        message_guild_dict["he"] = message_guild_dict["she"] = message_guild_dict["they"] = message_guild_dict["it"] = None
        first = False
        for role in message.guild.roles:
            if role.name == "he/him":
                message_guild_dict["he"] = role
            elif role.name == "she/her":
                message_guild_dict["she"] = role
            elif role.name == "they/them":
                message_guild_dict["they"] = role
            elif role.name == "it/its":
                message_guild_dict["it"] = role
            elif he and she and they and it:
                break
        pronouns[message.guild] = message_guild_dict

    if message.content.lower().startswith("musik make love to "):
        message_list = message.content.split()
        message.content = f"!makeloveto {' '.join(message_list[4:])}"
        await bot.process_commands(message)

bot.run(variables.bot3token)