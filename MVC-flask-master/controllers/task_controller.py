from flask import request, url_for, jsonify
from models.user import User, Task, db

class TaskController:
    @staticmethod
    def tasks():
        if request.method == 'POST':
            data = request.json
            if User.query.get(data['user_id']):
                new_task = Task(id=data['id'], title=data['title'], description=data['description'], user_id=data['user_id'])
                db.session.add(new_task)
                db.session.commit()
                return request.json
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
        if request.method == 'PUT':
            data = request.json
            task = Task.query.get(task_id)
            data['id'] = task.id
            data['user_id'] = task.user_id

            if task is None:
                return jsonify({'Tarefa Não Encontrada'}), 404
            
            if "title" in data:
                task.title = data['title']
            else:
                data['title'] = task.title

            if "description" in data:
                task.description = data['description']
            else:
                data['description'] = task.description

            if "status" in data:
                task.status = data['status']
            else:
                data['status'] = task.status
            
            db.session.commit()
            return jsonify(data), 200
        if request.method == 'DELETE':
            task = Task.query.get(task_id)
            if not task:
                return jsonify({'Task Não Encontrada'}), 404
            db.session.delete(task)
            db.session.commit()
            return jsonify(('Task deletada')), 200

