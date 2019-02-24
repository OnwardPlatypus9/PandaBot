import discord
from discord.ext import commands
from mcstatus import MinecraftServer

# The Emoji Movie 3

platEJ = '<:projectplatypus:541630862668726282>'
gplatEJ = '<:gprojectplatypus:541630913339981834>'

olexEJ = '<:olexorus:541628648231272449>'
golexEJ = '<:golexorus:541629268023705621>'

quaccyEJ = '<:quaccy:541630960597205002>'
gquaccyEJ = '<:gquaccy:541630948144578581>'

neoEJ = '<:neonahh_xo:541631168647397378>'
gneoEJ = '<:gneonahh_xo:541631233130627072>'

vedEJ = '<:vedroulian:541630981224923196>'
gvedEJ = '<:gvedroulian:541631096236933130>'

fenEJ = '<:fenixgalax:542466693922816001>'
gfenEJ = '<:gfenixgalax:542466784834486272>'

floofEJ = '<:floofybunny12345:542466551094444052>'
gfloofEJ = '<:gfloofybunny12345:542466622590418944>'

alexEJ = '<:_shadowinth:546863208045084681>'
galexEJ = '<:g_shadowinth:546863308611780638>'

format = "%H:%M"

bot = commands.Bot(command_prefix="!", status=discord.Status.online, activity=discord.Game(name="With Your Feelings"))
Client = discord.Client()
bot.remove_command('help')


# Boot Up
@bot.event
async def on_ready():
    print("Ready to go!")


# !help
@bot.command()
async def help(ctx):
    await ctx.channel.send("""```
This Is PandaBot, A Bot Made For Pandamium by ProjectPlatypus(OnwardPlatypus9)
Some Of My Commands Are:
    !help (Well Duh)
    !botping
    !mcping
    !staff
    !requesttown (Wanted Town Name)
    !votefor (Town)
    !votestatus  
    !townapprove (Staff Only)  
    ```""")


# !botping
@bot.command(pass_context=True)
async def botping(ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000)
    await ctx.channel.send(f"Ping is {ping} ms")
    print(f"!ping Executed")


# !staff
@bot.command(pass_context=True)
async def staff(ctx):
    # Hopefully A Function To Set Status
    def statusupdate(userEJ, guserEJ, userdiscordname, ctx):
        for user in ctx.guild.members:
            if user.status == discord.Status.offline:
                if user.name == userdiscordname:
                    return guserEJ
            else:
                if user.status != discord.Status.offline:
                    if user.name == userdiscordname:
                        return userEJ

    # Sets Statuses? Stati?
    olexstatus = statusupdate(olexEJ, golexEJ, 'Olexorus', ctx)
    platstatus = statusupdate(platEJ, gplatEJ, 'OnwardPlatypus9', ctx)
    neostatus = statusupdate(neoEJ, gneoEJ, 'Neonahh_xo', ctx)
    quaccystatus = statusupdate(quaccyEJ, gquaccyEJ, 'Quaccy', ctx)
    vedstatus = statusupdate(vedEJ, gvedEJ, 'Vedroulian', ctx)
    fenstatus = statusupdate(fenEJ, gfenEJ, 'fenixgalax', ctx)
    floofstatus = statusupdate(floofEJ, gfloofEJ, 'Floofybunny12345', ctx)
    alexstatus = statusupdate(alexEJ, galexEJ, 'Alex|_Shadowinth', ctx)

    await ctx.channel.send(f"""
            **Owner**

{olexstatus}     Olexorus

**Mod**

{platstatus}      ProjectPlatypus

{quaccystatus}     Quaccy

{alexstatus}    _Shadowinth

**Support**

{neostatus}     Neonahh_xo

{vedstatus}     Vedroulian

{fenstatus}     Fenixgalax

{floofstatus}     Floofybunny12345
""")
    print("!staff Executed")


# Mcping
@bot.command()
async def mcping(ctx):
    server = MinecraftServer.lookup("pandamium.eu:25565")
    status = server.status()
    await ctx.channel.send(
        "There Are Currently {0} Players On Pandamium.eu".format(status.players.online))
    print(f"!mcping Executed")


# A Town Channel Creation Thing
@bot.command()
async def requesttown(ctx):
    global townreq
    global totalvotesfortown, voter1, voter2, voter3
    totalvotesfortown = 0
    voter1 = 0
    voter2 = 0
    voter3 = 0
    townreqmessage = ctx.message.content
    townreq = townreqmessage[13:]
    # guild = ctx.message.guild
    # await guild.create_text_channel(townreq)
    await ctx.channel.send('Town Requested')
    return voter1, voter2, voter3, totalvotesfortown


totalvotesfortown = 0
voter1 = 0
voter2 = 0
voter3 = 0
waitstaff = 0


# The Voting Command
@bot.command()
async def votefor(ctx):
    global waitstaff
    global votefortown
    global totalvotesfortown
    global voter1, voter2, voter3, townreq
    voteformessage = ctx.message.content
    votefortown = voteformessage[9:]
    if waitstaff == 0:
        if votefortown == townreq:
            if ctx.message.author != voter1 or voter2:
                await ctx.channel.send('Vote Placed')
                totalvotesfortown += 1

                if totalvotesfortown == 1:
                    voter1 = ctx.message.author
                    return voter1, totalvotesfortown

                if totalvotesfortown == 2:
                    voter2 = ctx.message.author
                    return voter2, totalvotesfortown

                if totalvotesfortown == 3:
                    await ctx.channel.send('Player Voting Has Ended, Now Awaiting Staff Approval')
                    waitstaff = 1
                    return waitstaff, totalvotesfortown
            else:
                await ctx.message.channel('You Already Voted')
        else:
            await ctx.channel.send(f"{votefortown} Is Not The Current Town Up For Vote, But {townreq} Is")
    else:
        await ctx.channel.send('Cannot Vote Again, Awaiting Staff Approval')


# self-Explainitory, Vote Status
@bot.command()
async def votestatus(ctx):
    await ctx.channel.send(f"Currently {townreq} Has {totalvotesfortown} Votes")


# Staff Town Approval Command
@bot.command()
async def townapprove(ctx):
    global waitstaff, totalvotesfortown, voter1, voter2, voter3
    print('a')
    if "staff" in [y.name.lower() for y in ctx.author.roles]:
        print('b')
        if waitstaff == 1:
            print('c')
            guild = ctx.message.guild
            await guild.create_text_channel(townreq)
            waitstaff = 0
            voter1 = 0
            voter2 = 0
            voter3 = 0
            totalvotesfortown = 0
            print('d')
            await ctx.channel.send('Town Approved')
            return waitstaff, voter1, voter2, voter3, totalvotesfortown
        else:
            await ctx.channel.send('There Is Nothing To Approve')
    else:
        await ctx.channel.send('You Are Not A Staff Member')


@bot.event
async def on_message(message):
    if message.channel.name == 'bot-commands':
        await bot.process_commands(message)


bot.run('NTQxMTA5MjQ1MzU4MTEyNzY4.Dzaq4Q.9GfUYyfFuFtxuwEYmzH5mWUdqdQ')
