import os
from flask import Flask
from config import Config # importa as 
from controllers.user_controller import UserController
from models.user import db, Task

app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
app.config.from_object(Config)

# inicializa o banco de dados
db.init_app(app)

# cria tabelas

with app.app_context():
    db.create_all()

# forma alternativa de criar rotas, parâmetros: rota em si, endpoint interno do flask e função a ser executada quando a URL for acessada
app.add_url_rule('/', 'index',  UserController.index)
app.add_url_rule('/contact', 'contact', UserController.contact, methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run(debug=True, port=5002)