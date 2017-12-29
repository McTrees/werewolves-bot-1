import discord
import asyncio
from discord.ext import commands
import botobject
import sqlite3
import re

bot = botobject.bot

@bot.command(pass_context=True)
async def signup(ctx, emoji):
    try:
        emoji = emoji #check an emoji was provided
    except:
        await bot.say("I'm glad you want to join the game, but the correct syntax for this command is `!signup :emoji:`")
    conn = sqlite3.connect("SignedUp.db")
    c = conn.cursor()
    try:
        emojihex = hex(ord(emoji))
    except:
        await bot.say("Please use a regular emoji. Emoji with a custom skin colour emoji will not work.")
        return

    try:
        await bot.add_reaction(ctx.message, emoji)
        invalid = False
    except:
        invalid = True

    if invalid:
        await bot.say("That's an invalid string! You need to use an emoji!!\n\n*Using an emoji and it won't work? Make sure it's not Nitro and try a different one.*")
        return

    c.execute("SELECT name FROM emojis WHERE emoji = ?", (emojihex,))
    try:
        r = c.fetchone()[0]
        name = await bot.get_user_info(r)
        await bot.say(name.mention + " is already using that emote :frowning: Try another.")
        conn.close()
        return
    except:
        try:
            c.execute("INSERT INTO emojis (name, emoji) VALUES (?, ?)", (str(ctx.message.author.id), emojihex))
            conn.commit()
            conn.close()
            await bot.say("Signed up " + ctx.message.author.mention + " with emoji " + emoji)
            return
        except:
            c.execute("UPDATE emojis SET emoji = ? WHERE name = ?", (emojihex, ctx.message.author.id))
            conn.commit()
            conn.close()
            await bot.say("Changed " + ctx.message.author.mention + "'s emoji to " + emoji)
            return

#TODO: Move this to it's own file
@bot.command()
async def reset():
    conn = sqlite3.connect("SignedUp.db")
    c = conn.cursor()
    c.execute("DELETE FROM emojis;")
    conn.commit()
    conn.close()
    await bot.say("done :)")




def CreateTable():
    sqlite_file = "SignedUp.db"
    conn = sqlite3.connect("SignedUp.db")
    c = conn.cursor()
    c.execute("CREATE TABLE emojis (name TEXT UNIQUE PRIMARY KEY, emoji TEXT)")