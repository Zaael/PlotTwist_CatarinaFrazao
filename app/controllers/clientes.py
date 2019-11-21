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


@app.route('/buscar_cliente',methods=['GET','POST'])
def buscar_cliente():
    if 'loggedin' in session:
        clientes = listaCliente()
        return render_template('clientes-consulta.html', clientes= clientes,
                                username=session['username'],
                                loggedin=session['loggedin'],
                                breadcrumb='Consultar clientes',
                                page_header='Menu de Consulta')
    return redirect(url_for('login'))


@app.route('/criar_cliente', methods=['GET','POST'])
def criar_cliente():
    if  request.method == 'POST':
        NomeCliente = request.form['Nomecliente']
        CPFCliente = request.form['CPF']
        CelularCliente = request.form['Celular']
        EmailCliente = request.form['Email']
        try:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO cliente (Nome, CPF, Celular, Email) VALUES (%s, %s, %s, %s)',(NomeCliente, CPFCliente, CelularCliente, EmailCliente))
            connection.commit()
            msg = 'Cadastro de cliente realizado com sucesso!'
            return redirect(url_for('cadastro_cliente'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('cadastro_cliente'))


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
            return redirect(url_for('buscar_cliente'))
        except mysql.connector.Error as err:
            msg = 'Erro ao realizar alteração. Erro: {}'.format(err)
            return redirect(url_for('buscar_cliente'))

@app.route('/deletar_cliente', methods=['GET','POST'])
def deletar_cliente():
    if request.method == 'POST':
        idcliente = request.form['id']
        try:
            deletarCliente(idcliente)
            return redirect(url_for('buscar_cliente'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Tente novamente. Erro: {}'.format(err)
            return redirect(url_for('buscar_cliente'))


def listaCliente():
    cursor = connection.cursor()
    cursor.execute("SELECT idCliente, Nome, CPF, Celular, Email from cliente")
    dadoscliente = cursor.fetchall()
    data = [list(item) for item in dadoscliente]
    return data

def buscaPorIdCliente(id):
    cursor = connection.cursor()
    cursor.execute('SELECT idCliente, Nome, CPF, Celular, Email FROM cliente WHERE idcliente = %s',(id))
    data = cursor.fetchone()
    return data

def atualizaCliente(id, nome, CPF, Celular, Email):
    cursor = connection.cursor()
    cursor.execute('UPDATE cliente SET Nome = %s, CPF = %s, Celular = %s, Email = %s WHERE idcliente = %s',(nome,CPF,Celular, Email,id))
    connection.commit()

def deletarCliente(id):
    delid = id
    cursor = connection.cursor()
    print(delid)
    cursor.execute('DELETE FROM cliente WHERE idcliente = %s' % delid)
    print('foi')
    connection.commit()