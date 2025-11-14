# /rolling_recipe_app/models/models.py

from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime

# --- Funções de Utilizador e Autenticação ---

def hash_password(password):
    """Gera um hash seguro para a password."""
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    """Verifica se a password corresponde ao hash."""
    return check_password_hash(hashed_password, password)

def create_user(mongo, username, email, password):
    """
    Cria um novo utilizador na base de dados.
    Retorna o ID do utilizador criado ou None se o utilizador/email já existir.
    """
    # Verifica se o username ou email já existem
    if mongo.db.users.find_one({"$or": [{"username": username}, {"email": email}]}):
        return None

    hashed_pass = hash_password(password)
    user_id = mongo.db.users.insert_one({
        "username": username,
        "email": email,
        "password": hashed_pass
    }).inserted_id
    return user_id

def find_user(mongo, username):
    """Encontra um utilizador pelo seu username."""
    return mongo.db.users.find_one({"username": username})

# --- Funções de Receitas ---

def get_random_recipe(mongo):
    """
    Sorteia uma receita aleatória da coleção usando a agregação $sample.
    Retorna o documento da receita ou None se a coleção estiver vazia.
    """
    pipeline = [{"$sample": {"size": 1}}]
    try:
        recipe = next(mongo.db.recipes.aggregate(pipeline))
        # Converte ObjectId para string para ser serializável em JSON
        recipe['_id'] = str(recipe['_id'])
        return recipe
    except StopIteration:
        return None

def get_recipe_by_ingredient(mongo, ingredient):
    """
    Sorteia uma receita aleatória que contém um ingrediente específico.
    Retorna o documento da receita ou None se nenhuma for encontrada.
    """
    pipeline = [
        {"$match": {"ingredients": ingredient}},
        {"$sample": {"size": 1}}
    ]
    try:
        recipe = next(mongo.db.recipes.aggregate(pipeline))
        recipe['_id'] = str(recipe['_id'])
        return recipe
    except StopIteration:
        return None

def get_unique_ingredients(mongo):
    """
    Retorna uma lista de todos os ingredientes únicos da coleção de receitas.
    """
    pipeline = [
        {"$unwind": "$ingredients"},
        {"$group": {"_id": "$ingredients"}},
        {"$sort": {"_id": 1}}
    ]
    ingredients_cursor = mongo.db.recipes.aggregate(pipeline)
    return [doc['_id'] for doc in ingredients_cursor]

# --- Funções de Favoritos ---

def add_favorite(mongo, user_id, recipe_name):
    """
    Adiciona uma receita à lista de favoritos de um utilizador.
    Usa $setOnInsert para evitar duplicados.
    """
    mongo.db.favorites.update_one(
        {"user_id": ObjectId(user_id), "recipe_name": recipe_name},
        {
            "$setOnInsert": {
                "user_id": ObjectId(user_id),
                "recipe_name": recipe_name,
                "date_added": datetime.utcnow()
            }
        },
        upsert=True
    )

def remove_favorite(mongo, user_id, recipe_name):
    """Remove uma receita dos favoritos de um utilizador."""
    mongo.db.favorites.delete_one({"user_id": ObjectId(user_id), "recipe_name": recipe_name})

def get_user_favorites(mongo, user_id):
    """Retorna uma lista com os nomes das receitas favoritas de um utilizador."""
    favorites_cursor = mongo.db.favorites.find(
        {"user_id": ObjectId(user_id)},
        {"_id": 0, "recipe_name": 1} # Projeta apenas o campo recipe_name
    )
    return [fav['recipe_name'] for fav in favorites_cursor]

def is_favorite(mongo, user_id, recipe_name):
    """Verifica se uma receita específica está nos favoritos de um utilizador."""
    return mongo.db.favorites.find_one({
        "user_id": ObjectId(user_id),
        "recipe_name": recipe_name
    }) is not None