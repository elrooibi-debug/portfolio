from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
from config import Config



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

@app.route('/about', methods=['GET', 'POST'])
def about():
    show_form = (request.args.get('action') == 'edit')
    about_id = request.args.get('id')

    if request.method == 'POST':
        if 'loggedin' not in session:
            return redirect(url_for('login'))

        edition_id = request.form.get('id')
        new_text = request.form['description']
        new_skills = request.form['skills']
        email = request.form['email']
        github_link = request.form['link']

        cursor = mysql.connection.cursor()

        if edition_id:
            cursor.execute("UPDATE `about` SET description = %s, skills = %s, email = %s, link = %s WHERE id = %s", (new_text, new_skills, email, github_link, edition_id))
        else: 
            cursor.execute("INSERT INTO `about` (description, skills, email, link) VALUES (%s, %s, %s, %s)", (new_text, new_skills, email, github_link))

        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('about'))

    # Pour remplir le formulaire d'édition
    selected_about = None
    if show_form and about_id:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM `about` WHERE id = %s", (about_id,))
        selected_about = cursor.fetchone()
        cursor.close()

    # Pour l'affichage normal
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `about`")
    about = cursor.fetchall()
    cursor.close()

    return render_template('about.html', title="About", about=about, show_form=show_form, selected_about=selected_about)
@app.route('/login', methods=['GET', 'POST'])
def login():
    
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






if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)