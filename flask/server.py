from flask import Flask, render_template, request
import sql_to_html as query

app = Flask(__name__, template_folder="../templates", static_folder="static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

mydb = None

def startup():
    global mydb
    mydb = query.database_connect()

# Main
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        exclude = request.form.get('exclude', 'Books and Movies')
        available = request.form.get('available', '')

        # Call the new search_items function
        query.search_items(mydb, title, exclude, available)

    return render_template("main.html")


# Checkout/in form
@app.route('/checkform', methods=['GET', 'POST'])
def checkForm():
    outputResult = ""
    if request.method == 'POST':
        if 'submitBtnOut' in request.form:
            item_id = request.form.get('itemIDOut')
            borrower_id = request.form.get('borrowerIDOut')
            item_type = request.form.get('itemTypeOut')
            if item_type == "book":
                procedureName = "checkout_book"
            else:
                procedureName = "checkout_movie"
        elif 'submitBtnIn' in request.form:
            item_id = request.form.get('itemIDIn')
            borrower_id = request.form.get('borrowerIDIn')
            item_type = request.form.get('itemTypeIn')
            if item_type == "book":
                procedureName = "checkin_book"
            else:
                procedureName = "checkin_movie"
        procedureParams = [item_id, borrower_id]
        outputResult = query.call_procedure(mydb, procedureName, procedureParams)
    return render_template("form.html", output=outputResult)

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = query.register_user(mydb, name, email)
    return render_template("register.html", message=message)

# Checkout display page
@app.route('/checkouts')
def checkouts():
    book_rows = query.get_book_checkouts(mydb)
    movie_rows = query.get_movie_checkouts(mydb)
    return render_template("checkouts.html", book_rows=book_rows, movie_rows=movie_rows)

# Home redirect
@app.route('/')
def home():
    return render_template("main.html")

# Start server
if __name__ == '__main__':
    startup()
    app.run(debug=True)
