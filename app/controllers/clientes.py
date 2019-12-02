from app import app
import mysql.connector

from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session
from app.services import db
from app.controllers import login
from app.controllers import logout
from app.controllers import home

connection = db.db_connection()

@app.route('/clientes')
def cliente_inicio():
    if 'loggedin' in session:
        return render_template('clientes.html',
                               username=session['username'],
                               loggedin=session['loggedin'],
                               breadcrumb='Clientes',
                               page_header ='Menu de Navegação')
    return redirect(url_for('login'))


@app.route('/cliente',methods=['GET','POST'])
def cliente():
    if 'loggedin' in session:
        clientes = listaCliente()
        return render_template('clientes.html', clientes= clientes,
                                username=session['username'],
                                loggedin=session['loggedin'],
                                breadcrumb='Clientes',
                                page_header='Ações em Clientes')
    return redirect(url_for('login'))


@app.route('/criar_cliente', methods=['GET','POST'])
def criar_cliente():
    if  request.method == 'POST':
        NomeCliente = request.form['NomeCliente']
        CPFCliente = request.form['CPF']
        CelularCliente = request.form['Celular']
        EmailCliente = request.form['Email']
        try:
            criaCliente(NomeCliente, CPFCliente, CelularCliente, EmailCliente)
            msg = 'Cadastro de cliente realizado com sucesso!'
            return redirect(url_for('cliente'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('cliente'))


@app.route('/alterar_cliente', methods=['POST'])
def alterar_cliente():
    if request.method == 'POST':
        idcliente = request.form['idCliente']
        NomeCliente = request.form['NomeCliente']
        CPF = request.form['CPF']
        Celular = request.form['Celular']
        Email = request.form['Email']
        try:
            atualizaCliente(idcliente, NomeCliente, CPF, Celular, Email)
            return redirect(url_for('cliente'))
        except mysql.connector.Error as err:
            msg = 'Erro ao realizar alteração. Erro: {}'.format(err)
            return redirect(url_for('cliente'))

@app.route('/deletar_cliente', methods=['GET','POST'])
def deletar_cliente():
    if request.method == 'POST':
        idcliente = request.form['id']
        try:
            deletarCliente(idcliente)
            return redirect(url_for('cliente'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Tente novamente. Erro: {}'.format(err)
            return redirect(url_for('cliente'))


def listaCliente():
    cursor = connection.cursor()
    cursor.execute("SELECT idCliente, CPF, Nome, Celular, Email from cliente")
    dadoscliente = cursor.fetchall()
    data = [list(item) for item in dadoscliente]
    return data

def buscaPorIdCliente(id):
    cursor = connection.cursor()
    cursor.execute('SELECT idCliente, CPF, Nome, Celular, Email FROM cliente WHERE idcliente = %s',(id))
    data = cursor.fetchone()
    return data

def atualizaCliente(id, nome, CPF, Celular, Email):
    cursor = connection.cursor()
    cursor.execute('UPDATE cliente SET Nome = %s, CPF = %s, Celular = %s, Email = %s WHERE idcliente = %s',(nome,CPF,Celular, Email,id))
    connection.commit()

def deletarCliente(id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM cliente WHERE idCliente = %s' % id)
    connection.commit()

def criaCliente(nome, CPF, Celular, Email):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO cliente (Nome, CPF, Celular, Email) VALUES (%s, %s, %s, %s)',(nome, CPF, Celular, Email))
    connection.commit()
