import sqlite3
db=sqlite3.connect("./english.db")
with open('new.sql','r') as f:
	db.cursor().executescript(f.read())
	db.commit()
