import discord
import asyncio
from discord.ext import commands
import botobject
import sqlite3
import re
import datetime
import csv
import config

bot = botobject.bot
import utilities
@bot.command(pass_context=True)
async def signup(ctx, emoji):
    try:
        emoji = emoji #check an emoji was provided
    except:
        await bot.say("I'm glad you want to join the game, but the correct syntax for this command is `!signup :emoji:`")
    conn = sqlite3.connect(config.databaseName)
    c = conn.cursor()
    try:
        emojihex = emoji
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
        if name == ctx.message.author:
            await bot.say("You can't sign up again with the same emote, silly! :stuck_out_tongue:\n\n*You have already signed up with that emote*")
        else:
            await bot.say(name.mention + " is already using that emote :frowning: Try another.")
        conn.close()
        return
    except:
        try:
            c.execute("INSERT INTO emojis (name, emoji) VALUES (?, ?)", (str(ctx.message.author.id), emojihex))
            conn.commit()
            conn.close()
            await bot.say("Signed up " + ctx.message.author.mention + " with emoji " + emoji)
            print("Signed up " + ctx.message.author.mention + " with emoji " + emoji)
            return
        except:
            c.execute("UPDATE emojis SET emoji = ? WHERE name = ?", (emojihex, ctx.message.author.id))
            conn.commit()
            conn.close()
            await bot.say("Changed " + ctx.message.author.mention + "'s emoji to " + emoji)
            print("Changed " + ctx.message.author.mention + "'s emoji to " + emoji)
            return

#TODO: Move this to it's own file
@bot.command()
async def reset():
    print("reset the database")
    conn = sqlite3.connect(config.databaseName)
    c = conn.cursor()
    c.execute("DELETE FROM emojis;")
    conn.commit()
    conn.close()
    await bot.say("done :)")
@bot.command()
async def resetRoles():
    print("reset the database")
    conn = sqlite3.connect(config.databaseName)
    c = conn.cursor()
    c.execute("DELETE FROM userData;")
    conn.commit()
    conn.close()
    await bot.say("done :)")
def resetRoles2():
    print("reset the database")
    conn = sqlite3.connect(config.databaseName)
    c = conn.cursor()
    c.execute("DELETE FROM userData;")
    conn.commit()
    conn.close()
@bot.command(pass_context=True)
async def fortuneTeller(ctx,data):
	print("the "+ctx.message.author.mention+" requested to see "+data+"'s role")
	if (datetime.datetime.now().hour < 20 and datetime.datetime.now().hour > 8):
		await bot.say("you can only run that command between 8pm and 8am GMT")
		return
	if not("fortune teller" in [y.name.lower() for y in ctx.message.author.roles]):
		await bot.say("only the @Fortune Teller can use that command")
		return
	else:
		await bot.say(data+"'s role is:......[insert role here]")

@bot.command(pass_context=True)
async def getUser(ctx,data):
	await bot.say(utilities.getId(data))

@bot.command(pass_context=True)
async def startSeason(ctx):
	resetRoles2()
	
	c.execute("INSERT into season (id,start) VALUES (SELECT max(id) + 1 FROM season,?)",(datetime.datetime.now()))
	print("starting the season")
	conn = sqlite3.connect(config.databaseName)
	c = conn.cursor()
	c.execute('SELECT * FROM emojis') 
	role ="innocent"
	for row in c.fetchall():
		row = (list(row))
		c.execute("INSERT INTO userData (id, nickname,emoji,role) VALUES (?, ?, ?, ?)", (row[0],ctx.message.server.get_member(row[0]).display_name ,row[1],role))
	conn.commit()
	conn.close()
	await bot.say("done :)")

def CreateTable():
    sqlite_file = config.databaseName
    conn = sqlite3.connect(config.databaseName)
    c = conn.cursor()
    #c.execute("CREATE TABLE emojis (name TEXT UNIQUE PRIMARY KEY, emoji TEXT)")
    #c.execute("CREATE TABLE userData (id TEXT UNIQUE PRIMARY KEY, nickname TEXT, emoji TEXT, role TEXT, demonized INTEGER, enchanted INTEGER, protected DATE, powers INTEGER)")
    c.execute("CREATE TABLE season (id TEXT UNIQUE PRIMARY KEY, start DATE, end DATE)")
CreateTable()
