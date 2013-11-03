#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import hashlib
# Import the SQLite3 module
import sqlite3 #Importing the library
from datetime import date, datetime

__author__ = 'coderz'

try:
  db = sqlite3.connect(':memory:')
  c = db.cursor()
  cur = db.cursor()
  cur.execute('SELECT SQLITE_VERSION()')
  data = cur.fetchone()
  print "SQLite version: %s" % data
  c.execute('''CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, phone TEXT)''')
  users = [
    ('John', '5557241'),
    ('Adam', '5547874'),
    ('Jack', '5484522'),
    ('Monthy',' 6656565')
  ]
  #Insert Multiple Rows with SQLite’s executemany
  c.executemany('''INSERT INTO users(name, phone) VALUES(?,?)''', users)
  db.commit()

  # Print the users
  c.execute('''SELECT * FROM users''')
  for row in c:
     print(row)

  db.close()
except sqlite3.Error, e:
  print "Error %s:" % e.args[0]
  sys.exit(1)
finally:
    if db:
        db.close()


#Execute SQL File with SQLite’s executescript
#db = sqlite3.connect(':memory:')
#c = db.cursor()
#datas=[('John', '5557241'),('Adam', '5547874'), ('Jack', '5484522')]
#script = '''CREATE TABLE if not exist users(id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
#        CREATE TABLE accounts(id INTEGER PRIMARY KEY, description TEXT);'''
#c.executescript(script)

# Print the results
#c.execute('''SELECT * FROM users''')
#for row in c:
#    print(row)
#
#db.close()


def encrypt_password(password):
    # Do not use this algorithm in a real environment
    encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
    return encrypted_pass

db = sqlite3.connect(':memory:')
# Register the function
db.create_function('encrypt', 1, encrypt_password)
c = db.cursor()
fd = open('myscript.sql', 'r')
script = fd.read()
c.executescript(script)
fd.close()


c.execute('''CREATE TABLE users(id INTEGER PRIMARY KEY, email TEXT, password TEXT)''')
user = ('johndoe@example.com', '12345678')
c.execute('''INSERT INTO users(email, password) VALUES (?,encrypt(?))''', user)


