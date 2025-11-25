from flask import Flask, render_template
import sql_to_html as query

app = Flask(__name__, template_folder="../templates")

@app.route('/main')
def main():
  return render_template("main.html")

@app.route('/search-results')
def search_results():
  mydb = query.database_connect()
  query.send_query(mydb, "select * FROM products WHERE productLine = \"Motorcycles\";")


  return render_template("main.html")


# Start server
if __name__ == '__main__':
  app.run(debug=True)