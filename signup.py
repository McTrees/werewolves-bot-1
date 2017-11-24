import discord
import asyncio
from discord.ext import commands
import botobject
import sqlite3

bot = botobject.bot
        
@bot.command(pass_context=True)
async def signup(ctx, emoji):
    try:
        emoji = emoji #check an emoji was provided
    except:
        await bot.say("I'm glad you want to join the game, but the correct syntax for this command is `!signup :emoji:`")
    conn = sqlite3.connect("SignedUp.db")
    c = conn.cursor()
    emojihex = hex(ord(emoji))
    c.execute("SELECT name FROM emojis WHERE emoji = ?", (emojihex,))
    try:
        r = c.fetchone()[0]
        r = await bot.get_member(r)
        await bot.say("Another user is already using that emote :frowning: Try another.")
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
            await bot.say("Seems like you're already signed up, or something went wrong!")
            conn.close()
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