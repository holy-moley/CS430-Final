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
        database='lib'
    )
    return mydb

# Test command
def send_query(mydb, command):

    #Get query results and put them in dataframe
    mycursor = mydb.cursor()
    mycursor.execute(command)
    myresult = mycursor.fetchall()
    dataframe = pd.DataFrame(myresult)

    # Get column names and set them in the dataframe
    if not dataframe.empty:
        column_names = [description[0] for description in mycursor.description]
        dataframe.columns = column_names
        html = dataframe.to_html(index=False)
    else:
        dataframe= pd.DataFrame(['No results found!'])
        html = dataframe.to_html(index=False, header=False)

    
    
    # Link to external CSS file for styling
    styled_html = f"""<link rel="stylesheet" href="../style.css">
    {html}"""
    with open('flask/static/query-results/sql-result.html', 'w', encoding='utf-8') as file:
        file.write(styled_html)