from flask import Flask
from flasgger import Swagger
from config import Config
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from models.user import db

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa Swagger
swagger = Swagger(app)

# Inicializa banco
db.init_app(app)
with app.app_context():
    db.create_all()

# ---------------- ROTAS DE USUÁRIOS ----------------
app.add_url_rule('/users', 'list_users', UserController.index, methods=['GET'])
app.add_url_rule('/users', 'create_user', UserController.contact, methods=['POST'])

# ---------------- ROTAS DE TAREFAS ----------------
app.add_url_rule('/tasks', 'list_tasks', TaskController.list_tasks, methods=['GET'])
app.add_url_rule('/tasks', 'create_task', TaskController.create_task, methods=['POST'])
app.add_url_rule('/tasks/<int:task_id>', 'update_task', TaskController.update_task, methods=['PUT'])
app.add_url_rule('/tasks/<int:task_id>', 'delete_task', TaskController.delete_task, methods=['DELETE'])

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5002)
