import sqlite3

with sqlite3.connect("task.db") as db:
    cursor = db.cursor()

#crete "users" table to the db
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
user_ID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
nickname VARCHAR(20) NOT NULL,
password VARCHAR(20) NOT NULL);
''')

#add entity to "users" table
cursor.execute('''
INSERT INTO users(username, nickname, password)
VALUES("admin","boss","admin") 
''')
db.commit()

#print "users" table content 
cursor.execute("SELECT * FROM users")
print (cursor.fetchall())


