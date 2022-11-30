import inspect

from flask import Flask, request, redirect, url_for, render_template
from markupsafe import escape

"""
HOWTO:

run from commmad line:

flask --app flasking/flasking run
python flasking/flasking.py
"""

app = Flask(__name__)

app.config['CORS_ORIGINS'] = ['http://localhost:5000', 'http://127.0.0.1:5000']
app.config['CORS_HEADERS'] = ['Content-Type']


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
def user(name):
    # return f"Hello, {name}!"
    return render_template("user.html", content=name)


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
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


def do_the_login():
    return f"{inspect.currentframe().f_code.co_name_}"


def show_the_login_form():
    return f"{show_the_login_form.__name__}"


if __name__ == "__main__":
    app.run(debug=True)
