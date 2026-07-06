from flask import Flask, render_template
from config import Config

from forms import LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] ="you-will-never-guess"

app.config.from_object(Config)

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', title = "Home")


@app.route('/learning')
def learning():
    return render_template('learning.html', title = "Learning")


@app.route('/projects')
def projects():
    return render_template('projects.html', title = "Projects")



@app.route('/about')
def about():
    return render_template('about.html', title = "About")

@app.route('/habits')
def habits():
    return render_template('habits.html', title = "Habits")

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Sign in", form = form)


