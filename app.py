# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_required, current_user
from bson import ObjectId
from bson.json_util import dumps
import random
import os, re

# Importa o Blueprint de autenticação
from auth import auth_bp
from models import User

# Cria a aplicação Flask
app = Flask(__name__,
            static_folder='static',
            template_folder='frontend')  # A pasta 'frontend' contém os templates HTML

# Chave secreta para a gestão de sessões (necessária para o Flask-Login)
# É recomendado usar uma variável de ambiente para a chave secreta em produção
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma-chave-secreta-muito-segura-e-dificil-de-adivinhar')

#--- Configuração do MongoDB ---
# Em produção, a URI deve vir de uma variável de ambiente para segurança.
mongo_uri = os.environ.get('MONGO_URI')
if not mongo_uri:
    # Fallback para a base de dados local se a variável de ambiente não estiver definida
    app.config["MONGO_URI"] = "mongodb://localhost:27017/rolling_recipes_db"
else:
    # Limpa a string de conexão para remover espaços ou quebras de linha acidentais
    app.config["MONGO_URI"] = mongo_uri.strip()

mongo = PyMongo()
mongo.init_app(app)

# --- Configuração do Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # Redireciona para esta rota se o acesso for negado

@login_manager.user_loader
def load_user(user_id):
    """Carrega o utilizador da base de dados para a sessão do Flask-Login."""
    user_doc = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user_doc:
        # Retorna uma instância da nossa classe User
        return User(user_doc)
    return None

# --- Registo dos Blueprints ---
app.register_blueprint(auth_bp, url_prefix='/auth')

# --- Rotas da Aplicação ---

# Rota principal que serve a página HTML
@app.route('/')
def index():
    # Renderiza o ficheiro index.html que está na pasta 'frontend'
    return render_template('index.html')

# Rota para a página de receitas favoritas
@app.route('/favorites')
@login_required # Garante que apenas utilizadores autenticados podem aceder
def favorites():
    # Obtém a lista de IDs de receitas favoritas do utilizador atual
    favorite_ids = current_user.favorites

    favorite_recipes = []
    if favorite_ids:
        # Busca todas as receitas cujos IDs estão na lista de favoritos
        favorite_recipes = list(mongo.db.receitas.find({
            "_id": {"$in": favorite_ids}
        }))

    # A lista de receitas é enviada diretamente para o template. O |tojson no HTML tratará da conversão.
    return render_template('favorites.html', recipes=favorite_recipes)

# Rota para a página de sugestões de receitas
@app.route('/suggestions')
@login_required # Garante que apenas utilizadores autenticados podem aceder
def suggestions():
    """Renderiza a página com o formulário de sugestão de receitas."""
    return render_template('suggestions.html')

# Rota da API para receber uma nova sugestão de receita
@app.route('/api/suggestions/add', methods=['POST'])
@login_required
def add_suggestion():
    """
    Recebe os dados do formulário de sugestão e guarda-os numa nova coleção.
    """
    data = request.get_json()

    # Validação simples dos dados recebidos
    if not data or not data.get('nome') or not data.get('ingredientes') or not data.get('instrucoes'):
        return jsonify({"error": "Os campos Nome, Ingredientes e Instruções são obrigatórios."}), 400

    # Cria o documento para ser inserido na base de dados
    suggestion_doc = {
        "nome": data.get('nome'),
        "categoria": data.get('categoria'),
        "dificuldade": data.get('dificuldade'),
        "tempo_preparo": data.get('tempo_preparo'),
        # Otimização: divide por vírgula ou quebra de linha, remove espaços e itens vazios.
        "ingredientes": [item.strip() for item in re.split(r'[,\n]+', data.get('ingredientes')) if item.strip()],
        "instrucoes": [item.strip() for item in re.split(r'[,\n]+', data.get('instrucoes')) if item.strip()],
        "link_receita": data.get('link_receita', ''), # Campo opcional
        "sugerido_por": current_user.username, # Guarda quem sugeriu
        "status": "pendente" # Status inicial
    }

    # Insere o documento na nova coleção 'sugestoes'
    mongo.db.sugestoes.insert_one(suggestion_doc)

    return jsonify({"message": "Sugestão enviada com sucesso! Obrigado pela sua contribuição."}), 201

