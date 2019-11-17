from app import app
import mysql.connector
from app.services import db
from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session
import json

connection = db.db_connection()

@app.route('/consulta', methods=['GET', 'POST'])
def redirecionarConsulta(mensagem = 'teste'):
    msg = mensagem
    if 'loggedin' in session:
        return render_template('clientes-consulta.html',
                                username=session['username'],
                                loggedin=session['loggedin'],
                                breadcrumb='Consultar Clientes',
                                page_header='Menu de Consulta')
    return redirect(url_for('login'))

@app.route('/consultar_cliente', methods=['GET','POST'])
def consultar_cliente():
    msg = ''
    data = []

    try:
        cursor = connection.cursor()
        cursor.execute('SELECT Nome, CPF, Celular, Email from cliente ')
        dadosCliente = cursor.fetchall()
        data = [list(item) for item in dadosCliente]
        dicDados = {'data':data}
        return dicDados

    except mysql.connector.Error as err:
        msg = 'Ops! Algo deu errado. Erro: {0}'.format(err)
        return redirecionar(msg)

