import sqlite3

#edits the supplied userdata
def editUserData(id, column, value):
	conn = sqlite3.connect(config.databaseName)
	c = conn.cursor()
	c.execute("UPDATE userData SET ? = ? WHERE id = ?", (column, value, id))
	return

#returns users id from id/emoji/nickname
def getId(data):
	data=str(data)
	if data[0] == "<":
		data= data[2:-1]
	conn = sqlite3.connect(config.databaseName)
	c = conn.cursor()
	c.execute("select id from userData where id=? or emoji=? or nickname=?",(data,data,data))
	id = c.fetchone()[0]
	return(id)

#initial setup for database	
def CreateTable():
    sqlite_file = config.databaseName
    conn = sqlite3.connect(config.databaseName)
    c = conn.cursor()
    c.execute("CREATE TABLE emojis (name TEXT UNIQUE PRIMARY KEY, emoji TEXT)")
    c.execute("CREATE TABLE userData (id TEXT UNIQUE PRIMARY KEY, nickname TEXT, emoji TEXT, role TEXT, demonized INTEGER, enchanted INTEGER, protected DATE, powers INTEGER)")
    c.execute("CREATE TABLE seasons (id INTEGER UNIQUE PRIMARY KEY, start DATE, end DATE)")

#reset 'emojis' database
@bot.command()
async def reset():
    print("reset the database")
    conn = sqlite3.connect(config.databaseName)
    c = conn.cursor()
    c.execute("DELETE FROM emojis;")
    conn.commit()
    conn.close()
    await bot.say("done :)")