# Rota da API para obter uma receita aleatória
@app.route('/api/recipe/random')
def get_random_recipe():
    """
    Obtém uma receita aleatória. Se um parâmetro 'ingredient' for fornecido na URL,
    filtra as receitas por esse ingrediente antes de fazer o sorteio.
    """
    recipes_collection = mongo.db.receitas
    ingredient = request.args.get('ingredient')

    # O aggregation pipeline permite construir consultas complexas passo a passo.
    pipeline = []

    if ingredient:
        # 1º Passo (opcional): Filtrar por ingrediente.
        # A busca usa uma expressão regular com a opção 'i' para ser case-insensitive.
        pipeline.append({
            "$match": {"ingredientes": {"$regex": ingredient, "$options": "i"}}
        })

    # 2º Passo: Obter 1 documento aleatório do resultado (filtrado ou da coleção inteira).
    pipeline.append({"$sample": {"size": 1}})

    random_recipe_list = list(recipes_collection.aggregate(pipeline))

    if not random_recipe_list:
        # Se a lista estiver vazia, retorna um erro.
        error_message = f"Nenhuma receita encontrada com o ingrediente '{ingredient}'." if ingredient else "Nenhuma receita encontrada na base de dados."
        return jsonify({"error": error_message}), 404 # A função deve parar aqui

    # Esta parte só é executada se a lista não estiver vazia
    recipe = random_recipe_list[0]

    # dumps converte o formato do MongoDB (BSON) para JSON
    return dumps(recipe)

# Rota da API para adicionar uma receita aos favoritos do utilizador
@app.route('/api/user/favorites/add', methods=['POST'])
@login_required
def add_favorite():
    data = request.get_json()
    recipe_id = data.get('recipe_id')

    if not recipe_id:
        return jsonify({"error": "ID da receita em falta."}), 400

    # Recarrega os dados do utilizador para garantir que a lista de favoritos está atualizada
    user_doc = mongo.db.users.find_one({"_id": ObjectId(current_user.id)})
    user_favorites = user_doc.get('favorites', [])

    # Verifica se o utilizador já atingiu o limite de 40 receitas favoritas
    if len(user_favorites) >= 40:
        return jsonify({"error": "Limite de 40 receitas favoritas atingido! Remova uma para poder adicionar outra."}), 400

    # Adiciona o ObjectId da receita ao array 'favorites' do utilizador
    # O operador $addToSet previne que a mesma receita seja adicionada várias vezes
    result = mongo.db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$addToSet": {"favorites": ObjectId(recipe_id)}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Receita adicionada aos favoritos!"}), 200
    else:
        return jsonify({"message": "Esta receita já estava nos seus favoritos."}), 200

# Rota da API para remover uma receita dos favoritos
@app.route('/api/user/favorites/remove', methods=['POST'])
@login_required
def remove_favorite():
    data = request.get_json()
    recipe_id = data.get('recipe_id')

    if not recipe_id:
        return jsonify({"error": "ID da receita em falta."}), 400

    # Recarrega os dados do utilizador para garantir que a lista de favoritos está atualizada
    user_doc = mongo.db.users.find_one({"_id": ObjectId(current_user.id)})
    user_favorites = user_doc.get('favorites', [])

    # Remove o ObjectId da receita do array 'favorites' do utilizador
    # O operador $pull remove todas as instâncias do valor do array
    result = mongo.db.users.update_one(
        {"_id": ObjectId(current_user.id)}, # A condição da busca continua a ser o ID do utilizador
        {"$pull": {"favorites": ObjectId(recipe_id)}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Receita removida dos favoritos."}), 200
    else:
        return jsonify({"error": "Não foi possível remover a receita ou já não era favorita."}), 404

if __name__ == '__main__':
    # Inicia o servidor em modo de debug
    print("A iniciar o servidor Flask...")
    app.run(debug=True)