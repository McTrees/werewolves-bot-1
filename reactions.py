import discord
import asyncio
from discord.ext import commands
import botobject

bot = botobject.bot

channelid = "303113715773997056"

@bot.command(pass_context=True)
async def rbr(ctx, messageid):
    msgchannel = bot.get_channel(channelid)
    msg = await bot.get_message(msgchannel, str(messageid))
    users = list(bot.get_all_members())
    for reaction in msg.reactions:
            for user in users:
                roles = []
                for role in user.roles:
                    roles.append(role.name)
                    if "RemoveReactions" in roles:
                        await bot.remove_reaction(msg, reaction.emoji, ctx.message.author)
                    else:
                        print("alive apparently")
                        pass