from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator

app = Flask(__name__)
nav = Nav(app)

nav.register_element('my_navbar',
                     Navbar('thenav',
                            View('Home Page', 'index'),
                            View('Items', 'item', item=1),
                            Link('Google', 'https://www.google.com'),
                            Separator(),
                            Text('Sea shell'),
                            Subgroup('Extras',
                                     Link('Yahoo', "https://www.yahoo.com"),
                                     View('Indices', 'indices', index=999))
                            )
                     )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/items/<item>')
def item(item):
    return f'<h1> THE ITEM PAGE!! THE ITEM IS: {item}'


@app.route('/indices/<index>')
def indices(index):
    return f'<h1> THE INDEX PAGE!! THE INDEX IS: {index}'


if __name__ == '__main__':
    app.run(debug=True)
