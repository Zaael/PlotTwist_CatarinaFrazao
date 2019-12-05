from app import app
from app.services import db
from flask import render_template, request, redirect, url_for, session

connection = db.db_connection()


@app.route('/')
@app.route('/login', methods=['GET', 'POST']) 
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Usuarios WHERE NomeUsuario = %s AND Senha = %s', (username, password))
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['IdUsuario']
            session['username'] = account['NomeUsuario']
            return redirect(url_for('home'))
        else:
            msg = 'Nome de usuário ou Senha inválido!'
    return render_template('login.html',
                           msg=msg,
                           loggedin='')
