import discord #Interacts with the discord API
import asyncio #Async
from discord.ext import commands #Used for the commands.bot

description = "Ben made it"

bot = commands.Bot(command_prefix='!', description=description) #Create the bot

