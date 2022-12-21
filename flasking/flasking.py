import inspect

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

"""
https://youtu.be/9MHYHgh4jYc

HOWTO:

run from commmad line:

flask --app flasking/flasking run
python flasking/flasking.py
"""

app = Flask(__name__)
app.secret_key = "hello world"
app.permanent_session_lifetime = timedelta(minutes=1)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['CORS_ORIGINS'] = ['http://localhost:5000', 'http://127.0.0.1:5000']
app.config['CORS_HEADERS'] = ['Content-Type']

db = SQLAlchemy(app)


class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    _name = db.Column("name", db.String)
    _email = db.Column("email", db.String)

    def __init__(self, name, email):
        self._name = name
        self._email = email


@app.route("/")
# @cross_origin()
def hello_world():
    # return "<p>Hello, World!</p>"
    return render_template("index.html")


@app.route("/home")
# @cross_origin()
def home():
    return f"Hello this this is {inspect.currentframe().f_code.co_name}.\n " \
           f"<h1>home<h1>"


@app.route("/<name>")
def name(name):
    # return f"Hello, {name}!"
    # return render_template("user_old.html", content=name)
    return f"<h1>{name}</h1>"


@app.route('/about')
def about():
    return 'The about page'


@app.route('/admin')
def admin():
    return redirect(url_for("user", name="admin!!!"))
    # return redirect(url_for("about"))


@app.route("/escaped/<name>")
def escaped_name(name):
    return f"Hello, {escape(name)}!"


@app.route("/non-escaped/<name>")
def non_escaped_name(name):
    return f"Hello, {name}!"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form['nm']
        session["user"] = user
        # return redirect(url_for("user", name=user))

        if Users.__:
            pass
        else:
            _user = Users(user, "")
            db.session.add(_user)
            db.commit()

        flash(f"Login successful")
        return redirect(url_for("user"))
    elif request.method == "GET":
        if "user" in session:
            flash(f"User {session.get('user')} already logged in")
            return redirect(url_for("user"))

        return render_template("login.html")

    # if request.method == 'POST':
    #     return do_the_login()
    # else:
    #     return show_the_login_form()


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session.get("user")
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
        elif request.method == "GET":
            if "email" in session:
                email = session.get("email")
        # return f"<h1>{user}</h1>"
        # return render_template("user.html", user=user)
        return render_template("user.html", user=email)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    user = session.get("user")
    session.pop("user", None)
    session.pop("email", None)
    if not session.get("user"):
        if user:
            flash(f"User {user} successfully logged out", "info")
        else:
            flash(f"Already logged out", "info")
    return redirect(url_for("login"))


def do_the_login():
    return f"{inspect.currentframe().f_code.co_name_}"


def show_the_login_form():
    return f"{show_the_login_form.__name__}"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
