from app import app
import mysql.connector

from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session
from app.services import db
from app.controllers import login
from app.controllers import logout
from app.controllers import home

connection = db.db_connection()

@app.route('/fornecedores',methods=['GET','POST'])
def fornecedores():
    if 'loggedin' in session:
        fornecedores = ListaFornecedores()
        return render_template('fornecedores.html', fornecedores= fornecedores,
                                username=session['username'],
                                loggedin=session['loggedin'],
                                breadcrumb='Consultar Fornecedores',
                                page_header='Fornecedores')
    return redirect(url_for('login'))

@app.route('/criar_fornecedor', methods=['GET','POST'])
def criar_fornecedor():
    if  request.method == 'POST':
        nomeFornecedor = request.form['NomeFornecedor']
        cnpj = request.form['CNPJ']
        contato = request.form['Contato']
        celular = request.form['Celular']
        email = request.form['Email']
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Fornecedor (nome_Fornecedor, CNPJ, Contato, Celular, Email) VALUES \
            (%s, replace(replace(replace(%s, '.', ''), '-', ''), '/', ''), %s \
            , replace(replace(replace(replace(%s, '(', ''), ')', ''), '-', ''), ' ', ''), %s)",(nomeFornecedor,cnpj,contato, celular, email))
            connection.commit()
            msg = 'Cadastro de Fornecedor realizado com sucesso!'
            return redirect(url_for('fornecedores'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('fornecedores'))

@app.route('/alterar', methods=['POST'])
def alterar_fornecedor():
    if  request.method == 'POST':
        idFornecedor = request.form['idFornecedor']
        nomeFornecedor = request.form['NomeFornecedor']
        contato = request.form['Contato']
        celular = request.form['Celular']
        email = request.form['Email']
        try:
            AtualizaFornecedor(idFornecedor, nomeFornecedor, contato, celular, email)
            return redirect(url_for('fornecedores'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('fornecedores'))

@app.route('/deletar_fornecedor', methods=['GET','POST'])
def deletar_fornecedor():
    if request.method == 'POST':
        idFornecedor = request.form['id']
        print(idFornecedor)
        try:
            msg = deletarFornecedor(idFornecedor)
            return msg
        except mysql.connector.Error as err:
            msg = 'Ops! Não é possível excluir este cliente!'
            return msg

def ListaFornecedores():
    cursor = connection.cursor()
    cursor.execute("SELECT idFornecedor, CNPJ, Nome_Fornecedor, Contato, Celular, Email from Fornecedor")
    dadosFornecedor = cursor.fetchall()
    data = [list(item) for item in dadosFornecedor]
    return data

def AtualizaFornecedor(id, nome, contato, celular, email):
    cursor = connection.cursor()
    cursor.execute("UPDATE Fornecedor SET Nome_Fornecedor = %s, Contato = %s, Celular =replace(replace(replace(replace(%s, '(', ''), ')', ''), '-', ''), ' ', '') \
    , Email = %s WHERE idFornecedor = %s",(nome,contato, celular, email, id))
    connection.commit()

def deletarFornecedor(id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Fornecedor WHERE idFornecedor = %s' %id)
    connection.commit()
    return 'Deletado!'