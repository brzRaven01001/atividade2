from flask import request, jsonify
from models.user import User, db

class UserController:
    @staticmethod
    def index():
        """
        Listar todos os usuários
        ---
        tags:
          - Users
        responses:
          200:
            description: Lista de usuários
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
        """
        users = User.query.all()
        return jsonify([{
            "id": user.id,
            "name": user.name,
            "email": user.email
        } for user in users]), 200

    @staticmethod
    def contact():
        """
        Criar um novo usuário
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - name
                - email
              properties:
                name:
                  type: string
                  example: "Maria Silva"
                email:
                  type: string
                  example: "maria@email.com"
        responses:
          201:
            description: Usuário criado
          400:
            description: Dados inválidos
        """
        if request.method == 'POST':
            data = request.get_json()

            if not data or "name" not in data or "email" not in data:
                return jsonify({"error": "Campos obrigatórios: name e email"}), 400

            if User.query.filter_by(email=data["email"]).first():
                return jsonify({"error": "E-mail já cadastrado"}), 400

            new_user = User(name=data["name"], email=data["email"])
            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                "message": "Usuário cadastrado com sucesso!",
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            }), 201

        return jsonify({"mensagem": "Método não permitido. Use POST."}), 405
