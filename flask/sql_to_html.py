import os
import pandas as pd
import mysql.connector


# Connect to database hosted on local machine
def database_connect():
    mydb = mysql.connector.connect (
        host='localhost',
        user='root',
        password='enderman',
        port=3306,
        database='classicmodels'
    )
    return mydb

# Test command
def send_query(mydb, command):
    # command = "select * FROM customers WHERE city = \"Nantes\";"

    mycursor = mydb.cursor()
    mycursor.execute(command)
    myresult = mycursor.fetchall()

    dataframe = pd.DataFrame()
    for i in myresult:
        dataframe2 = pd.DataFrame(list(i)).T
        dataframe = pd.concat([dataframe, dataframe2])

    dataframe.to_html('static/query-results/sql-result.html')