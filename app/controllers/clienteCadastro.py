from app import app
import mysql.connector
from app.services import db
from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session

connection = db.db_connection()

@app.route('/cadastro', methods=['GET', 'POST'])
def redirecionarCadastro(mensagem = 'teste'):
    msg = mensagem
    if 'loggedin' in session:
        return render_template('clientes-cadastro.html',
                                username=session['username'],
                                loggedin=session['loggedin'],
                                breadcrumb='Cadastro Clientes',
                                page_header='Menu de Cadastro',
                                msg='teste')
    return redirect(url_for('login'))

@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    msg = ''
    if request.method == 'POST' and 'nomeCliente' in request.form \
                                and 'cpfCliente' in request.form \
                                and 'celularCliente' in request.form \
                                and 'emailCliente' in request.form:
        nomeCliente = request.form['nomeCliente']
        cpfCliente = request.form['cpfCliente']
        celularCliente = request.form['celularCliente']
        emailCliente = request.form['emailCliente']

        try:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO cliente (Nome, CPF, Celular, Email) VALUES (%s, %s, %s, %s)', (nomeCliente, cpfCliente, celularCliente, emailCliente))
            connection.commit()
            msg = 'Cadastro realizado com sucesso!'
            return redirecionarCadastro(msg)

        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {0}'.format(err)
            return redirecionarCadastro(msg)