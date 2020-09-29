import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio



Client = discord.Client()
client = commands.Bot(command_prefix = "?")



# On voice state update:
@client.event
async def on_voice_state_update(member, before, after):
    file = open("config.txt", "r")
    config = eval(file.read())
    file.close()
    
    if not after.channel == None:
        if after.channel.id == config[1]:
            for i in config[2]:
                if member.name.lower() in config[2][i]:
                    await member.edit(voice_channel = client.get_channel(i))
              
            if member.nick != None:
                for i in config[2]:
                    if member.nick.lower() in config[2][i]:
                        await member.edit(voice_channel = client.get_channel(i))
                                          

    if before != None:
        empty = True
        if before.channel != None:
            for i in before.channel.members:
                empty = False

            if empty:
                try:
                    del config[2][before.channel.id]
                    await before.channel.delete()
                except:
                    pass

    file = open("config.txt", "w")
    file.write(str(config))
    file.close()


    
# On ready:
@client.event
async def on_ready():
    print("Bot is ready!")
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("?help"))



    
# On message:
@client.event
async def on_message(message):

    content = message.content
    channel = message.channel
    author = message.author
    name = author.name

    msg = content.split(" ")

   

    if msg[0].lower() in ["?help"]:
        await message.delete()
        embed = discord.Embed(title = "**Bot Commands**",
                                description = "",
                                color = 0x22a7f0)

        embed.add_field(name = "**?help**", value = "Shows this menu")
        embed.add_field(name = "**?setrole**", value = "Sets the role which is needed for using the `?voice` command.\nSyntax: ?setrole [roleName]")
        embed.add_field(name = "**?setchannel**", value = "Sets the voice channel you are currently in as waiting channel.\nSyntax: ?setchannel")
        embed.add_field(name = "**?voice**", value = "Creates a new voice channel and moves the users given in the arguments in this channel.\nSyntax: ?voice _name_ _user1_, _user2_, _etc_")
        embed.add_field(name = "**?info**", value = "Gives information about needed role for ?voice and which the waiting channel is.\nSyntax: ?info")


        await channel.send(embed = embed, delete_after = 300)


                
    if msg[0].lower() in ["?voice"]:
        await message.delete()
        file = open("config.txt", "r")
        config = eval(file.read())
        file.close()
        
        if config[1] != 0:
            authorRolesIds = []
            for i in author.roles:
                authorRolesIds.append(i.id)
            
            if config[0] in authorRolesIds or author.guild_permissions.administrator:
                if len(msg) < 3:
                    await channel.send("**:x: Syntax: ?voice _name_ _user1_, _user2_, _etc_ :x:**", delete_after = 15)

                else:
                    category = client.get_channel(735738201209176084)
                    createdChannel = await message.guild.create_voice_channel(msg[1], category = category)

                    setup = []
                    output = ""
                    spaceCounter = 0
                    for i in content:
                        if spaceCounter >= 2:
                            if i != ",":
                                output += i.lower()

                            else:
                                if output.startswith(" "):
                                    output = output[1:]
                                    
                                setup.append(output)
                                output = ""

                        if i == " ":
                            spaceCounter += 1

                    if output.startswith(" "):
                        output = output[1:]
                        
                    setup.append(output)
                                
                    config[2][createdChannel.id] = setup

                    output = ""
                    guildMembers = []
                    for i in message.guild.members:
                        guildMembers.append(i.name)
                        
                    for i in setup:
                        nameFound = False
                        for member in guildMembers:
                            if member.lower() == i:
                                output += "`" + str(member) + "` "
                                nameFound = True

                        if not nameFound:
                            output += "\n`" + str(i) + "` "

                    output = output[:len(output) - 1]
                    
                    await author.send("**Your boosters in channel `" + str(createdChannel.name) + "` are: " + str(output) + ".**")
                    for member in client.get_channel(config[1]).members:
                        if member.name.lower() in config[2][createdChannel.id]:
                            await member.edit(voice_channel = createdChannel)

                        if not member.nick == None:
                            if member.nick.lower() in config[2][createdChannel.id]:
                                await member.edit(voice_channel = createdChannel)

                    file = open("config.txt", "w")
                    file.write(str(config))
                    file.close()

            else:
                await channel.send("**:x: You do not have permissions for `?voice`. :x:**", delete_after = 15)

        else:
            await channel.send("**:x: There is no waiting channel defined. :x:**", delete_after = 15)





    if msg[0].lower() in ["?setrole"]:
        await message.delete()
        if author.id == 698458162147229748:
            if len(msg) == 1:
                await channel.send("**:x: Syntax: ?setrole [roleName] :x:**", delete_after = 15)

            else:
                roles = {}
                for i in author.guild.roles:
                    roles[str(i).lower()] = [i.name, i.id]

                if not content[9:].lower() in roles:
                    await channel.send("**:x: Role could not be found. :x:**", delete_after = 15)

                else:
                    file = open("config.txt", "r")
                    config = eval(file.read())
                    file.close()
                    
                    await channel.send("**Role `" + str(roles[content[9:].lower()][0]) + "` has been set.**", delete_after = 15)

                    config[0] = roles[content[9:].lower()][1]

                    file = open("config.txt", "w")
                    file.write(str(config))
                    file.close()

        else:
            await channel.send("**:x: You do not have permissions for `?setrole`. :x:**", delete_after = 15)



    if msg[0].lower() in ["?setchannel", "?setwaitingchannel"]:
        await message.delete()
        if author.id == 698458162147229748:
            if author.voice == None:
                await channel.send("**:x: You are not connected to a voice channel. :x:**", delete_after = 15)

            else:
                await channel.send("**Waiting channel has been set as `" + str(author.voice.channel) + "`.**", delete_after = 15)
                file = open("config.txt", "r")
                config = eval(file.read())
                file.close()

                config[1] = author.voice.channel.id

                file = open("config.txt", "w")
                file.write(str(config))
                file.close()

        else:
            await channel.send("**:x: You do not have permissions for `?setchannel`. :x:**", delete_after = 15)



    if msg[0].lower() in ["?info", "?config"]:
        await message.delete()
        file = open("config.txt", "r")
        config = eval(file.read())
        file.close()

        if config[0] == 0:
            var1 = "has not been set yet"
        else:
            var1 = message.guild.get_role(config[0]).name
            
        if config[1] == 0:
            var0 = "has not been set yet"
        else:
            var0 = client.get_channel(config[1]).name

        await channel.send("**Waiting channel: `" + str(var0) + "`\nNeeded role for ?voice: `" + str(var1) + "`**", delete_after = 60)

            
client.run("NzU4MTM2NDcwODQxNDU4Njg4.X2qjnA.HFi8VlFiA7eMw07Rq-FwqKHNEM0")
