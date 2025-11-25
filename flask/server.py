from flask import Flask, redirect, request, render_template, url_for
import sql_to_html as query

app = Flask(__name__, template_folder="../templates")

@app.route('/', methods=['GET','POST'])
def main():
  if request.method == 'POST':
    title = request.form['title']
    mydb = query.database_connect()
    query.send_query(mydb, """
                    SELECT * 
                    FROM(
                    SELECT 
                    BookTitle as Title, BookYear as YearMade, BookGen as Genre, BookAuthor as Creator, 
                    BookForm as Media, BookAvailable as Available 
                    FROM Books
                    UNION
                    SELECT
                    MovTitle as Title, MovYear as YearMade, MovGen as Genre, 
                    MovDir as Creator, MovForm as Media, MovAvailable as Available
                    FROM Movies) AS unionTable
                    WHERE Title LIKE '%"""+ title +"%';")
  
  return render_template("main.html")


# Start server
if __name__ == '__main__':
  app.run(debug=True)