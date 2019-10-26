from app import app
import mysql.connector
from app.services import db
from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session

connection = db.db_connection()

@app.route('/consultar_cliente', methods=['GET','POST'])
def consultar_cliente():
    msg = ''
    data = []

    try:
        cursor = connection.cursor()
        cursor.execute('UPDATE cliente SET Nome =  CPF, Celular, Email  ')
        dadosCliente = cursor.fetchall()
        data = [list(item) for item in dadosCliente]
        dicDados = {'data':data}
        return dicDados

    except mysql.connector.Error as err:
        msg = 'Ops! Algo deu errado. Erro: {0}'.format(err)
        return redirecionar(msg)