try:
    con = sqlite3.connect('test.db')
    cur = con.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS Cars;
        CREATE TABLE Cars(OID INTEGER PRIMARY KEY autoincrement NOT NULL ,Id INT, Name TEXT, Price INT);
        INSERT INTO Cars(Id,Name,Price) VALUES(1,'Audi',52642);
        INSERT INTO Cars (Id,Name,Price) VALUES(2,'Mercedes',57127);
        INSERT INTO Cars (Id,Name,Price) VALUES(3,'Skoda',9000);
        INSERT INTO Cars (Id,Name,Price) VALUES(4,'Volvo',29000);
        INSERT INTO Cars (Id,Name,Price) VALUES(5,'Bentley',350000);
        INSERT INTO Cars (Id,Name,Price) VALUES(6,'Citroen',21000);
        INSERT INTO Cars (Id,Name,Price) VALUES(7,'Hummer',41400);
        INSERT INTO Cars (Id,Name,Price) VALUES(8,'Volkswagen',21600);
        """)

    con.commit()
    lid = cur.lastrowid
    print lid
    print "The last Id of the inserted row is " , lid

#Parameterized queries
#  cur.execute("UPDATE Cars SET Price=? WHERE Id=?", (uPrice, uId))
#  cur.execute("SELECT Name, Price FROM Cars WHERE Id=:Id",   {"Id": uId})
#Metadata
#cur.execute('PRAGMA table_info(Cars)')

#Export and import of data
#    data = '\n'.join(con.iterdump())

except sqlite3.Error, e:

    if con:
        con.rollback()
    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()



##################################
# sqlite3 operations
##################################
db_name='mydb.db'
if os.path.exists(db_name) and os.path.isfile(db_name):
    #remove old db
    os.remove(db_name)

# Create a database in RAM
dbmem = sqlite3.connect(':memory:')
##cx = sqlite3.connect(':memory:')


def readData():
    f = open('cars.sql', 'r')
    with f:
        data = f.read()
        return data

try:
  #Connecting to the database
  con = sqlite3.connect(db_name)
  cur = con.cursor()
  #Create a Table
  cur.execute('''CREATE TABLE if not exists log_filter
            ( id integer primary key autoincrement NOT NULL,
            oid integer,
            htype VARCHAR(16),
            reason varchar(128),
            type varchar(16),
            session_id integer,
            name varchar(128) )''')
  con.commit()

  #INSERT Operation
  cur.execute('INSERT INTO log_filter ( oid, htype,reason,type,session_id) VALUES(234, "rh", "nem","FULL",25)')
  cur.execute('INSERT INTO log_filter ( oid, htype,reason,type,session_id) VALUES(2134, "BB", "nem","FULL",25)')
  cur.execute('''INSERT INTO log_filter(oid, htype, reason, type,session_id)
                  VALUES(?,?,?,?,?)''', (2134, "BB", "olol","FULL",235))
  cur.execute('''INSERT INTO log_filter(oid, htype,reason,type,session_id)
                  VALUES(?,?,?,?,?)''', (2134, "BB", "olol","PART",235))

  cars = (
    (1, 'Audi', 52643),
    (2, 'Mercedes', 57642),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Hummer', 41400),
    (7, 'Volkswagen', 21600))
  #cur.executemany("INSERT INTO log_filter VALUES(?, ?, ?,?)", cars)

  sql = ""#readData()
  cur.executescript(sql)

  con.commit()
  print cur.lastrowid
  cur.execute('SELECT * FROM log_filter')
  col_names = [cn[0] for cn in cur.description]
  rows=cur.fetchall()
  print "%10s %10s %10s %10s" % (col_names[1], col_names[2], col_names[3],col_names[4])

  for row in rows:
        print "%10s %10s %10s %10s" % (row[1], row[2], row[3],row[4])
  con.commit()

  #Querying the database
  #record = cur.fetchone()
  #while record:
  #  print record
  #  record = cur.fetchone()

  #retrive data with conditions, use again the “?” placeholder
  #cursor.execute('''SELECT name, email, phone FROM users WHERE id=?''', (user_id,))

  #fetchall method to return all of the records into a list.
  cur.execute("SELECT count(*) FROM log_filter WHERE type='table'")
  rows = cur.fetchall()
  for row in rows:
      print row[0]

  #Using Python variables inside SQL
  #current_experiment = 'Teleportation'
  #cur.execute("SELECT * FROM Experiment WHERE Project = ?", (current_experiment,))


  #newphone = '3113093164'
  #userid = 1
  #cursor.execute('''UPDATE users SET phone = ? WHERE id = ? ''',(newphone, userid))

  #Modifying a database
  #conn.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
  #cur.execute("INSERT INTO Experiment VALUES ('gimli', 'TrollKilling', '1', 112, '1954-07-21')")
  #cu.execute("update catalog set name='name2' where id = 0")
  #con.commit()

  #Execute commands across many values
  #cur.executemany("INSERT INTO Experiment VALUES (?, ?, ?, ?, ?)", new_data_records)


  #SQLite Row Factory and Data Types
  #db.row_factory = sqlite3.Row
  #cursor = db.cursor()
  #cursor.execute('''SELECT name, email, phone FROM users''')
  #for row in cursor:
  #  print('{0} : {1}, {2}'.format(row['name'], row['email'], row['phone']))
  #db.close()


  db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
  c = db.cursor()
  c.execute('''CREATE TABLE example(id INTEGER PRIMARY KEY, created_at timestamp)''')

  # Insert a date object into the database
  #today = date.today()
  #c.execute('''INSERT INTO example(created_at) VALUES(?)''', (today,))
  now = datetime.now()
  c.execute('''INSERT INTO example(created_at) VALUES(?)''', (now,))
  db.commit()

  # Retrieve the inserted object
  c.execute('''SELECT created_at FROM example''')
  row = c.fetchone()
  print('The date is {0} and the datatype is {1}'.format(row[0], type(row[0])))

  # The date is 2013-04-14 and the datatype is <class 'str'>
  db.close()

except sqlite3.Error, e:
    if con:
        con.rollback()
    print "Error %s:" % e.args[0]
    sys.exit(1)
finally:
    if con:
        con.close()

