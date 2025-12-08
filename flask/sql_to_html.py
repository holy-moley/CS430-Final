import mysql.connector
import pandas as pd

# Connect to database on local machine
def database_connect():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='enderman',
        port=3306,
        database='lib'
    )
    return mydb


def register_user(mydb, name, email):
    if not name or not email:
        return "Must enter name and email!"

    try:
        mycursor = mydb.cursor()
        query = "INSERT INTO Users (name, email) VALUES (%s, %s)"
        mycursor.execute(query, (name, email))
        mydb.commit()
        mycursor.close()
        return "User registered successfully!"
    except mysql.connector.Error as error:
        return "There was an error registering the user!"

def call_procedure(mydb, procedureName, procedureParams):
    mycursor = mydb.cursor()
    try:
        mycursor.callproc(procedureName, procedureParams)
        mydb.commit()
        for result in mycursor.stored_results():
                result.fetchall()
        mycursor.execute('SELECT @outputMsg')
        return mycursor.fetchone()[0]
        #cursor.close()
    except mysql.connector.Error as error:
        mydb.rollback()
        return "An ID you entered was invalid!"

# Get checkouts
def get_book_checkouts(mydb):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM book_checkouts")
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_movie_checkouts(mydb):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movie_checkouts")
    rows = cursor.fetchall()
    cursor.close()
    return rows

#search
def search_items(mydb, title, exclude, available):
    cursor = mydb.cursor(dictionary=True)

    title = title.strip() if title else ""

    try:
        if exclude == 'No Books':
            query = """
                SELECT MovID as ID, MovTitle as Title, MovYear as Year, MovGen as Genre,
                       MovDir as Creator, MovForm as Media, MovAvailable as Available
                FROM Movies
                WHERE MovTitle LIKE %s
            """
            params = (f"%{title}%",)
            if available == "Available":
                query += " AND MovAvailable > 0"

        elif exclude == 'No Movies':
            query = """
                SELECT BookID as ID, BookTitle as Title, BookYear as Year, BookGen as Genre,
                       BookAuthor as Creator, BookForm as Media, BookAvailable as Available
                FROM Books
                WHERE BookTitle LIKE %s
            """
            params = (f"%{title}%",)
            if available == "Available":
                query += " AND BookAvailable > 0"

        else: 
            query = """
                SELECT BookID as ID, BookTitle as Title, BookYear as Year, BookGen as Genre,
                       BookAuthor as Creator, BookForm as Media, BookAvailable as Available
                FROM Books
                WHERE BookTitle LIKE %s
            """
            params = [f"%{title}%"]
            if available == "Available":
                query += " AND BookAvailable > 0"

            query += """
                UNION
                SELECT MovID as ID, MovTitle as Title, MovYear as Year, MovGen as Genre,
                       MovDir as Creator, MovForm as Media, MovAvailable as Available
                FROM Movies
                WHERE MovTitle LIKE %s
            """
            params.append(f"%{title}%")
            if available == "Available":
                query += " AND MovAvailable > 0"

        #Stop injection
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        #Convert to HTML
        df = pd.DataFrame(rows)
        if not df.empty:
            df.columns = rows[0].keys()
            html = df.to_html(index=False)
        else:
            html = pd.DataFrame(['No results found!']).to_html(index=False, header=False)

        #Style HTML and save it
        styled_html = f"""<link rel="stylesheet" href="../style.css">{html}"""
        with open('flask/static/query-results/sql-result.html', 'w', encoding='utf-8') as f:
            f.write(styled_html)

    finally:
        cursor.close()

