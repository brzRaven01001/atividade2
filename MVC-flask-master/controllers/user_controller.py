from flask import render_template, request, redirect, url_for
from models.user import User, db

class UserController:
    @staticmethod
    def index():
        users = User.query.all()
        return render_template('index.html', users=users)

    @staticmethod
    def contact():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']

            # validações simples: se usuário já existe no db, etc

            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('index'))

        return render_template('contact.html')