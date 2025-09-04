import os
from flask import Flask
from flasgger import Swagger
from config import Config
from controllers.user_controller import UserController
from models.user import db
from controllers.task_controller import TaskController

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

swagger = Swagger(app)

print("=" * 50)
print("DEBUG: Verificando estrutura de pastas")
print("Diretório atual:", os.getcwd())
print("Pasta templates existe?", os.path.exists('templates'))
if os.path.exists('templates'):
    print("Arquivos na pasta templates:", os.listdir('templates'))
print("=" * 50)

# inicializa o banco de dados
db.init_app(app)

# cria tabelas
with app.app_context():
    db.create_all()

app.add_url_rule('/index', 'index', UserController.index)
app.add_url_rule('/contact', 'contact', UserController.contact, methods=['GET', 'POST'])

# Rotas de tarefas
app.add_url_rule('/tasks', 'tasks', TaskController.tasks, methods=['GET', 'POST'])
app.add_url_rule('/tasks/<int:task_id>', 'edit_tasks', TaskController.edit_tasks, methods=['PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True, port=5002)