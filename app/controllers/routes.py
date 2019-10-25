from app import app
import mysql.connector
from app.services import db
from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session

connection = db.db_connection()

@app.route('/produtos')
def produto():
    if 'loggedin' in session:
        return render_template('produtos.html',
                               username=session['username'],
                               loggedin=session['loggedin'],
                               breadcrumb='Produtos',
                               page_header='Menu de Navegação')
    return redirect(url_for('login'))


@app.route('/cadastro', methods=['GET', 'POST'])
def redirecionarProduto():
    if 'loggedin' in session:
        return render_template('cadastro-produtos.html',
                                username=session['username'],
                                loggedin=session['loggedin'],
                                breadcrumb='Cadastro Produtos',
                                page_header='Menu de Cadastro')
    return redirect(url_for('login'))


@app.route('/criar_produto', methods=['POST', 'GET'])
def criar_produto():
    if request.method == 'POST' and 'descProduto' in request.form and 'marcaProduto' in request.form:
        descProduto = request.form['descProduto']
        marcaProduto = request.form['marcaProduto']
        try:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO Produtos (Descricao, Marca) VALUES (%s, %s)', (descProduto, marcaProduto))
            connection.commit()
            msg = 'Cadastro realizado com sucesso!'
            return redirect(url_for('redirecionar'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('redirecionar'))



