from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL
from config import Config
from forms import LoginForm
from datetime import datetime

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        cursor.close()

        if account: 
            session['loggedin'] = True
            session['id_user'] = account['id_user']
            session['username'] = account['username']
            return render_template('index.html', msg='Logged successfully')
        else:
            msg = 'Incorrect username or password, try again'

    return render_template('login.html', title="Sign in", msg=msg)


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

    show_form = (request.args.get('action') == 'add')
    today_date = datetime.now().strftime('%Y-%m-%d')
    current_month = datetime.now().month

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        times = request.form['times']
        done = request.form['done']
        goal = request.form['goal']
        
        cursor.execute('SELECT * FROM habits WHERE Habits = %s', (name,))
        existing_habit = cursor.fetchone()

        if existing_habit:
            flash("This habit has already been saved!")
        else:
            
            cursor.execute(
                ''' INSERT INTO habits (Habits, Done, Times, Goal, last_checked_date, last_checked_month) 
                    VALUES (%s, %s, %s, %s, %s, %s) ''',
                (name, done, times, goal, today_date, current_month)
            )
            mysql.connection.commit()
            flash("Habit successfully added!")

        cursor.close()
        return redirect(url_for('habits'))
    
    
    cursor.execute('SELECT * FROM habits')
    habits_list = cursor.fetchall()

    for habit in habits_list:
        if habit['last_checked_month'] != current_month:
            cursor.execute(
                """UPDATE habits SET Times = 0, Done = 0, last_checked_month = %s WHERE id_habit = %s""", 
                (current_month, habit['id_habit'])
            )

        elif habit['last_checked_date'] != today_date:
            cursor.execute(
                """UPDATE habits SET Done = 0 WHERE id_habit = %s""", 
                (habit['id_habit'],)
            )
                    
    mysql.connection.commit()
    cursor.close()
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM habits')
    habitude = cursor.fetchall()
    cursor.close()

    return render_template('habits.html', title="Habits tracker", habitudes=habitude, show_form=show_form)

@app.route('/check-habit/<int:id_habit>', methods=['POST'])
def check_habit(id_habit):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    today_date = datetime.now().strftime('%Y-%m-%d')
    current_month = datetime.now().month

    cursor.execute(""" 
        UPDATE habits 
        SET Done = 1, 
            Times = Times + 1, 
            last_checked_date = %s, 
            last_checked_month = %s 
        WHERE id_habit = %s
    """, (today_date, current_month, id_habit))
    
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('habits'))

@app.route('/delete-habit/<int:id_habit>', methods=['POST'])
def delete_habit(id_habit):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM habits WHERE id_habit = %s', (id_habit,))
    mysql.connection.commit()
    cursor.close()

    flash("Habit successfully deleted!")
    return redirect(url_for('habits'))


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    show_form = (request.args.get('action') =='add')
    

    if request.method =='POST':
        nom_tache = request.form['nom_tache']
        temps_tache = request.form['temps_tache']
        realise = request.form['realise']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM to_do WHERE nom_tache =%s", (nom_tache,))
        tache = cursor.fetchone()

        if tache:
            flash('task already in to do list')
        else:
            cursor.execute("""INSERT INTO to_do (nom_tache, temps_tache, realise) VALUES (%s ,%s, %s) """, (nom_tache, temps_tache, realise))
            mysql.connection.commit()
        cursor.close()
        return redirect(url_for('todo'))


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM to_do")
    mes_taches = cursor.fetchall()
    cursor.close()
    
    return render_template('todo.html', title="To Do List", show_form = show_form, taches = mes_taches)

@app.route('/check-task/<int:id_tache>', methods=['POST'])

def check_task(id_tache):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("""UPDATE to_do 
    SET realise = 1
    WHERE id_tache = %s""", (id_tache,))

    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('todo'))

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)