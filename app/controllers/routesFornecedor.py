from app import app
import mysql.connector

from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session
from app.services import db
from app.controllers import login
from app.controllers import logout
from app.controllers import home

connection = db.db_connection()

@app.route('/fornecedor/')
def fornecedor():
    if 'loggedin' in session:
        return render_template('fornecedor.html',
                                username=session['username'],
                                loggedin=session['loggedin'],
                                breadcrumb='Fornecedor',
                                page_header ='Menu de Navegação')
    return redirect(url_for('login'))

@app.route('/cadastro_fornecedor', methods=['GET', 'POST'])
def cadastro_fornecedor():
    if 'loggedin' in session:
        return render_template('cadastro-fornecedor.html',
                                username=session['username'],
                                loggedin=session['loggedin'],
                                breadcrumb='Cadastro Fornecedor',
                                page_header='Menu de Cadastro')
    return redirect(url_for('login'))


@app.route('/criar_fornecedor', methods=['GET','POST'])
def criar_fornecedor():
    if  request.method == 'POST':
        nomeFornecedor = request.form['Nome_Fornecedor']
        cnpj = request.form['CNPJ']
        contato = request.form['Contato']
        try:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO Fornecedor (nome_Fornecedor, CNPJ, Contato) VALUES (%s, %s, %s)',(nomeFornecedor,cnpj,contato))
            connection.commit()
            msg = 'Cadastro de Fornecedor realizado com sucesso!'
            return redirect(url_for('cadastro_fornecedor'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('cadastro_fornecedor'))

@app.route('/buscar',methods=['GET','POST'])
def buscar():
    if 'loggedin' in session:
        fornecedores = ListaFornecedores()
        return render_template('buscar_fornecedor.html', fornecedores= fornecedores,
                                username=session['username'],
                                loggedin=session['loggedin'],
                                breadcrumb='Consultar Fornecedores',
                                page_header='Menu de Consulta')
    return redirect(url_for('login'))

@app.route('/alterar', methods=['POST'])
def alterar_fornecedor():
    if request.method == 'POST':
        idFornecedor = request.form['idFornecedor']
        nomeFornecedor = request.form['Nome_Fornecedor']
        cnpj = request.form['CNPJ']
        contato = request.form['Contato']
        try:
            AtualizaFornecedor(idFornecedor, nomeFornecedor, cnpj, contato)
            return redirect(url_for('buscar'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('buscar'))

@app.route('/deletar', methods=['POST'])
def deletar_fornecedor(id):
    if request.method == 'POST':
        idFornecedor = request.form['idFornecedor']
        try:
            deletarFornecedor(idFornecedor)
            return redirect(url_for('buscar'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('buscar'))


def ListaFornecedores():
    cursor = connection.cursor()
    cursor.execute("SELECT idFornecedor, Nome_Fornecedor, CNPJ, Contato from Fornecedor")
    dadosFornecedor = cursor.fetchall()
    data = [list(item) for item in dadosFornecedor]
    return data

def buscaPorIdFornecedor(id):
    cursor = connection.cursor()
    cursor.execute('SELECT idFornecedor, Nome_Fornecedor, CNPJ, Contato FROM Fornecedor WHERE idFornecedor = %s',(id,))
    data = cursor.fetchone()
    return data

def AtualizaFornecedor(id, nome, cnpj, contato):
    cursor = connection.cursor()
    cursor.execute('UPDATE Fornecedor SET Nome_Fornecedor = %s, CNPJ = %s, Contato = %s WHERE idFornecedor = %s',(nome,cnpj,contato,id))
    connection.commit()

def deletarFornecedor(id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Fornecedores WHERE idFornecedor = %s',(id,))
    connection.commit()