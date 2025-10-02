import sqlite3 as s

class HandleDb:
	def __init__(self):
		self.conn = s.connect('rc.db')
		self.cursor = self.conn.cursor()
#		self.createtable()
#		self.register('Alice')
	def createtable(self):
		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS users (
		    id INTEGER PRIMARY KEY AUTOINCREMENT,
		    name TEXT UNIQUE NOT NULL,
		    slot TEXT
		)
		""")
	def register(self, name):
		self.cursor.execute("INSERT OR IGNORE INTO users (name, slot) VALUES (?, ?)", (name, None))
		self.conn.commit()
	def deleteuser(self, name):
		self.cursor.execute("DELETE FROM users WHERE name = ?", (name,))
		self.conn.commit()
	def updateslot(self, name, newslot):
		self.cursor.execute("UPDATE users SET slot = ? WHERE name = ?", (newslot, name))
		self.conn.commit()
	def getslot(self, name):
		self.cursor.execute("SELECT slot FROM users WHERE name = ?", (name,))
		result = self.cursor.fetchone()
		return result[0] if result else None
	def printusers(self):
		self.cursor.execute("SELECT * FROM users")
		rows = self.cursor.fetchall()
		for row in rows: print(row)		
	def printuser(self, name):
		self.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
		rows = self.cursor.fetchall()
		for row in rows: print(row)
	def closedb(self):
		self.conn.commit()
		self.conn.close()
