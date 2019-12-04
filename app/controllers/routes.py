from app import app
import mysql.connector
from app.services import db
from mysql.connector.errors import Error
from flask import render_template, request, redirect, url_for, session
from app.controllers import routesFornecedor

connection = db.db_connection()

@app.route('/produtos')
def produtos():
    if 'loggedin' in session:
        produtos = ListaProdutoItens()
        marcas = ListaMarcas()
        cores = ListaCores()
        materiais = ListaMateriais()
        fornecedores = routesFornecedor.ListaFornecedores()
        return render_template('produtos.html', produtos = produtos, marcas = marcas, cores=cores, materiais = materiais, fornecedores=fornecedores,
                               username=session['username'],
                               loggedin=session['loggedin'],
                               breadcrumb='Produtos',
                               page_header='Produtos')
    return redirect(url_for('login'))


@app.route('/criar_produto', methods=['POST', 'GET'])
def criar_produto():
    if request.method == 'POST':
        descricao = request.form['descricao']
        IdMarca = request.form['Marca']
        idCor = request.form['Cor']
        idMaterial = request.form['Material']
        idFornecedor = request.form['Fornecedor']
        Custo = request.form['Custo']
        Preco = request.form['Preco']
        Quantidade = request.form['Quantidade']
        print(descricao, IdMarca, idCor, idMaterial, idFornecedor, Custo, Preco, Quantidade)
        try:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO Produtos (Descricao, IdMarca, IdCor, IdMaterial, IdFornecedor, Custo, Preco, Quantidade)\
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (descricao, IdMarca, idCor, idMaterial, idFornecedor, Custo, Preco, Quantidade))
            connection.commit()
            msg = 'Cadastro realizado com sucesso!'
            return redirect(url_for('produtos'))
        except mysql.connector.Error as err:
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('produtos'))

@app.route('/alterar_Produto', methods=['POST','GET'])
def alterar_Produto():
    if request.method == 'POST':
        idProduto = int(request.form['idProduto'])
        Preco = float(request.form['Preco'])    
        Quantidade = int(request.form['Quantidade'])
        print(idProduto,Preco,Quantidade)
        try:
            cursor = connection.cursor()
            print('chegou')
            cursor.execute('UPDATE Produtos SET Preco = %s, Quantidade = %s WHERE idProduto = %s)', (Preco, Quantidade, idProduto))
            connection.commit()
            return redirect(url_for('produtos'))
        except mysql.connector.Error as err:
            print('Deu erro')
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('produtos'))

@app.route('/deletar_produto', methods=['GET','POST'])
def deletar_produto():
    if request.method == 'POST':
        idProduto = request.form['id']
        try:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM Produtos WHERE idProduto = %s' %idProduto)
            connection.commit()
            return redirect(url_for('produtos'))
        except mysql.connector.Error as err:
            print('sa pohha não funciona')
            msg = 'Ops! Algo deu errado. Verifique as informações e tente novamente. Erro: {}'.format(err)
            return redirect(url_for('produtos'))


def ListaProdutoItens():
    cursor = connection.cursor()
    cursor.execute("Select idProduto, Descricao, M.DescricaoMarca, C.DescricaoCor, MT.DescricaoMaterial, Custo, Preco, Quantidade, F.Nome_Fornecedor\
                    from Produtos P Inner join Marcas M ON (P.idMarca = M.idMarca)\
                                    inner join Cores C ON (P.idCor = C.idCor)\
                                    Inner join Materiais MT ON (P.idMaterial = MT.IdMaterial)\
                                    Inner join Fornecedor F ON (P.idFornecedor = F.idFornecedor);")
    dadosProduto = cursor.fetchall()
    data = [list(item) for item in dadosProduto]
    return data

def ListaMarcas():
    cursor = connection.cursor()
    cursor.execute("select IdMarca, DescricaoMarca from Marcas")
    dadosMarca = cursor.fetchall()
    data = [list(item) for item in dadosMarca]
    return data

def ListaCores():
    cursor = connection.cursor()
    cursor.execute("select IdCor, DescricaoCor from Cores;")
    dadosCores = cursor.fetchall()
    data = [list(item) for item in dadosCores]
    return data

def ListaMateriais():
    cursor = connection.cursor()
    cursor.execute("select IdMaterial, DescricaoMaterial from Materiais;")
    dadosMateriais = cursor.fetchall()
    data = [list(item) for item in dadosMateriais]
    return data