# -*- coding: utf-8 -*-
import re

def extrair_ingrediente(texto_ingrediente: str) -> list[dict]:
    """
    Extrai quantidade, unidade e nome de uma ou mais strings de ingredientes,
    otimizado para formatos comuns em português.

    Args:
        texto_ingrediente: A string a ser processada (ex: "250g de açúcar",
                           "1 cebola grande", "Sal, pimenta a gosto").

    Returns:
        Uma LISTA de dicionários. Cada dicionário contém 'quantidade',
        'unidade' e 'nome'. A função retorna sempre uma lista.
    """
    # 1. Divide a string por vírgulas para lidar com múltiplos ingredientes.
    if ',' in texto_ingrediente:
        partes = [parte.strip() for parte in texto_ingrediente.split(',')]
    else:
        partes = [texto_ingrediente]

    lista_final_ingredientes = []

    # 2. Itera sobre cada parte (seja uma ou várias)
    for parte_str in partes:
        if not parte_str:  # Ignora partes vazias (ex: "sal, , pimenta")
            continue

        texto_limpo = parte_str.strip()

        # 3. Trata casos de "a gosto"
        nome_processado = re.sub(r'\s*\(?a gosto\)?$', '', texto_limpo, flags=re.IGNORECASE).strip()
        is_a_gosto = len(nome_processado) < len(texto_limpo)

        # 4. Regex melhorada para capturar (quantidade) (unidade) (nome)
        padrao = re.compile(
            r"^\s*(\d+[\.,]?\d*)?"  # Grupo 1: Quantidade (opcional)
            r"\s*"
            r"(g|kg|ml|l|un|unidades?|colher(?:es)?|xícaras?|chávenas?)?"  # Grupo 2: Unidade (opcional)
            r"\s*"
            r"(?:de\s)?"  # Ignora a preposição "de"
            r"(.*)$",  # Grupo 3: Nome do ingrediente
            re.IGNORECASE
        )

        match = padrao.match(nome_processado)

        if not match:
            # Se a regex falhar, retorna o nome original sem quantidade/unidade
            resultado = {"quantidade": 0, "unidade": None, "nome": nome_processado}
            lista_final_ingredientes.append(resultado)
            continue

        quantidade_str, unidade_str, nome_str = match.groups()

        # 5. Processa os valores capturados
        quantidade = 0.0
        if quantidade_str:
            try:
                quantidade = float(quantidade_str.replace(',', '.'))
            except (ValueError, TypeError):
                pass  # Mantém 0.0 se a conversão falhar

        if is_a_gosto:
            quantidade = 0.0

        # 6. Infere a unidade se não for explícita mas houver quantidade
        unidade_final = unidade_str.lower() if unidade_str else None
        if quantidade > 0 and not unidade_final:
            unidade_final = "un"  # Assume "unidade(s)"

        resultado = {
            "quantidade": quantidade,
            "unidade": unidade_final,
            "nome": nome_str.strip() if nome_str else "" # Garante que o nome não é None
        }
        lista_final_ingredientes.append(resultado)

    return lista_final_ingredientes

def gerar_lista_compras(lista_de_receitas: list) -> list:
    """
    Gera uma lista de compras consolidada a partir de uma lista de receitas.

    Agrupa ingredientes por nome (case-insensitive) e unidade, somando as quantidades.

    Args:
        lista_de_receitas: Uma lista de dicionários de receitas. Espera-se que
                           cada receita tenha uma chave 'ingredientes' contendo
                           uma lista de strings ou uma lista de dicionários já estruturados.

    Returns:
        Uma lista de dicionários, onde cada dicionário representa um item
        da lista de compras com a quantidade total.
    """
    lista_agregada = {}

    def normalizar_ingrediente(nome, unidade, quantidade):
        """Função auxiliar para padronizar nomes e unidades de ingredientes."""
        # 1. Normalização do nome
        nome_norm = nome.lower().strip()

        # Remove "a gosto" e variações
        nome_norm = re.sub(r'\s*\(?a gosto\)?$', '', nome_norm).strip()

        # Remove palavras descritivas comuns do final
        palavras_a_remover = [
            'grande', 'pequena', 'médio', 'média', 'picado', 'picada', 'picados', 'picadas',
            'fatiado', 'fatiada', 'ralado', 'ralada', 'fino', 'fina', 'grosso', 'grossa',
            'fresco', 'fresca'
        ]
        # Loop para remover palavras repetidas no final (ex: "picado fino")
        for _ in range(3): # Limita a 3 iterações para segurança
            for palavra in palavras_a_remover:
                if nome_norm.endswith(f" {palavra}"):
                    nome_norm = nome_norm[:-len(f" {palavra}")].strip()

        # Regras específicas de substituição
        if nome_norm.startswith('dente de ') or nome_norm.startswith('dentes de '):
            nome_norm = nome_norm.replace('dente de ', '').replace('dentes de ', '')

        # 2. Normalização da unidade
        unidade_norm = unidade.lower() if unidade else None
        if unidade_norm in ['unidade', 'unidades']:
            unidade_norm = 'un'

        return nome_norm, unidade_norm

    for receita in lista_de_receitas:
        if 'ingredientes' not in receita:
            continue

        for item_ingrediente in receita['ingredientes']:
            lista_de_objetos = []
            # A função é flexível: funciona se os ingredientes já estiverem
            # estruturados (lista de dicts) ou se ainda forem strings.
            if isinstance(item_ingrediente, str):
                # extrair_ingrediente agora retorna uma lista, então iteramos sobre ela
                lista_de_objetos = extrair_ingrediente(item_ingrediente)
            elif isinstance(item_ingrediente, dict):
                # Se for um dict (formato antigo), envolvemos numa lista para consistência
                lista_de_objetos = [item_ingrediente]
            elif isinstance(item_ingrediente, list):
                # Garante que processamos corretamente listas mistas
                for sub_item in item_ingrediente:
                    if isinstance(sub_item, str):
                        lista_de_objetos.extend(extrair_ingrediente(sub_item))
                    elif isinstance(sub_item, dict):
                        lista_de_objetos.append(sub_item)
            else:
                continue

            # Percorre a lista de ingredientes (pode ter 1 ou mais)
            for ingrediente_obj in lista_de_objetos:
                nome = ingrediente_obj.get('nome', "")
                unidade = ingrediente_obj.get('unidade')
                quantidade = ingrediente_obj.get('quantidade', 0)

                if not nome:
                    continue

                # Normaliza o nome e a unidade para criar a chave de agrupamento
                nome_normalizado, unidade_normalizada = normalizar_ingrediente(nome, unidade, quantidade)

                # A chave de agrupamento usa os valores normalizados
                chave_agrupamento = (nome_normalizado, unidade_normalizada)

                if chave_agrupamento not in lista_agregada:
                    # Guarda o primeiro nome "bonito" que encontrarmos para este grupo
                    lista_agregada[chave_agrupamento] = {
                        'nome': nome,  # Guarda o nome original para exibição
                        'unidade': unidade_normalizada,
                        'quantidade': 0
                    }

                # Soma a quantidade
                lista_agregada[chave_agrupamento]['quantidade'] += quantidade

    # Converte o dicionário de volta para uma lista e ordena alfabeticamente pelo nome
    return sorted(lista_agregada.values(), key=lambda item: item['nome'])