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
        cliente = request.form['idCliente']
        usuario = request.form['IdUsuario']
        print(usuario)
        try:
            print('Entrou')
            insertPedido(cliente,usuario)
            return jsonify(selectUltimoPedido())
        except mysql.connector.Error as err:
            ('Deu ruim')
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)            
            return redirect(url_for('vendas'))

@app.route('/AdicionaPedidoItem', methods=['POST'])
def AdicionaPedidoItem():
    if request.method =='POST':
        idPedido = request.form['idPedido']
        idProduto = request.form['idProduto']
        QuantidadePedidoItem = request.form['QuantidadePedidoItem']
        print(idPedido,idProduto,QuantidadePedidoItem)
        try:
            print('Entoru Pedido Itens')
            InsertPedidoItem(idPedido, idProduto, QuantidadePedidoItem)
            view = selectPedidosItensView(idPedido)
            return jsonify(view)
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('vendas'))

@app.route('/deletarPedidoItem', methods=['POST','GET'])
def deletarPedidoItem():
    if request.method =='POST':
        idPedidoItem = request.form['idPedidoItem']
        try:
            resultado = deletaPedidoItem(idPedidoItem)
            return jsonify(resultado)
        except mysql.connector.Error as err:
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
            print('passou')
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)  
            return redirect(url_for('vendas'))
    return jsonify(dadosProduto)


@app.route('/pedidosValoresView', methods=['POST','GET'])
def pedidosValoresView():
    if request.method =='POST':
        idPedido = request.form['idPedido']
        try:
            cursor = connection.cursor()
            cursor.execute("Select ValorFinal from PedidosValoresView where IdPedido = %s" %idPedido)
            dadosPedidos = cursor.fetchone()
            print('passou')
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)  
            return redirect(url_for('vendas'))
    return jsonify(dadosPedidos)

@app.route('/InserirDescontoPedido', methods=['POST','GET'])
def InserirDescontoPedido():
    if request.method =='POST':
        idPedido = request.form['idPedido']
        percDesconto = request.form['percDesconto']
        print('entrou na rota')
        try:
            print(jsonify(InsertDescontoPedido(idPedido,percDesconto)))
            return jsonify(InsertDescontoPedido(idPedido,percDesconto))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)  
            return redirect(url_for('vendas'))

@app.route('/FinalizarPedido', methods=['POST','GET'])
def FinalizarPedido():
    if request.method =='POST':
        idPedido = request.form['idPedido']
        try:
            return jsonify(InsertVenda(idPedido))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)  
            return redirect(url_for('vendas'))

def insertPedido(cliente,usuario):
    IdUsuario = BuscaIdUsuario(usuario)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Pedidos (IdCliente, IdUsuario, DataPedido, HoraPedido)  VALUES (%s, %s, now(), now())', (cliente, IdUsuario))            
    connection.commit()

def InsertPedidoItem(idPedido, idProduto, QuantidadePedidoItem):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO PedidosItens (IdPedido, IdProduto, QtdPedidoItem)  VALUES (%s, %s, %s)', (idPedido, idProduto,QuantidadePedidoItem))            
    connection.commit()

def InsertDescontoPedido(idPedido, percDesconto):
    print(idPedido, percDesconto)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO PedidosDescontos (IdPedido, PercentualDesconto) VALUES (%s,%s)", (idPedido,percDesconto))
    connection.commit()

def InsertVenda(idPedido):
    cursor = connection.cursor()
    cursor.execute('insert into Vendas (IdPedido) values (%s)' %idPedido)          
    connection.commit()

def selectUltimoPedido():
    cursor = connection.cursor()
    cursor.execute('SELECT IdPedido FROM Pedidos ORDER BY 1 DESC LIMIT 1')
    IdPedido =  cursor.fetchone()
    return IdPedido

def selectUltimoPedidoItem():
    cursor = connection.cursor()
    cursor.execute('SELECT IdPedidoItem FROM PedidosItens ORDER BY 1 DESC LIMIT 1')
    IdPedidoItem =  cursor.fetchone()
    return IdPedidoItem

def selectPedidosItensView(idPedido):
    cursor = connection.cursor()
    cursor.execute('select * from PedidosItensView where idPedido = %s' %idPedido)
    dadosPedidos = cursor.fetchall()
    data = [list(item) for item in dadosPedidos]
    return data

def deletaPedidoItem(idPedidoItem):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM PedidosItens WHERE idPedidoItem = %s" %idPedidoItem)
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