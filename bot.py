import discord
from discord.ext import commands
import variables
import asyncio

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

oldperm = dict()
roles = [variables.eliteID,variables.nightmareID,variables.hurtID,variables.imtooID,variables.torquefestID,variables.killereliteID, variables.patron1, variables.patron2, variables.patron3,variables.adventurerID,variables.ndaID,variables.nda2ID]
react = None
qmessage = None
qflag = None
letter = None
imposter_embed = None
alphabet = {"🇦":"A","🇧":"B","🇨":"C","🇩":"D","🇪":"E","🇫":"F","🇬":"G","🇭":"H","🇮":"I","🇯":"J","🇰":"K","🇱":"L","🇲":"M","🇳":"N","🇴":"O","🇵":"P","🇶":"Q","🇷":"R","🇸":"S","🇹":"T","🇼":"W","🇺":"U","🇻":"V","🇽":"X","🇾":"Y","🇿":"Z"}
count = 0

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
    if ctx.author.id not in [variables.joao_id, bot.user.id]:
        return
    for channel in ctx.guild.channels:
        if channel.category and channel.category.name != "MODERATOR CHAT" and channel.name != "the-end-is-nye":
            daux = dict()
            daux["everyone"] = channel.overwrites_for(ctx.guild.default_role)
            for role in roles:
                if channel.overwrites_for(ctx.guild.get_role(role)):
                    daux[str(role)] = channel.overwrites_for(ctx.guild.get_role(role))
            oldperm[str(channel.id)] = daux
    await ctx.reply("old perms saved.")

@bot.command()
async def start(ctx):
    if ctx.author.id not in [variables.joao_id, bot.user.id]:
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
        if channel.category and channel.category.name != "MODERATOR CHAT" and channel.name != "the-end-is-nye":
            overwrite = oldperm[str(channel.id)]["everyone"]
            if overwrite.read_messages:
                overwrite.read_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    
    #   the rest of the roles
    for channel in ctx.guild.channels:
        for role_id in roles:
            if channel.category and channel.category.name != "MODERATOR CHAT" and channel.name != "the-end-is-nye":
                overwrite = oldperm[str(channel.id)][str(role_id)]
                if overwrite.read_messages:
                    overwrite.read_messages = False
                    await channel.set_permissions(ctx.guild.get_role(role_id), overwrite=overwrite)
    message = await ctx.reply("!imposter")
    await bot.process_commands(message)

@bot.command()
async def imposter(ctx):
    global react
    if ctx.author.id not in [variables.joao_id, bot.user.id]:
        return
    
    the_end_is_nyeID = bot.get_channel(variables.the_end_is_nyeID)
    await the_end_is_nyeID.trigger_typing()
    await asyncio.sleep(3)
    embed = discord.Embed(title="SUSPICIOUS BEHAVIOR DETECTED AMONG THIS SERVER'S ADMINISTRATIVE STAFF :: SCANNING POPULATION", description=" ")
    await the_end_is_nyeID.send(embed=embed)
    await the_end_is_nyeID.trigger_typing()
    await asyncio.sleep(5)

    embed = discord.Embed(title="SCAN RESULTS :: SEVERAL POTENTIAL IMPOSTER ACCOUNTS HAVE BEEN IDENTIFIED BY DEEP LEARNING METRICS", description=f"**REQUIRES {variables.react_number} <:cacopog:697621015337107466> REACTS TO CONTINUE**")
    #react = await the_end_is_nyeID.send(content="@everyone",embed = embed)
    react = await the_end_is_nyeID.send(embed = embed)
    emoji = bot.get_emoji(697621015337107466)
    await react.add_reaction(emoji)
    await asyncio.sleep(5)

@bot.command()
async def stop(ctx):
    if ctx.author.id not in [variables.joao_id, bot.user.id]:
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
            if channel.category and channel.category.name != "MODERATOR CHAT" and channel.name != "the-end-is-nye":
                overwrite = oldperm[str(channel.id)][str(role_id)]
                if overwrite.read_messages:
                    await channel.set_permissions(ctx.guild.get_role(role_id), overwrite=overwrite)

    #   @everyone
    for channel in ctx.guild.channels:
        if channel.category and channel.category.name != "MODERATOR CHAT" and channel.name != "the-end-is-nye":
            overwrite = oldperm[str(channel.id)]["everyone"]
            if overwrite and overwrite.read_messages:
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply("channels are visible")


async def eject_animation(member,avatar,channel):
    animation = [member+"ඞ",member+" was an ඞ",member+" was an Impostor. ඞ"]
    description = ".             .        .\n    .\n                 .\nඞ\n.          .\n                 .\n .                  ."
    embed=discord.Embed(title=" ", description=description, color=0xff0000)
    embed.set_author(name= member + " is being ejected.", icon_url= avatar)
    message = await channel.send(embed= embed)

    for frame in animation:
        await asyncio.sleep(2)
        description = ".             .        .\n    .\n                 .\n{0}\n.          .\n                 .\n .                  .".format(frame)
        embed=discord.Embed(title=" ", description=description, color=0xff0000)
        embed.set_author(name= member + " is being ejected.", icon_url= avatar)
        await message.edit(embed= embed)
    
    await asyncio.sleep(2)
    description = ".             .        .\n    .\n                 .\n{0}\n.          .\n                 .\n .                  .".format(member+" was an Impostor.")
    embed=discord.Embed(title=" ", description=description, color=0xff0000)
    embed.set_author(name= member + " has been ejected.", icon_url= avatar)
    await message.edit(embed= embed)


