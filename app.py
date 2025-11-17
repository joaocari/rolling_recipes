# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
import random
import os

# Cria a aplicação Flask
app = Flask(__name__,
            static_folder='frontend',  # Pasta para ficheiros estáticos (CSS, JS, imagens)
            template_folder='frontend') # Pasta para o template HTML

# --- Configuração do MongoDB ---
# Altere a URI se a sua base de dados não estiver local
app.config["MONGO_URI"] = "mongodb://localhost:27017/rolling_recipes_db"
try:
    mongo = PyMongo(app)
except Exception as e:
    print(f"\nERRO CRÍTICO: Não foi possível inicializar a conexão com o MongoDB. Verifique se o serviço está a correr. Detalhes: {e}\n")

# --- Rotas da Aplicação ---

# Rota principal que serve a página HTML
@app.route('/')
def index():
    # Renderiza o ficheiro index.html que está na pasta 'frontend'
    return render_template('index.html')

# Rota da API para obter uma receita aleatória
@app.route('/api/recipe/random')
def get_random_recipe():
    recipes_collection = mongo.db.receitas
    # O '$sample' do MongoDB é perfeito para obter documentos aleatórios
    random_recipe = list(recipes_collection.aggregate([{"$sample": {"size": 1}}]))
    
    if not random_recipe:
        return jsonify({"error": "Nenhuma receita encontrada na base de dados."}), 404

    # dumps converte o formato do MongoDB (BSON) para JSON
    return dumps(random_recipe[0])

if __name__ == '__main__':
    # Inicia o servidor em modo de debug
    print("A iniciar o servidor Flask...")
    print(f"A procurar templates na pasta: {os.path.abspath(app.template_folder)}")
    app.run(debug=True)