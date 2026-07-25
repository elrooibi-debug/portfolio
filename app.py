from flask import Flask, render_template, request, session, url_for, redirect
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

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")

@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/login', methods= ['GET', 'POST'] )
def login():
    form = LoginForm()
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        cursor.execute( 'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))

        account = cursor.fetchone()

        if account: 
            session['loggedin'] = True
            session['id_user'] = account[0]
            session['username'] = account[1]
            return render_template('index.html', msg = 'Logged successfully')
        else:
            msg = 'Incorrect username or password,try again'

    return render_template('login.html', title="Sign in", msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id_user', None)
    session.pop('username', None)
    return redirect(url_for('login'))





@app.route('/learning')
def learning():
    if 'loggedin' not in session: 
        return redirect(url_for('login'))
    return render_template('learning.html', title="Learning")


@app.route('/projects')
def projects():
    if 'loggedin' not in session: 
        return redirect(url_for('login'))
    return render_template('projects.html', title="Projects")




@app.route('/habits', methods=['GET', 'POST'])
def habits():
    

    if 'loggedin' not in session: 
        return redirect(url_for('login'))
    
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

        return redirect(url_for('habits'))
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM habits')
    habitude = cursor.fetchall()
    cursor.close()
        
    return render_template('habits.html', title= "Habits tracker" , habitudes = habitude)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)