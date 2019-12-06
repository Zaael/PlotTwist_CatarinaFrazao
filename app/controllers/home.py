from app import app
import mysql.connector

from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session, jsonify
from app.services import db
from app.controllers import login
from app.controllers import logout
from app.controllers import home

connection = db.db_connection()

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


@app.route('/maisVendidos', methods=['GET','POST'])
def maisVendidos():
    if request.method == 'POST':
        datamin = str(request.form['datamin'])
        datamax = str(request.form['datamax'])
        print(datamax, datamin)

        try:
            return ProdMaisVendidos(datamin, datamax)
        except mysql.connector.Error as err:
            print('Erro ao realizar alteração. Erro: {}'.format(err))
            return redirect(url_for('cliente'))

@app.route('/menosVendidos', methods=['GET','POST'])
def menosVendidos():
    if request.method == 'POST':
        datamin = str(request.form['datamin'])
        datamax = str(request.form['datamax'])
        try:
            return ProdMenosVendidos(datamin, datamax)
        except mysql.connector.Error as err:
            msg = 'Erro ao realizar alteração. Erro: {}'.format(err)
            return redirect(url_for('cliente'))

def ProdMaisVendidos(datamin, datamax):
    cursor = connection.cursor()
    cursor.callproc("ProcProdutosMaisVendidos",[datamin, datamax])
    dados = ''
    for result in cursor.stored_results():
      dados = result.fetchall()
    return jsonify(dados)

def ProdMenosVendidos(datamin, datamax):
    cursor = connection.cursor()
    cursor.callproc("ProcProdutosMenosVendidos",[datamin, datamax])
    dados = ''
    for result in cursor.stored_results():
      dados = result.fetchall()
      print(dados)
    return jsonify(dados)