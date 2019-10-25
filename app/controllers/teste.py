import mysql.connector
from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session
import json
def db_connection():
    connection = mysql.connector.connect(host='localhost',
                                         database='ope_impacta',
                                         user='root',
                                         password='12345',
                                         auth_plugin='mysql_native_password')
    return connection


def consultar_cliente():
    msg = ''
    data = []
    conn = db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT Nome, CPF, Celular, Email from cliente ')
        dadosCliente = cursor.fetchall()
        data = [list(item) for item in dadosCliente]
        dicDados = {'dado':data}
        return json.dumps(dicDados)
    except mysql.connector.Error as err:
        msg = 'Ops! Algo deu errado. Erro: {0}'.format(err)
        return msg

print (consultar_cliente())