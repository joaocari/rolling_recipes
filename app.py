# /rolling_recipe_app/app.py

import os
from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
from functools import wraps
from models import models

# --- Configuração da Aplicação ---
app = Flask(__name__)

# Chave secreta para a gestão de sessões
app.secret_key = os.environ.get("SECRET_KEY", "uma-chave-secreta-muito-segura")

# Configuração da ligação ao MongoDB
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/rolling_recipes_db")
mongo = PyMongo(app)

# --- Decorador de Autenticação ---

def login_required(f):
    """
    Decorador para proteger rotas que exigem autenticação.
    Verifica se 'user_id' está na sessão.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Autenticação necessária"}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- Rotas de Autenticação ---

@app.route('/register', methods=['POST'])
def register():
    """Regista um novo utilizador."""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"error": "Faltam dados obrigatórios"}), 400

    user_id = models.create_user(mongo, username, email, password)

    if user_id is None:
        return jsonify({"error": "Utilizador ou email já existe"}), 409

    return jsonify({"message": "Utilizador criado com sucesso", "user_id": str(user_id)}), 201

@app.route('/login', methods=['POST'])
def login():
    """Autentica um utilizador e cria uma sessão."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = models.find_user(mongo, username)

    if user and models.verify_password(user['password'], password):
        session['user_id'] = str(user['_id'])
        session['username'] = user['username']
        return jsonify({"message": f"Login bem-sucedido. Bem-vindo, {user['username']}!"}), 200
    
    return jsonify({"error": "Credenciais inválidas"}), 401

@app.route('/logout', methods=['GET'])
def logout():
    """Encerra a sessão do utilizador."""
    session.clear()
    return jsonify({"message": "Logout bem-sucedido"}), 200

# --- Rotas de Receitas (Públicas) ---

@app.route('/roll-random', methods=['GET'])
def roll_random():
    """Retorna uma receita aleatória."""
    recipe = models.get_random_recipe(mongo)
    if recipe:
        return jsonify(recipe), 200
    return jsonify({"error": "Nenhuma receita encontrada"}), 404

@app.route('/roll-by-ingredient', methods=['POST'])
def roll_by_ingredient():
    """Retorna uma receita aleatória baseada num ingrediente."""
    data = request.get_json()
    ingredient = data.get('ingredient')

    if not ingredient:
        return jsonify({"error": "Ingrediente não fornecido"}), 400

    recipe = models.get_recipe_by_ingredient(mongo, ingredient)
    if recipe:
        return jsonify(recipe), 200
    return jsonify({"error": f"Nenhuma receita encontrada com o ingrediente '{ingredient}'"}), 404

@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    """Retorna uma lista de todos os ingredientes únicos."""
    ingredients = models.get_unique_ingredients(mongo)
    return jsonify(ingredients), 200

# --- Rotas de Favoritos (Protegidas) ---

@app.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    """Retorna as receitas favoritas do utilizador autenticado."""
    user_id = session['user_id']
    favorites = models.get_user_favorites(mongo, user_id)
    return jsonify(favorites), 200

@app.route('/add-favorite', methods=['POST'])
@login_required
def add_favorite_route():
    """Adiciona uma receita aos favoritos do utilizador."""
    data = request.get_json()
    recipe_name = data.get('recipe_name')
    if not recipe_name:
        return jsonify({"error": "Nome da receita não fornecido"}), 400

    user_id = session['user_id']
    models.add_favorite(mongo, user_id, recipe_name)
    return jsonify({"message": f"'{recipe_name}' adicionada aos favoritos."}), 200

@app.route('/remove-favorite', methods=['POST'])
@login_required
def remove_favorite_route():
    """Remove uma receita dos favoritos do utilizador."""
    data = request.get_json()
    recipe_name = data.get('recipe_name')
    if not recipe_name:
        return jsonify({"error": "Nome da receita não fornecido"}), 400

    user_id = session['user_id']
    models.remove_favorite(mongo, user_id, recipe_name)
    return jsonify({"message": f"'{recipe_name}' removida dos favoritos."}), 200

@app.route('/is-favorite/<path:recipe_name>', methods=['GET'])
@login_required
def is_favorite_route(recipe_name):
    """Verifica se uma receita está nos favoritos do utilizador."""
    user_id = session['user_id']
    is_fav = models.is_favorite(mongo, user_id, recipe_name)
    return jsonify({"is_favorite": is_fav}), 200

# --- Ponto de Entrada ---

if __name__ == '__main__':
    # O modo debug não é recomendado para produção
    app.run(debug=True)