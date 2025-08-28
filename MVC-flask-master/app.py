import os
from flask import Flask
from config import Config
from controllers.user_controller import UserController
from models.user import db, Task
from controllers.task_controller import TaskController


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


# rotas de tarefas

app.add_url_rule('/tasks', 'list_tasks', TaskController.list_tasks, methods=['GET'])
app.add_url_rule('/tasks/new', 'create_task', TaskController.create_task, methods=['GET', 'POST'])
app.add_url_rule('/tasks/update/<int:task_id>', 'update_task_status', TaskController.update_task_status, methods=['POST'])
app.add_url_rule('/tasks/delete/<int:task_id>', 'delete_task', TaskController.delete_task, methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True, port=5002)