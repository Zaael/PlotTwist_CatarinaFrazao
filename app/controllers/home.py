from app import app
from flask import render_template, request, redirect, url_for, session


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('home.html',
                               username=session['username'],
                               loggedin=session['loggedin'],
                               breadcrumb='HOME',
                               page_header='Painel de Navegação')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
