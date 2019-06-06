import os, requests


from flask import Flask, session, render_template, request, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('login.html', error=0)
    else:
        username = request.form.get("login")
        password = request.form.get("password")
        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
                      {"username": username, "password": password}).rowcount == 0:
            return render_template('login.html', error=1)

        # Session
        row = db.execute("SELECT id FROM users WHERE username = :username AND password = :password",
                            {"username": username, "password": password}).fetchone()
        userID = row["id"]
        session['userID'] = userID

        row = db.execute("SELECT username FROM users WHERE id = :id", {"id": session['userID']}).fetchone()
        loged = row['username']

        return render_template("search.html", loged=loged)

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if (not username or not password) or (not username and not password) or (' ' in username or ' ' in password):
            return render_template("signup.html", error=1)

        elif db.execute("SELECT * FROM users WHERE username = :username",
                          {"username": username}).rowcount != 0:

            return render_template("signup.html", error=1)

        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username,
                                                                                            "password": password})
        db.commit()

        return render_template('login.html')


@app.route("/searching", methods=["POST"])
def searching():
    requested_book = request.form.get("search")
    row = db.execute("SELECT username FROM users WHERE id = :id", {"id": session['userID']}).fetchone()
    loged = row['username']

    if db.execute("SELECT * FROM books WHERE isbn LIKE :string OR title LIKE :string OR author LIKE :string OR year LIKE :string",
                  {"string": f"%{requested_book}%"}).fetchall():

        books = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn LIKE :string OR title LIKE :string OR author LIKE :string OR year LIKE :string",
                  {"string": f"%{requested_book}%"})

        return render_template("search.html", books=books, loged=loged)

    return render_template("search.html", message=1, loged=loged)

@app.route("/book_page/<string:isbn>", methods=["GET", "POST"])
def book_page(isbn):
    row = db.execute("SELECT username FROM users WHERE id = :id", {"id": session['userID']}).fetchone()
    loged = row['username']

    row = db.execute("SELECT title FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    title = row['title']
    row = db.execute("SELECT author FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    author = row['author']
    row = db.execute("SELECT year FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    year = row['year']


    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "Kb1Izh2O79dR9Po6CJmvA", "isbns": isbn})

    res = res.json()
    work_ratings_count = res["books"][0]["work_ratings_count"]
    average_rating = res["books"][0]["average_rating"]


    reviews = db.execute("SELECT rating, review, username FROM reviews WHERE isbn = :b", {"b": isbn}).fetchall()



    return render_template("book_page.html", loged=loged, isbn=isbn, title=title, author=author, year=year,
                           work_ratings_count=work_ratings_count, average_rating=average_rating, reviews=reviews)


@app.route("/book_page_commented/<string:isbn>", methods=["GET", "POST"])
def book_page_commented(isbn):
    row = db.execute("SELECT username FROM users WHERE id = :id", {"id": session['userID']}).fetchone()
    loged = row['username']


    #
    row = db.execute("SELECT title FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    title = row['title']
    row = db.execute("SELECT author FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    author = row['author']
    row = db.execute("SELECT year FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    year = row['year']

    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "Kb1Izh2O79dR9Po6CJmvA", "isbns": isbn})

    res = res.json()
    work_ratings_count = res["books"][0]["work_ratings_count"]
    average_rating = res["books"][0]["average_rating"]

    reviews = db.execute("SELECT review, rating, username FROM reviews WHERE isbn = :b", {"b": isbn}).fetchall()
    #

    rating = request.form.get("rate")
    comment = request.form.get("comment")
    if db.execute("SELECT review FROM reviews WHERE username = :username AND isbn = :isbn", {"username": loged, "isbn": isbn}).rowcount >= 1:
        return render_template("book_page.html", loged=loged, isbn=isbn, title=title, author=author, year=year,
                           work_ratings_count=work_ratings_count, average_rating=average_rating, reviews=reviews, error=1)


    db.execute("INSERT INTO reviews (isbn, review, rating, username) VALUES (:isbn, :review, :rating, :username)",
               {"isbn": isbn, "review": comment, "rating": rating, "username": loged})
    db.commit()



    row = db.execute("SELECT title FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    title = row['title']
    row = db.execute("SELECT author FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    author = row['author']
    row = db.execute("SELECT year FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    year = row['year']


    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "Kb1Izh2O79dR9Po6CJmvA", "isbns": isbn})

    res = res.json()
    work_ratings_count = res["books"][0]["work_ratings_count"]
    average_rating = res["books"][0]["average_rating"]


    reviews = db.execute("SELECT review, username FROM reviews WHERE isbn = :b", {"b": isbn}).fetchall()



    return render_template("book_page.html", loged=loged, isbn=isbn, title=title, author=author, year=year,
                           work_ratings_count=work_ratings_count, average_rating=average_rating, reviews=reviews)

@app.route("/api/<string:isbn>", methods=["GET"])
def isbn_api(isbn):

    if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).rowcount != 1:
        return abort(404)

    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "Kb1Izh2O79dR9Po6CJmvA", "isbns": isbn})

    res = res.json()
    work_ratings_count = res["books"][0]["work_ratings_count"]
    average_rating = res["books"][0]["average_rating"]


    response = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

    return jsonify(
        title = response["title"],
        author = response["author"],
        year = response["year"],
        isbn = isbn,
        review_count = work_ratings_count,
        average_score = average_rating
    )