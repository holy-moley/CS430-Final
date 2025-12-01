import mysql.connector
import pandas as pd

# Connect to database hosted on local machine
def database_connect():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='peepy',
        port=3306,
        database='lib'
    )
    return mydb

# -------------------------
# User Registration
# -------------------------
def register_user(mydb, name, email):
    """Insert a new user safely using parameterized query."""
    if not name or not email:
        return "All fields are required."

    try:
        cursor = mydb.cursor()
        query = "INSERT INTO Users (Name, Email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        mydb.commit()
        cursor.close()
        return "User registered successfully!"
    except mysql.connector.Error as err:
        return f"Database error: {err}"

# -------------------------
# Checkout / Checkin
# -------------------------
def checkout_item(mydb, item_id, borrower_id, item_type):
    cursor = mydb.cursor()
    if item_type == "book":
        table = "Books"
        checkout_table = "book_checkouts"
        id_col = "BookID"
        available_col = "BookAvailable"
    else:
        table = "Movies"
        checkout_table = "movie_checkouts"
        id_col = "MovID"
        available_col = "MovAvailable"

    try:
        # Check availability
        cursor.execute(f"SELECT {available_col} FROM {table} WHERE {id_col} = %s", (item_id,))
        result = cursor.fetchone()
        if not result:
            return "Item ID not found."
        if result[0] < 1:
            return "No copies available."

        # Insert checkout
        cursor.execute(f"INSERT INTO {checkout_table} (idUsers, {id_col}, CheckoutDate) VALUES (%s, %s, CURDATE())", (borrower_id, item_id))
        # Decrement available count
        cursor.execute(f"UPDATE {table} SET {available_col} = {available_col} - 1 WHERE {id_col} = %s", (item_id,))
        mydb.commit()
        cursor.close()
        return "Checked out successfully!"
    except mysql.connector.Error as err:
        mydb.rollback()
        return f"Database error: {err}"

def checkin_item(mydb, item_id, borrower_id, item_type):
    cursor = mydb.cursor()
    if item_type == "book":
        table = "Books"
        checkout_table = "book_checkouts"
        id_col = "BookID"
        available_col = "BookAvailable"
    else:
        table = "Movies"
        checkout_table = "movie_checkouts"
        id_col = "MovID"
        available_col = "MovAvailable"

    try:
        # Find matching checkout
        cursor.execute(f"SELECT CheckoutID FROM {checkout_table} WHERE {id_col} = %s AND idUsers = %s AND ReturnDate IS NULL", (item_id, borrower_id))
        result = cursor.fetchone()
        if not result:
            return "No matching checkout found."

        checkout_id = result[0]
        # Update checkout return
        cursor.execute(f"UPDATE {checkout_table} SET ReturnDate = CURDATE() WHERE CheckoutID = %s", (checkout_id,))
        # Increment available count
        cursor.execute(f"UPDATE {table} SET {available_col} = {available_col} + 1 WHERE {id_col} = %s", (item_id,))
        mydb.commit()
        cursor.close()
        return "Checked in successfully!"
    except mysql.connector.Error as err:
        mydb.rollback()
        return f"Database error: {err}"

# Search through movies/books
def search_items(mydb, title, exclude=None, available=None):
    cursor = mydb.cursor(dictionary=True)
    queries = []

    if exclude != "No Books":
        queries.append("SELECT BookID AS ID, BookTitle AS Title, BookYear AS Year, BookGen AS Genre, BookAuthor AS Creator, BookForm AS Media, BookAvailable AS Available FROM Books")
    if exclude != "No Movies":
        queries.append("SELECT MovID AS ID, MovTitle AS Title, MovYear AS Year, MovGen AS Genre, MovDir AS Creator, MovForm AS Media, MovAvailable AS Available FROM Movies")

    if not queries:
        return []

    union_query = " UNION ".join(queries)
    sql = f"SELECT * FROM ({union_query}) AS combined WHERE Title LIKE %s"
    params = [f"%{title}%"]
    if available == "Available":
        sql += " AND Available > 0"

    cursor.execute(sql, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    return rows

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
    """
    Search books/movies based on title, type, and availability,
    write results to 'sql-result.html'.
    """
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

        else:  # Both books and movies
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

        # Prevent SQL injection
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        # Convert to DataFrame
        import pandas as pd
        df = pd.DataFrame(rows)
        if not df.empty:
            df.columns = rows[0].keys()
            html = df.to_html(index=False)
        else:
            html = pd.DataFrame(['No results found!']).to_html(index=False, header=False)

        # Write HTML file for JS to fetch
        styled_html = f"""<link rel="stylesheet" href="../style.css">{html}"""
        with open('flask/static/query-results/sql-result.html', 'w', encoding='utf-8') as f:
            f.write(styled_html)

    finally:
        cursor.close()

