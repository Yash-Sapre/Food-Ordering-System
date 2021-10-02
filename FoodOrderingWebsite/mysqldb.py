import mysql.connector

db = mysql.connector.connect(host="localhost",user="root",password="root123")
dbCursor = db.cursor()


# init_db is responsible for creating the database and its respective tables
def init_db():
    dbCursor.execute('CREATE DATABASE COUNTER')
    dbCursor.execute('USE COUNTER')
    dbCursor.execute('CREATE TABLE USER (user_id INT AUTO_INCREMENT PRIMARY KEY ,'
                     'username VARCHAR(100),password VARCHAR(100),email VARCHAR(100))')
    
    dbCursor.execute('CREATE TABLE CUSTOMER (customer_id INT AUTO_INCREMENT PRIMARY KEY ,customer_name VARCHAR(100))')
    dbCursor.execute('CREATE TABLE CUSTOMER_ORDER (order_id INT, food_id INT,customer_id INT,count INT,status BOOLEAN)')
    dbCursor.execute('CREATE TABLE ADMIN(username varchar(20),password varchar(100))')
    dbCursor.execute('CREATE TABLE FOOD (food_id INT AUTO_INCREMENT PRIMARY KEY,food_name VARCHAR(100),price INT,food_img BLOB NULL)')

'''
Executing show databases 
Fetching all database names
Checking for the presence of COUNTER database
if no : create database with tables and use COUNTER
else : use COUNTER
'''
dbCursor.execute('SHOW DATABASES')
db_list = dbCursor.fetchall()

if ('counter',) in db_list:
    print('DB present')
    dbCursor.execute('USE COUNTER')
else:
    print('DB not present')
    print('CREATING DATABASE COUNTER')
    init_db()
    dbCursor.execute('USE COUNTER')



