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

@app.route('/index', methods=['GET', 'POST'])
def index():

    show_form = (request.args.get('action') == 'edit')

    if request.method == 'POST':
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        
        nouveau_texte = request.form['Presentation']

        cursor = mysql.connection.cursor()

        cursor.execute("""UPDATE `index` SET Presentation = %s WHERE id_presentation =1 """, (nouveau_texte, ))

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('index'))

    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM `index` LIMIT 1 """)
    description = cursor.fetchone()
    cursor.close()

    texte_actuel = ""
    if description:
        if isinstance(description, dict):
            texte_actuel = description.get('Presentation', '')
        else:
            texte_actuel = description[0]

    
    return render_template('index.html', title="Home", show_form=show_form, presentation=texte_actuel)

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


@app.route('/projects', methods = ['GET', 'POST'])
def projects():

    show_form = (request.args.get('action') == 'edit')
    project_id = request.args.get('id_project')

    if request.method == 'POST':
        if 'loggedin' not in session: 
            return redirect(url_for('login'))

        edit_id = request.form.get('id')
        name_project = request.form['name_project']
        language_info = request.form['language_info']
        new_description = request.form['description']
        time = request.form['time']
        new_skills = request.form['skills']
        lien = request.form['lien']

        cursor = mysql.connection.cursor()

        if edit_id:
            cursor.execute("UPDATE project SET name_project = %s, language_info = %s, description = %s, time = %s, skills = %s, lien = %s WHERE id_project = %s", (name_project, language_info,new_description,time, new_skills, lien, edit_id))
        else: 
            cursor.execute("INSERT INTO `project` (id_project, name_project, language_info, time, skills, lien, description) VALUES (1, %s, %s, %s, %s, %s,%s)", (name_project, language_info,new_description,time, new_skills, lien))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('projects'))

    selected_project = None
    if show_form and project_id:
        cursor = mysql.connection.cursor()
        cursor.execute( "SELECT * FROM `project` WHERE id_project = %s", (project_id, ))
        selected_project = cursor.fetchone()
        cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `project` ")
    all_projects = cursor.fetchall()
    cursor.close()


    return render_template(
        'projects.html',
        title="Projects",
        show_form=show_form,
        projects = all_projects,
        project = selected_project
    )

@app.route('/habits', methods=['GET', 'POST'])
def habits():


    show_form = (request.args.get('action') == 'add')
    today_date = datetime.now().strftime('%Y-%m-%d')
    current_month = datetime.now().month

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        if 'loggedin' not in session: 
            return redirect(url_for('login'))
        
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

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM to_do WHERE nom_tache =%s", (nom_tache,))
        tache = cursor.fetchone()

        if tache:
            flash('task already in to do list')
        else:
            cursor.execute("""INSERT INTO to_do (nom_tache, temps_tache) VALUES (%s ,%s) """, (nom_tache, temps_tache))
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

@app.route('/delete-task/<int:id_tache>', methods=['POST'])
def delete_task(id_tache):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM to_do WHERE id_tache = %s', (id_tache,))
    mysql.connection.commit()
    cursor.close()

    flash("Task successfully deleted!")
    return redirect(url_for('todo'))

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)