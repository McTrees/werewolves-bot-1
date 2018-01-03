import discord
import asyncio
from discord.ext import commands
import botobject
import sqlite3
import re
import datetime
import config

bot = botobject.bot
import utilities
@bot.command(pass_context=True)
async def signup(ctx, emoji):
    conn = sqlite3.connect(config.databaseName)
    c = conn.cursor()
    c.execute("select end from seasons where id = (select max(id) FROM seasons)")
    if c.fetchone()!=None:
        c.execute("select end from seasons where id = (select max(id) FROM seasons)")
        s = list(c.fetchone())[0]
        if (s==None):
            await bot.say("The game already started! Signup next season.")
            return
    try:
        emoji = emoji #check an emoji was provided
    except:
        await bot.say("I'm glad you want to join the game, but the correct syntax for this command is `!signup :emoji:`")
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

@bot.command()
async def endSeason():
	conn = sqlite3.connect(config.databaseName)
	c = conn.cursor()
	print("ending the season")
	c.execute("update seasons set end=? where id = (select max(id) FROM seasons)",[datetime.datetime.now()])
	c.execute("DELETE FROM emojis;")
	conn.commit()
	conn.close()
	
@bot.command(pass_context=True)
async def startSeason(ctx):
	resetRoles()
	print("starting the season")
	conn = sqlite3.connect(config.databaseName)
	c = conn.cursor()
	c.execute("DELETE FROM userData;")
	c.execute("INSERT into seasons (start) values(?)",[str(datetime.datetime.now())])
	c.execute('SELECT * FROM emojis') 
	role ="innocent"
	for row in c.fetchall():
		row = (list(row))
		c.execute("INSERT INTO userData (id, nickname,emoji,role) VALUES (?, ?, ?, ?)", (row[0],ctx.message.server.get_member(row[0]).display_name ,row[1],role))
	conn.commit()
	conn.close()
	await bot.say("done :)")