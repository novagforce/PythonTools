import mysql.connector
from pymongo import MongoClient

mysqlconfig={'host':'127.0.0.1',
        'user':'root',
        'password':'root',
        'port':3306 ,
        'database':'finance',
        }
try:
    mongoClient=MongoClient()
    db=mongoClient.finance
    con=mysql.connector.connect(**mysqlconfig)
    cursor=con.cursor(True)
    
    cursor.execute("SELECT* FROM expense")
    des=""
    for i in range(len(cursor.description)):
        des=des+cursor.description[i][0]+","
        print(cursor.description[i][1])
    print(des)
    for tup in cursor:
        tupMap={}
        for i in range(len(tup)):
            tupMap[cursor.description[i][0]]=tup[i]
        print(tupMap)
        db.expense.insert(tupMap)
except mysql.connector.Error as e:
    print('connect fails!{}'.format(e))