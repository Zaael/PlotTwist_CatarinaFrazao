from app import app
import mysql.connector

from mysql.connector.errors import Error
from flask import render_template, request
from app.services import db
from app.controllers import login
from app.controllers import logout
from app.controllers import home

connection = db.db_connection()

@app.route('/cadastro_produto', methods=['GET', 'POST'])
def cadastro_produto():
    return render_template('cadastro-produtos.html')


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
            return render_template('cadastro-produtos.html', msg=msg)
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return render_template('cadastro-produtos.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page



