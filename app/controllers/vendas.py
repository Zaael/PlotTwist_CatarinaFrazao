from app import app
import mysql.connector
from app.services import db
from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session, jsonify
from app.controllers import routes


connection = db.db_connection()

@app.route('/vendas')
def vendas():
    pedidos = listaPedidos()
    Clientes = listaCliente()
    produtos = routes.ListaProdutoItens()
    if 'loggedin' in session:
        return render_template('vendas.html', pedidos = pedidos, Clientes = Clientes, Produtos = produtos,
                                username=session['username'],
                                loggedin=session['loggedin'],
                                breadcrumb='Vendas',
                                page_header='Página de Vendas')
    return redirect(url_for('login'))

@app.route('/AdicionaPedido', methods=['POST'])
def AdicionaPedido():
    if request.method == 'POST':
        cliente = request.form['Cliente']
        usuario = request.form['IdUsuario']
        print(usuario)
        try:
            print('Entrou')
            insertPedido(cliente,usuario)
            return 'bangos'
        except mysql.connector.Error as err:
            ('Deu ruim')
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)            
            return redirect(url_for('vendas'))

@app.route('/GetProduto', methods=['GET','POST'])
def GetProduto():
    if request.method == 'POST':
        id = request.form['id']
        try:
            print('ENTROU NO TRY')
            cursor = connection.cursor()
            cursor.execute("Select idProduto, Descricao, M.DescricaoMarca, C.DescricaoCor, MT.DescricaoMaterial, Custo, Preco, Quantidade, F.Nome_Fornecedor\
                            from Produtos P Inner join Marcas M ON (P.idMarca = M.idMarca)\
                                            inner join Cores C ON (P.idCor = C.idCor)\
                                            Inner join Materiais MT ON (P.idMaterial = MT.IdMaterial)\
                                            Inner join Fornecedor F ON (P.idFornecedor = F.idFornecedor)\
                            WHERE idProduto = %s" %id)
            dadosProduto = cursor.fetchone()
            #data = [list(item) for item in dadosProduto]
            print('passou')
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)  
            return redirect(url_for('vendas'))
    return jsonify(dadosProduto)


def insertPedido(cliente,usuario):
    IdUsuario = BuscaIdUsuario(usuario)
    print(IdUsuario, cliente)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Pedidos (IdCliente, IdUsuario, DataPedido, HoraPedido)  VALUES (%s, %s, now(), now())', (cliente, IdUsuario))
    cursor.execute('SELECT idPedido FROM Pedidos ORDER BY 1 DESC LIIMT 1')
    connection.commit()



def listaPedidos():
    cursor = connection.cursor()
    cursor.execute("SELECT IdCliente, IdUsuario, DataPedido, HoraPedido FROM Pedidos")
    dadosPedidos = cursor.fetchall()
    data = [list(item) for item in dadosPedidos]
    return data

def listaCliente():
    cursor = connection.cursor()
    cursor.execute("SELECT IdCliente, Nome, CPF FROM Cliente")
    dadosCleintes = cursor.fetchall()
    data = [list(item) for item in dadosCleintes]
    return data

def BuscaIdUsuario(NomeUsuario):
    print('entrou na busca',NomeUsuario)
    cursor = connection.cursor()
    cursor.execute("SELECT IdUsuario FROM Usuarios WHERE NomeUsuario = '%s'" %NomeUsuario)
    dados = cursor.fetchone()
    idUsuario = dados[0]
    return idUsuario