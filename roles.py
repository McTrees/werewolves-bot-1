import botobject

bot = botobject.bot #import the bot object
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
