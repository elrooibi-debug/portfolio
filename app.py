from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from config import Config
from forms import LoginForm

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = "you-will-never-guess"
app.config.from_object(Config)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projet_portfolio'

mysql = MySQL(app)


# Routes
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")


@app.route('/learning')
def learning():
    return render_template('learning.html', title="Learning")


@app.route('/projects')
def projects():
    return render_template('projects.html', title="Projects")


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/habits', methods=['GET', 'POST'])
def habits():
    if request.method == 'POST':
        name = request.form['name']
        times = request.form['times']
        done = request.form['done']
        goal = request.form['goal']
        
        cursor = mysql.connection.cursor()
        
        cursor.execute(
            ''' INSERT INTO habits (Habits, Done, Times, Goal) VALUES (%s, %s, %s, %s) ''',
            (name, done, times, goal)
        )
        mysql.connection.commit()
        cursor.close()
        
        return "Done!!"
    
    return render_template('habits.html', title="Habits")


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Sign in", form=form)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)