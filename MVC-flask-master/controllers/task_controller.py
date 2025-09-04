from flask import request, url_for, jsonify
from models.user import User, Task, db

class TaskController:
    @staticmethod
    def tasks():
        """
        Criar e Listar Tasks
        ---
        tags:
          - Tasks
        get:
          description: Lista todas as tarefas cadastradas
          responses:
            200:
              description: Lista de tarefas retornada com sucesso
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    title:
                      type: string
                      example: "Fazer compras no mercado"
                    description:
                      type: string
                      example: "banana, café, macarrão"
                    status:
                      type: string
                      example: "Pendente"
                    user_id:
                      type: integer
                      example: 2
        post:
          description: Criar uma nova tarefa
          parameters:
            - in: body
              name: body
              required: true
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  title:
                    type: string
                    example: "Fazer compras no mercado"
                  description:
                    type: string
                    example: "banana, café, macarrão"
                  status:
                    type: string
                    example: "Pendente"
                  user_id:
                    type: integer
                    example: 2
          responses:
            200:
              description: Tarefa criada com sucesso
            404:
              description: Usuário não encontrado
        """
        if request.method == 'POST':
            data = request.json
            if User.query.get(data['user_id']):
                new_task = Task(
                    id=data['id'],
                    title=data['title'],
                    description=data['description'],
                    user_id=data['user_id']
                )
                db.session.add(new_task)
                db.session.commit()
                return jsonify(data), 200
            else:
                return jsonify({"Usuário não encontrado"}), 404
        if request.method == 'GET':
            tasks = Task.query.all()
            tasks_list = []
            for task in tasks:
                tasks_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "user_id": task.user_id
                })
            return jsonify(tasks_list), 200
    
    @staticmethod
    def edit_tasks(task_id):
        """
        Editar ou Deletar Task
        ---
        tags:
          - Tasks
        parameters:
          - in: path
            name: task_id
            type: integer
            required: true
            description: ID da tarefa
            example: 1
        put:
          description: Editar uma task existente
          parameters:
            - in: body
              name: body
              required: true
              schema:
                type: object
                properties:
                  title:
                    type: string
                    example: "Ir ao Petshop"
                  description:
                    type: string
                    example: "Comprar ração e brinquedo"
                  status:
                    type: string
                    example: "Pendente"
                    enum: [Pendente, Em andamento, Concluída]
          responses:
            200:
              description: Tarefa atualizada com sucesso
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  user_id:
                    type: integer
                    example: 10
                  title:
                    type: string
                    example: "Estudar Flask (atualizado)"
                  description:
                    type: string
                    example: "Ler documentação e praticar"
                  status:
                    type: string
                    example: "Em andamento"
            404:
              description: Tarefa não encontrada
        delete:
          description: Deletar uma tarefa existente
          responses:
            200:
              description: Tarefa deletada com sucesso
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Task deletada"
            404:
              description: Tarefa não encontrada
        """
        if request.method == 'PUT':
            task = Task.query.get(task_id)
            if task is None:
                return jsonify({'Tarefa Não Encontrada'}), 404

            data = request.json
            data['id'] = task.id
            data['user_id'] = task.user_id

            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.status = data.get("status", task.status)

            db.session.commit()
            return jsonify(data), 200

        if request.method == 'DELETE':
            task = Task.query.get(task_id)
            if not task:
                return jsonify({'Task Não Encontrada'}), 404
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deletada'}), 200
