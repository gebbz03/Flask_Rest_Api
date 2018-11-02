import sqlite3


connection=sqlite3.connect('data.db')

cursor=connection.cursor()

create_table="CREATE TABLE users(id int,username text,password text)"
cursor.execute(create_table)

user=(1,'gebbz','gebbz4ever')
insert_query="INSERT INTO users values(?,?,?)"
cursor.execute(insert_query,user)

users=[
    (2,'gebbz2','gebbz4ever2'),
    (3,'gebbz23','gebbz4ever3')
]

cursor.executemany(insert_query,users)

select_query="SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)


connection.commit()
connection.close()

#delete data.db every run