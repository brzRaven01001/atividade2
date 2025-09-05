from flask import request, jsonify
from models.user import Task, User, db
from models.user import User, db

class TaskController:
    @staticmethod
    def list_tasks():
        """
        Listar todas as tarefas
        ---
        tags:
          - Tasks
        responses:
          200:
            description: Lista de tarefas
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  description:
                    type: string
                  status:
                    type: string
                  user_id:
                    type: integer
        """
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks]), 200

    @staticmethod
    def create_task():
        """
        Criar uma nova tarefa
        ---
        tags:
          - Tasks
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - title
                - description
                - user_id
              properties:
                title:
                  type: string
                  example: "Fazer compras"
                description:
                  type: string
                  example: "banana, café, macarrão"
                status:
                  type: string
                  example: "Pendente"
                user_id:
                  type: integer
                  example: 1
        responses:
          201:
            description: Tarefa criada
        """
        data = request.get_json()

        if not data or "title" not in data or "description" not in data or "user_id" not in data:
            return jsonify({"error": "Campos obrigatórios: title, description e user_id"}), 400

        user = User.query.get(data["user_id"])
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        new_task = Task(
            title=data["title"],
            description=data["description"],
            status=data.get("status", "Pendente"),
            user_id=data["user_id"]
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            "message": "Tarefa criada com sucesso!",
            "task": new_task.to_dict()
        }), 201

    @staticmethod
    def update_task(task_id):
        """
        Atualizar uma tarefa existente
        ---
        tags:
          - Tasks
        parameters:
          - name: task_id
            in: path
            type: integer
            required: true
          - in: body
            name: body
            schema:
              type: object
              properties:
                title:
                  type: string
                description:
                  type: string
                status:
                  type: string
        responses:
          200:
            description: Tarefa atualizada
          404:
            description: Tarefa não encontrada
        """
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404

        data = request.get_json()
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.status = data.get("status", task.status)

        db.session.commit()
        return jsonify({
            "message": "Tarefa atualizada com sucesso!",
            "task": task.to_dict()
        }), 200

    @staticmethod
    def delete_task(task_id):
        """
        Excluir uma tarefa
        ---
        tags:
          - Tasks
        parameters:
          - name: task_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Tarefa deletada
          404:
            description: Tarefa não encontrada
        """
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404

        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Tarefa excluída com sucesso!"}), 200
