# -*- coding: utf-8 -*-
from flask_login import UserMixin

class User(UserMixin):
    """
    Modelo de utilizador para integração com o Flask-Login.
    """
    def __init__(self, user_data):
        """
        Inicializa o objeto User a partir de dados do MongoDB.
        'user_data' é um dicionário vindo da base de dados.
        """
        self.id = str(user_data.get('_id'))
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        # Carrega a lista de favoritos, que são ObjectIds
        self.favorites = user_data.get('favorites', [])

    # O Flask-Login já implementa os métodos necessários através do UserMixin:
    # - is_authenticated: retorna True se o utilizador estiver autenticado.
    # - is_active: retorna True se a conta do utilizador estiver ativa.
    # - is_anonymous: retorna False para utilizadores reais.
    # - get_id(): retorna o ID do utilizador (em formato string).

    # Não é necessário mais nada para uma implementação básica.