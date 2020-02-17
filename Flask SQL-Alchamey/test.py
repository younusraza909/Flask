import sqlite3

connection=sqlite3.connect("data.db")

cursor=connection.cursor()

create_table="CREATE TABLE users(id int,username text,password text)"

cursor.execute(create_table)

user=(1,"Raza","abcd")
insert_query="INSERT INTO users VALUES(?,?,?)"
cursor.execute(insert_query,user)

users=[
    (2,"wasif","faf"),
    (3,"Farhan","fdads")
]
cursor.executemany(insert_query,users)

select_query="SELECT * FROM users"
for i in cursor.execute(select_query):
    print(i)

connection.commit()

connection.close()    