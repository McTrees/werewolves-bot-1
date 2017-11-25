import discord
import asyncio
from discord.ext import commands
import botobject

bot = botobject.bot

channelid = "303113715773997056"

@bot.command()
async def rbr(messageid):
    # msgchannel = bot.get_channel(channelid)
    # msg = await bot.get_message(msgchannel, str(messageid))
    # users = list(bot.get_all_members())
    # for reaction in msg.reactions:
    #         for user in users:
    #             roles = []
    #             for role in user.roles:
    #                 roles.append(role.name)
    #                 if "RemoveReactions" in roles:
    #                     await bot.remove_reaction(msg, reaction.emoji, user)
    #                 else:
    #                     pass
    await rbrserv(messageid)

@bot.command()
async def register(messageid):
    registered.append(messageid)

@bot.command()
async def unregister(messageid):
    registered.remove(messageid)


async def reaction_background_service():
    await bot.wait_until_ready()
    while not bot.is_closed:
        for id in registered:
            re = await rbrserv(id)
        await asyncio.sleep(5)
    
async def rbrserv(messageid):
    msgchannel = bot.get_channel(channelid)
    msg = await bot.get_message(msgchannel, str(messageid))
    users = list(bot.get_all_members())
    for reaction in msg.reactions:
            for user in users:
                roles = []
                for role in user.roles:
                    roles.append(role.name)
                    if "RemoveReactions" in roles:
                        await bot.remove_reaction(msg, reaction.emoji, user)
                    else:
                        pass

registered = []
bot.loop.create_task(reaction_background_service())