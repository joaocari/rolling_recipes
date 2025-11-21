# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

# Cria um Blueprint para as rotas de autenticação.
# O primeiro argumento 'auth' é o nome do Blueprint.
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Importa o objeto mongo aqui para evitar importação circular
        from app import mongo

        username = request.form.get('username')
        password = request.form.get('password')

        # Usamos current_app para aceder à instância 'mongo'
        user_doc = mongo.db.users.find_one({'username': username})

        # Verifica se o utilizador existe e se a password está correta
        if user_doc and check_password_hash(user_doc['password'], password):
            user_obj = User(user_doc)
            login_user(user_obj) # Efetua o login com Flask-Login
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nome de utilizador ou password inválidos.')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Importa o objeto mongo aqui para evitar importação circular
        from app import mongo

        username = request.form.get('username')
        password = request.form.get('password')

        user_doc = mongo.db.users.find_one({'username': username})

        if user_doc:
            flash('Este nome de utilizador já existe.')
            return redirect(url_for('auth.register'))

        # Cria um novo utilizador com a password encriptada
        mongo.db.users.insert_one({
            'username': username,
            'password': generate_password_hash(password, method='pbkdf2:sha256')
        })

        flash('Registo concluído com sucesso! Pode agora fazer login.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required # Só quem está logado pode sair
def logout():
    logout_user()
    return redirect(url_for('index'))