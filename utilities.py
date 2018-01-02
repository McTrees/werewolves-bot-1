def editUserData(id, column, value):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	c.execute("UPDATE userData SET ? = ? WHERE id = ?", (column, value, id))
	return

def getId(data):
	data=str(data)
	if data[0] == "<":
		data= data[2:-1]
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	c.execute("select id from userData where id=? or emoji=? or nickname=?",(data,data,data))
	id = c.fetchone()[0]
	return(id)