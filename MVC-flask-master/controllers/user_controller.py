from flask import request, url_for, jsonify
from models.user import User, db

class UserController:
    @staticmethod
    def index():
        users = User.query.all()
        users_list = []
        for user in users:
            users_list.append({
                "id": user.id,
                "name": user.name,
                "email": user.email
            })
        return jsonify(users_list), 200

    @staticmethod
    def contact():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']

            # validações simples: se usuário já existe no db, etc

            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                "mensagem": "Usuário cadastrado com sucesso!",
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            }), 201
        
        return jsonify({"mensagem": "Utilize POST para cadastrar."}), 405
