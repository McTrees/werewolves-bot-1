#Import libraries
import discord #The Discord API
import asyncio #Used for await and async
from discord.ext import commands #Used to define commands and some other things
import botobject
import sqlite3
import re
import datetime


#Import other dependencies created by Ben
import config
import credentials #The Bot's Secret Key
import botobject
import signup #The Function Which Handles Signing Up
import reactions #Handles adding & removing reactions
import utilities

bot = botobject.bot #import the bot object

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(credentials.BotSecret) #run bot