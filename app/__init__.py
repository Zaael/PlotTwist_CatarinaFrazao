from flask import Flask

app = Flask(__name__)
app.secret_key = 'segredo'

from app.controllers import routes, routesFornecedor, clientes, vendas
