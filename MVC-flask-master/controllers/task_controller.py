from flask import render_template, request, redirect, url_for
from models.user import User, db, Task


class TaskController:
    @staticmethod
    def list_tasks():
        tasks = Task.query.all()
        return render_template('tasks.html', tasks=tasks)


    @staticmethod
    def create_task(title,description,user_id):
        usuario = User.query.get(user_id)
        if not usuario:
            return "usuário não encontrado"
        
        new_task = Task(title=title,description=description,user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        return render_template('create_task.html', new_task=new_task)


    @staticmethod
    def update_task_status(task_id):
        task = Task.query.get(task_id)
        if task is None:
            return 'Tarefa Não Encontrada'
       
        if task.status == "Pendente":
            task.status = "Concluido"
        else:
            task.status =  "Pendente"
        db.session.commit()
        return redirect(url_for("list_tasks"))


    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return 'Task Não Encontrada'
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("list_tasks"))