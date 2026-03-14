# -*- coding: utf-8 -*-
import os
from pymongo import MongoClient
from bson import ObjectId
from utils import extrair_ingrediente # Importa a nossa nova função

def migrate_recipes_ingredients():
    """
    Este script percorre todas as receitas na coleção 'receitas' e converte
    o campo 'ingredientes' de uma lista de strings para uma lista de dicionários.
    """
    # --- Ligação à Base de Dados ---
    # Garante que usa a mesma string de conexão que a sua app
    mongo_uri = os.environ.get('MONGO_URI', "mongodb://localhost:27017/rolling_recipes_db")
    client = MongoClient(mongo_uri.strip())
    db = client.get_default_database() # Obtém a base de dados da URI
    receitas_collection = db.receitas

    print("A iniciar a migração dos ingredientes...")

    # Obtém todas as receitas da coleção
    receitas = list(receitas_collection.find())
    
    updated_count = 0

    for receita in receitas:
        # Verifica se o campo 'ingredientes' existe e é uma lista
        if 'ingredientes' in receita and isinstance(receita['ingredientes'], list):
            
            novos_ingredientes = []
            needs_update = False
            for item in receita['ingredientes']:
                # Apenas processa se o item for uma string (para não reprocessar)
                if isinstance(item, str):
                    needs_update = True
                    ingrediente_estruturado = extrair_ingrediente(item)
                    novos_ingredientes.append(ingrediente_estruturado)
                else:
                    # Se já for um dicionário, mantém como está
                    novos_ingredientes.append(item)
            
            if needs_update:
                # Atualiza o documento na base de dados com a nova lista de ingredientes
                receitas_collection.update_one(
                    {'_id': receita['_id']},
                    {'$set': {'ingredientes': novos_ingredientes}}
                )
                updated_count += 1
                print(f"Receita '{receita.get('nome')}' atualizada.")

    print(f"\nMigração concluída! {updated_count} receitas foram atualizadas.")

if __name__ == '__main__':
    migrate_recipes_ingredients()