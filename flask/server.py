from ast import Constant
from flask import Flask, redirect, request, render_template, url_for
import sql_to_html as query

app = Flask(__name__, template_folder="../templates")
mydb = None

def startup():
  global mydb
  mydb = query.database_connect()

#Main page logic
@app.route('/', methods=['GET','POST'])
def main():
  
  if request.method == 'POST':
    title = request.form.get('title')
    exclude = request.form.get('exclude')
    available = request.form.get('available')

    #Query based on filters
    if available == 'Available':
      availablequery = " AND Available > 0"
    else:
      availablequery = ""

    if exclude == 'No Books':
      queryString =  """
                      SELECT * 
                      FROM(
                      SELECT 
                      MovID as ID, MovTitle as Title, MovYear as Year, MovGen as Genre, 
                      MovDir as Creator, MovForm as Media, MovAvailable as Available
                      FROM Movies) as movieTable
                      WHERE Title LIKE '%"""+ title +"%'" + availablequery + ";"
    elif exclude == 'No Movies':
      queryString =  """
                      SELECT * 
                      FROM(
                      SELECT 
                      BookID as ID, BookTitle as Title, BookYear as Year, BookGen as Genre, BookAuthor as Creator, 
                      BookForm as Media, BookAvailable as Available 
                      FROM Books) as bookTable
                      WHERE Title LIKE '%"""+ title +"%'" + availablequery + ";"
    else:
      queryString =  """
                      SELECT * 
                      FROM(
                      SELECT 
                      BookID as ID, BookTitle as Title, BookYear as Year, BookGen as Genre, BookAuthor as Creator, 
                      BookForm as Media, BookAvailable as Available 
                      FROM Books
                      UNION
                      SELECT
                      MovID as ID, MovTitle as Title, MovYear as Year, MovGen as Genre, 
                      MovDir as Creator, MovForm as Media, MovAvailable as Available
                      FROM Movies) AS unionTable
                      WHERE Title LIKE '%"""+ title +"%'" + availablequery + ";"
    
    query.send_query(mydb, queryString)
  
  return render_template("main.html")


@app.route('/checkform', methods=['GET','POST'])
def checkForm():
  if request.method == 'POST':
    formOut = request.form.get('submitBtnOut')
    if formOut == 'Check out!':
      itemID = request.form.get('itemIDOut')
      borrowerID = request.form.get('borrowerIDOut')
      """
      if "B" in itemID:
       queryString = 
      else:
        queryString = 
        """
    else:
      itemID = request.form.get('itemIDIn')
      borrowerID = request.form.get('borrowerIDIn')
      """
      if "B" in itemID:
        queryString = 
      else:
        queryString = 
      """


    query.send_query(mydb, queryString)
  return render_template("form.html")

# Start server
if __name__ == '__main__':
  startup()
  app.run(debug=True)