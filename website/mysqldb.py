import mysql.connector

db = mysql.connector.connect(host="localhost",user="root",password="Amoeba!23")

print(db)
dbCursor = db.cursor()


def init_db():
    dbCursor.execute('CREATE DATABASE UNIVERSITY')
    dbCursor.execute('USE UNIVERSITY')
    dbCursor.execute('CREATE TABLE USER (user_id INT AUTO_INCREMENT PRIMARY KEY ,username VARCHAR(100),password VARCHAR(100),email VARCHAR(100))')

dbCursor.execute('USE UNIVERSITY')

