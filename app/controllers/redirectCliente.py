from app import app
import mysql.connector
from flask import render_template, request, redirect, url_for, session


@app.route('/clientes')
def cliente_inicio():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('clientes.html',
                               username=session['username'],
                               loggedin=session['loggedin'],
                               breadcrumb='Clientes',
                               page_header='Menu de Navegação')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