def checkletter(w,l):
    if l not in w:
        return False, -1
    for i in range(len(w)):
        if w[i] == l:
            return True, i

@bot.event
async def on_reaction_add(reaction, user):
    global react
    global imposter_embed
    global qmessage
    global alphabet
    global count
    global letter
    global qflag
    savior = reaction.message.guild.get_role(variables.saviorID)
    cacopog = bot.get_emoji(697621015337107466)

    if reaction.message == react and reaction.emoji == cacopog:
        await user.add_roles(savior,reason="cacopog reaction", atomic=True)
        if reaction.count == variables.react_number:
            
            imposters_list = [] # [image-url, (username1, username2, real/imposter1, real/imposter2), (username, date, no. messages), (username, date, no. messages), imposter-avatar-url]
            
            anar = ["https://i.imgur.com/lH9ALaO.png", ("ANAR :: LOST IN THE ETHER", "ANAR :: LOST IN THE ΞTHER","FAKE","REAL"), ("ANARCHY&ECSTASY#5556","April 2021","231"),("ANARCHY&ECSTASY#5555","April 2020","38680"), ("ANAR :: LOST IN THE ETHER", "https://i.imgur.com/vH6x9CS.jpg")]
            alice = ["https://i.imgur.com/zmuNZ8c.png", ("//alice++ (uk) :: hurt myself\\\\", "alice++ (uk) :: hurt myself", "REAL", "FAKE"), ("n_s#5150","April 2020","129234"),("n_s#4939","April 2021", "5"), ("alice++ (uk) :: hurt myself", "https://i.imgur.com/dF5FHPa.jpg")]
            jonny = ["https://i.imgur.com/wGePL6Q.png", ("JONNY UTAH", "JOHNNY UTAH", "REAL", "FAKE"), ("JONNY UTAH#1382","April 2020","32435"),("JOHNNY UTAH#0435", "April 2021", "4"), ("JOHNNY UTAH", "https://i.imgur.com/QSrWuE8.jpg")]
            aura = ["https://i.imgur.com/HwxN9gp.png", ("AURA","AURA :: BLACKBLOOD", "FAKE", "REAL"), ("Aura⚡#4272","April 2021", "6"),("Aura⚡#7274","November 2020","53102"), ("AURA", "https://i.imgur.com/7tQ5Ncx.jpg")]
            clown = ["https://i.imgur.com/ZwUNhS7.png", ("CHAMPAGNE JESTER", "CLOWNPOND", "REAL", "FAKE"), ("clownpond#1386","September 2020","30469"),("clownpond#9680","April 2021","3"), ("CLOWNPOND", "https://i.imgur.com/Sj6lFzs.jpg")]

            imposters_list.append(anar)
            imposters_list.append(alice)
            imposters_list.append(jonny)
            imposters_list.append(aura)
            imposters_list.append(clown)

            for imposters in imposters_list:
                description = f"""```diff
- SUBJECT A ({imposters[1][0]})
+ USERNAME:
  {imposters[2][0]}
+ JOINED HEALTHCORD:
  {imposters[2][1]}
+ MESSAGES SENT IN HEALTHCORD:
  {imposters[2][2]}

- SUBJECT B ({imposters[1][1]})
+ USERNAME:
  {imposters[3][0]}
+ JOINED HEALTHCORD:
  {imposters[3][1]}
+ MESSAGES SENT IN HEALTHCORD:
  {imposters[3][2]}
```"""
                embed = discord.Embed(title= "PLEASE IDENTIFY THE IMPOSTER", description= description, color=0xff0000)
                embed.set_image(url= imposters[0])
                imposter_embed = await reaction.message.channel.send(embed=embed)
                await imposter_embed.add_reaction("🇦")
                await imposter_embed.add_reaction("🇧")

                error_message = None
                if imposters[1][2] == "REAL":
                    imposter_option = "B"
                else:
                    imposter_option = "A"
                while True:
                    count = 0
                    for i in range(0,10):
                        if error_message and i == 3:
                            await error_message.delete()
                        await imposter_embed.edit(content= f"```COUNTING THE MOST REACTED OPTION...\n{str(10-i)}```", embed= embed)
                        await asyncio.sleep(1)
                    if letter == imposter_option:
                        break
                    else:
                        embed_error = discord.Embed(title= "ERROR IDENTIFYING IMPOSTER :: TRY AGAIN", description= " ", color=0xff0000)
                        error_message = await reaction.message.channel.send(content="", embed= embed_error)
                        await imposter_embed.clear_reactions()
                        await imposter_embed.add_reaction("🇦")
                        await imposter_embed.add_reaction("🇧")


                description = f"""```diff
- SUBJECT A ({imposters[1][2]} ACCOUNT)
+ USERNAME:
  {imposters[2][0]}
+ ACCOUNT CREATED ON:
  {imposters[2][1]}
+ MESSAGES SENT IN HEALTHCORD:
  {imposters[2][2]}

- SUBJECT B ({imposters[1][3]} ACCOUNT)
+ USERNAME:
  {imposters[3][0]}
+ ACCOUNT CREATED ON:
  {imposters[3][1]}
+ MESSAGES SENT IN HEALTHCORD:
  {imposters[3][2]}
```"""

                embed = discord.Embed(title= "IMPOSTER IDENTIFIED", description= description, color=0x00ff00)
                embed.set_image(url= imposters[0])
                await imposter_embed.edit(content="", embed= embed)
                await asyncio.sleep(3)
                await eject_animation(imposters[4][0],imposters[4][1],reaction.message.channel)
                await asyncio.sleep(3)

            
            album_guess = ("IMPOSTERS SUCCESFULLY EJECTED :: CORRUPTED FILE RECOVERED DURING PROFILE DELETION","_ACK_WASH","B___X____","FILE SUCCESSFULLY RETRIEVED","https://media.discordapp.net/attachments/918553475321847858/925477333270396968/THEENDISNYE.png","https://media.discordapp.net/attachments/918553475321847858/925407374796279828/DISCO4_PT2_FRONT_FINAL_FLAT.png")
            word = album_guess[1]
            blank = album_guess[2]
            embed = discord.Embed(title= album_guess[0], description= f"Guess a collaboration from DISCO4 PART II\nHint: it's an artist in this server.```{blank}```", color=0xff0000)
            embed.set_image(url= album_guess[4])
            qmessage = await reaction.message.channel.send(embed= embed)

            count = 0
            i = 3
            usedletters = []
            wrongletterlist = []
            wrongletters = "Letters not present in this word: "

            while True:
                await asyncio.sleep(1)
                if not(word):
                    embed = discord.Embed(title= album_guess[3], description=blank, color=0x00ff00)
                    embed.set_image(url= album_guess[5])
                    await qmessage.edit(content="", embed= embed)
                    break
                if qflag:
                    content = f"```\nCOUNTING THE MOST REACTED LETTER...\n{str(i)}```"
                    i-=1
                    await qmessage.edit(content= content)
                if i == -1:
                    fixedletter = letter
                    await qmessage.clear_reactions()
                    count = 0
                    i = 3
                    if fixedletter not in usedletters:
                        check,index = checkletter(word,fixedletter)
                        usedletters.append(fixedletter)
                        if check:
                            new_word = ""
                            new_blank = ""
                            for l in range(len(list(word))):
                                if word[l] != word[index]:
                                    new_word += word[l]
                                    new_blank += blank[l]
                                else:
                                    new_blank += word[l]
                                    new_word += "_"
                            blank = new_blank
                            word = new_word
                            if wrongletterlist:
                                description = "``" + blank + "``\n\n" + wrongletters
                            else:
                                description = "``" + blank + "``"
                            embed = discord.Embed(title= album_guess[0], description= description, color=0xff0000)
                            if album_guess[4]:
                                embed.set_image(url= album_guess[4])
                            await qmessage.edit(embed= embed)
                            tempflag = True
                            for x in word:
                                if x != "_" and x != " ":
                                    tempflag = False
                                    break
                            if tempflag:
                                word = False
                        else:
                            if wrongletterlist:
                                if fixedletter not in wrongletterlist:
                                    wrongletterlist.append(fixedletter)
                                    wrongletters += ", " + fixedletter
                                    description = "``" + blank + "``\n\n" + wrongletters
                                    embed = discord.Embed(title= album_guess[0], description= description, color=0xff0000)
                                    if album_guess[4]:
                                        embed.set_image(url= album_guess[4])
                                    await qmessage.edit(embed= embed)
                            else:
                                wrongletterlist.append(fixedletter)
                                wrongletters += fixedletter
                                description = "``" + blank + "``\n\n" + wrongletters
                                embed = discord.Embed(title= album_guess[0], description= description, color=0xff0000)
                                if album_guess[4]:
                                    embed.set_image(url= album_guess[4])
                                await qmessage.edit(embed= embed)
            await asyncio.sleep(2)
            qmessage = False
            qflag = False
            embed = discord.Embed(title=" ", description=" ", color=0x00ff00)
            embed.set_image(url="https://i.imgur.com/PFUyjyj.png")
            await reaction.message.channel.send(embed=embed)

    if reaction.emoji in alphabet and user.id != bot.user.id:
        if reaction.message == imposter_embed and reaction.count > count:
            count = reaction.count
            letter = alphabet[reaction.emoji]
        elif reaction.message == qmessage:
            qflag = True
            if reaction.count > count:
                count = reaction.count
                letter = alphabet[reaction.emoji]

bot.run(variables.bottoken)