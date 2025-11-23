# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def get_recipes():
    """
    Retorna uma lista de dicionários com as receitas portuguesas.
    """
    return [
        {
            "nome": "Bacalhau à Brás",
            "categoria": "Peixe",
            "dificuldade": "Média",
            "tempo_preparo": "45 min",
            "ingredientes": [
                "600g de bacalhau dessalgado",
                "200g de batata palha",
                "6 ovos",
                "1 cebola grande cortada em rodelas finas",
                "4 dentes de alho picados",
                "Azeitonas pretas a gosto",
                "Azeite extra virgem a gosto",
                "Salsa picada a gosto",
                "Sal e pimenta do reino a gosto"
            ],
            "instrucoes": [
                "Cozinhe o bacalhau em água a ferver. Assim que levantar fervura, desligue o lume e reserve por 15 minutos.",
                "Retire o bacalhau da água, deixe arrefecer, retire a pele e as espinhas e desfie.",
                "Numa frigideira grande, aqueça o azeite e refogue a cebola e o alho até ficarem macios e translúcidos.",
                "Adicione o bacalhau desfiado ao refogado e envolva bem.",
                "Junte a batata palha e misture cuidadosamente.",
                "Bata os ovos, tempere com sal e pimenta e deite sobre o preparado na frigideira, mexendo sempre em lume brando.",
                "O objetivo é que os ovos cozinhem lentamente e o prato fique cremoso, não seco.",
                "Retire do lume, adicione as azeitonas e a salsa picada.",
                "Sirva de imediato."
            ]
        },
        {
            "nome": "Arroz de Pato",
            "categoria": "Carne",
            "dificuldade": "Média",
            "tempo_preparo": "2 horas",
            "ingredientes": [
                "1 pato com cerca de 2kg",
                "400g de arroz carolino ou agulha",
                "1 chouriço de carne",
                "150g de presunto ou bacon em cubos",
                "1 cebola grande",
                "2 dentes de alho",
                "1 folha de louro",
                "Azeite a gosto",
                "Sal e pimenta a gosto",
                "Rodelas de chouriço para decorar"
            ],
            "instrucoes": [
                "Coza o pato numa panela com água, a cebola cortada em quartos, os alhos, o louro, o chouriço inteiro e o presunto. Tempere com sal e pimenta.",
                "Numa panela, coza o pato em água com a cebola, os alhos, o louro, o chouriço e o presunto. Tempere com sal e pimenta.",
                "Quando o pato estiver bem cozido e macio, retire-o juntamente com o chouriço e o presunto. Coe o caldo da cozedura e reserve.",
                "Desfie a carne do pato, corte o chouriço cozido em rodelas e o presunto em pedaços.",
                "Meça o volume do arroz e utilize o dobro do volume em caldo da cozedura do pato para o cozer.",
                "Num tacho, faça um refogado ligeiro com um fio de azeite e um pouco de cebola picada (opcional). Adicione o arroz, deixe fritar um pouco e junte o caldo a ferver.",
                "Quando o arroz estiver quase seco, junte o pato desfiado e metade do chouriço e presunto. Envolva bem.",
                "Transfira o arroz para um tabuleiro de ir ao forno, decore a superfície com as restantes rodelas de chouriço.",
                "Transfira o arroz para um tabuleiro de forno e decore a superfície com as restantes rodelas de chouriço.",
                "Leve ao forno pré-aquecido a 200°C para tostar por cima, cerca de 10-15 minutos."
            ]
        },
        {
            "nome": "Caldo Verde",
            "categoria": "Sopa",
            "dificuldade": "Fácil",
            "tempo_preparo": "30 min",
            "ingredientes": [
                "500g de batata",
                "300g de couve-galega cortada em tiras finas",
                "1 cebola média",
                "2 dentes de alho",
                "1 chouriço de carne de boa qualidade",
                "Azeite a gosto",
                "Sal q.b."
            ],
            "instrucoes": [
                "Descasque as batatas, a cebola e os alhos. Corte tudo em pedaços.",
                "Coloque os legumes numa panela, cubra com água e tempere com sal. Deixe cozer até as batatas estarem bem macias.",
                "Retire a panela do lume e passe a sopa com a varinha mágica até obter um puré cremoso.",
                "Leve a panela de novo ao lume. Quando levantar fervura, junte a couve e um fio generoso de azeite.",
                "Deixe cozer a couve por cerca de 5 a 7 minutos.",
                "Entretanto, corte o chouriço em rodelas finas.",
                "Sirva a sopa bem quente, com umas rodelas de chouriço em cada prato e um fio de azeite."
            ]
        },
        {
            "nome": "Francesinha",
            "categoria": "Carne",
            "dificuldade": "Difícil",
            "tempo_preparo": "1 hora",
            "ingredientes": [
                "2 fatias de pão de forma grosso",
                "1 bife de vaca fino",
                "1 linguiça",
                "1 salsicha fresca",
                "2 fatias de fiambre",
                "4 fatias de queijo flamengo",
                "Para o molho:",
                "1 cebola pequena",
                "1 dente de alho",
                "Azeite, 1 folha de louro",
                "1 cebola pequena picada",
                "1 dente de alho picado",
                "Azeite",
                "1 folha de louro",
                "1 cerveja (33cl)",
                "50ml de vinho do Porto",
                "200ml de polpa de tomate",
                "1 cubo de caldo de carne",
                "Piri-piri a gosto"
                "Piri-piri a gosto",
                "Ovo estrelado (opcional)",
                "Batatas fritas para acompanhar"
            ],
            "instrucoes": [
                "Molho: Refogue a cebola e o alho picados em azeite com o louro. Junte a polpa de tomate, a cerveja, o vinho do Porto, o caldo de carne e o piri-piri. Deixe ferver em lume brando por 20-30 minutos. Passe o molho com a varinha mágica e retifique o sal.",
                "Molho: Refogue a cebola e o alho em azeite com o louro.",
                "Molho: Junte a polpa de tomate, a cerveja, o vinho do Porto, o caldo de carne e o piri-piri.",
                "Molho: Deixe ferver em lume brando por 20-30 minutos e depois passe com a varinha mágica. Retifique o sal.",
                "Grelhe o bife, a linguiça e a salsicha fresca.",
                "Monte a sanduíche: torre ligeiramente uma fatia de pão, coloque o bife, a linguiça e a salsicha abertas ao meio, e o fiambre. Tape com a outra fatia de pão.",
                "Cubra toda a sanduíche com as fatias de queijo.",
                "Leve a gratinar ao forno até o queijo derreter.",
                "Retire do forno, regue abundantemente com o molho bem quente. Sirva com um ovo estrelado por cima (opcional) e batatas fritas."
                "Retire do forno, regue abundantemente com o molho bem quente.",
                "Sirva com um ovo estrelado por cima (opcional) e batatas fritas."
            ]
        },
        {
            "nome": "Amêijoas à Bulhão Pato",
            "categoria": "Marisco",
            "dificuldade": "Fácil",
            "tempo_preparo": "25 min",
            "ingredientes": [
                "1kg de amêijoas",
                "4 dentes de alho",
                "1 molho de coentros",
                "100ml de vinho branco",
                "Azeite extra virgem a gosto",
                "Sumo de 1/2 limão",
                "Sal e pimenta q.b."
            ],
            "instrucoes": [
                "Deixe as amêijoas de molho em água com sal durante pelo menos 1 hora para largarem a areia. Lave-as bem depois.",
                "Num tacho largo, aqueça um fundo generoso de azeite. Junte os alhos laminados e deixe alourar ligeiramente.",
                "Adicione as amêijoas, os coentros picados (reserve um pouco para o final), o vinho branco, sal e pimenta.",
                "Tape o tacho e cozinhe em lume forte, agitando o tacho ocasionalmente, até as amêijoas abrirem (cerca de 5-8 minutos).",
                "Descarte as amêijoas que não abriram.",
                "Regue com o sumo de limão, polvilhe com mais coentros frescos e sirva imediatamente com fatias de pão para ensopar no molho."
            ]
        },
        {
            "nome": "Cozido à Portuguesa",
            "categoria": "Carne",
            "dificuldade": "Difícil",
            "tempo_preparo": "3 horas",
            "ingredientes": [
                "500g de carne de vaca para cozer",
                "500g de entrecosto de porco",
                "1 orelha de porco",
                "1 chouriço de carne",
                "1 morcela",
                "1 farinheira",
                "1 couve portuguesa ou lombarda",
                "4 batatas médias",
                "4 cenouras",
                "2 nabos",
                "Arroz branco para acompanhar"
            ],
            "instrucoes": [
                "Numa panela grande com água e sal, coza as carnes de porco e de vaca. Vá retirando a espuma que se forma à superfície.",
                "A meio da cozedura das carnes, junte os enchidos (pique a farinheira e a morcela para não rebentarem).",
                "À medida que as carnes e os enchidos ficam cozidos, retire-os para uma travessa e reserve o caldo.",
                "No caldo da cozedura das carnes, coza os legumes: primeiro as cenouras e os nabos, e por último as batatas e a couve.",
                "Pode também cozer o arroz no mesmo caldo para mais sabor.",
                "Sirva tudo numa travessa grande: as carnes e os enchidos fatiados, rodeados pelos legumes cozidos. O arroz serve-se à parte."
            ]
        },
        {
            "nome": "Feijoada à Transmontana",
            "categoria": "Carne",
            "dificuldade": "Média",
            "tempo_preparo": "2h 30min (+ demolhar)",
            "ingredientes": [
                "500g de feijão vermelho seco",
                "1 orelha de porco",
                "1 pé de porco (chispe)",
                "300g de entrecosto",
                "1 chouriço de carne",
                "1 morcela",
                "1 cebola grande",
                "2 dentes de alho",
                "1 cebola grande picada",
                "2 dentes de alho picados",
                "1 folha de louro",
                "Azeite, sal, pimenta, polpa de tomate",
                "Couve lombarda ou portuguesa"
                "Azeite",
                "Polpa de tomate a gosto",
                "Sal e pimenta a gosto",
                "Couve lombarda ou portuguesa cortada"
            ],
            "instrucoes": [
                "Demolhe o feijão e as carnes salgadas de véspera.",
                "De véspera, demolhe o feijão e as carnes salgadas em recipientes separados.",
                "Coza o feijão em água. Em panelas separadas, coza as carnes.",
                "Faça um refogado com azeite, cebola picada, alho e a folha de louro. Adicione um pouco de polpa de tomate.",
                "Faça um refogado com azeite, cebola, alho e louro. Adicione um pouco de polpa de tomate.",
                "Junte ao refogado as carnes cozidas e cortadas em pedaços e os enchidos em rodelas. Deixe apurar um pouco.",
                "Adicione o feijão cozido com um pouco da sua água de cozedura.",
                "Acrescente a couve cortada em pedaços e deixe cozinhar até estar tenra.",
                "Retifique os temperos e sirva bem quente, acompanhado de arroz branco."
            ]
        },
        {
            "nome": "Cataplana de Marisco",
            "categoria": "Marisco",
            "dificuldade": "Média",
            "tempo_preparo": "40 min",
            "ingredientes": [
                "500g de amêijoas",
                "500g de camarão",
                "500g de peixe branco em postas (ex: tamboril)",
                "1 cebola grande",
                "2 dentes de alho",
                "1 pimento vermelho",
                "2 tomates maduros",
                "1 cebola grande em rodelas",
                "2 dentes de alho picados",
                "1 pimento vermelho em tiras",
                "2 tomates maduros (sem pele e sementes) em pedaços",
                "100ml de vinho branco",
                "Azeite, sal, pimenta, coentros"
                "Azeite a gosto",
                "Sal e pimenta a gosto",
                "Coentros picados"
            ],
            "instrucoes": [
                "Na base da cataplana (ou num tacho largo), faça um refogado com azeite, a cebola em rodelas, os alhos picados e o pimento em tiras.",
                "Quando a cebola estiver macia, adicione o tomate em pedaços, sem pele nem sementes.",
                "Numa cataplana (ou tacho largo), refogue em azeite a cebola, os alhos e o pimento.",
                "Quando a cebola estiver macia, adicione o tomate e deixe cozinhar um pouco.",
                "Disponha as postas de peixe sobre o refogado, seguidas do camarão e das amêijoas.",
                "Tempere com sal e pimenta, regue com o vinho branco e polvilhe com coentros picados.",
                "Feche a cataplana e leve a lume brando por cerca de 15-20 minutos, até o peixe estar cozido e as amêijoas abertas.",
                "Sirva diretamente da cataplana, acompanhado de pão ou batatas cozidas."
            ]
        },
        {
            "nome": "Polvo à Lagareiro",
            "categoria": "Marisco",
            "dificuldade": "Média",
            "tempo_preparo": "1h 30min",
            "ingredientes": [
                "1 polvo com cerca de 1.5kg",
                "1kg de batatas pequenas (para assar)",
                "6 dentes de alho",
                "Azeite extra virgem abundante",
                "Sal grosso q.b.",
                "Salsa ou coentros picados"
            ],
            "instrucoes": [
                "Coza o polvo numa panela com água a ferver (sem sal) e uma cebola inteira com casca, até estar tenro (cerca de 40-60 minutos).",
                "Coza o polvo em água a ferver (sem sal) com uma cebola inteira, até estar tenro (40-60 min).",
                "Lave bem as batatas e coza-as com a pele em água e sal. Depois de cozidas, escorra-as e dê um 'murro' em cada uma para as abrir ligeiramente.",
                "Coloque o polvo cozido e as batatas num tabuleiro de ir ao forno.",
                "Esmague os dentes de alho com casca e espalhe-os pelo tabuleiro.",
                "Regue tudo muito generosamente com azeite.",
                "Leve ao forno pré-aquecido a 200°C por cerca de 20 minutos, ou até as batatas estarem douradas e o polvo ligeiramente tostado.",
                "Sirva polvilhado com salsa ou coentros picados."
            ]
        },
        {
            "nome": "Pastel de Nata",
            "categoria": "Doce",
            "dificuldade": "Média",
            "tempo_preparo": "40 min",
            "ingredientes": [
                "1 rolo de massa folhada redonda",
                "500ml de leite",
                "250g de açúcar",
                "6 gemas de ovo",
                "40g de farinha Maizena (amido de milho)",
                "1 casca de limão",
                "1 pau de canela"
            ],
            "instrucoes": [
                "Forre formas de queques com a massa folhada. Pique o fundo com um garfo.",
                "Leve ao lume o leite com a casca de limão e o pau de canela. Deixe ferver.",
                "Numa tigela, misture o açúcar com a Maizena. Adicione as gemas e bata bem.",
                "Retire o leite do lume. Verta um pouco da mistura de gemas no leite, mexendo sempre, e depois junte o resto, para temperar as gemas sem as cozer.",
                "Leve o creme de novo a lume brando, mexendo sempre até engrossar.",
                "Retire a casca de limão e o pau de canela. Deixe o creme arrefecer um pouco.",
                "Encha as formas com o creme.",
                "Leve ao forno pré-aquecido no máximo (250°C ou mais) por cerca de 10-15 minutos, até a massa estar dourada e o creme queimado por cima.",
                "Deixe arrefecer antes de servir. Polvilhe com canela em pó e açúcar em pó a gosto."
            ]
        }
    ]

# This block only runs when you execute `python data/seed_data.py` directly.
if __name__ == '__main__':
    # --- MongoDB Configuration ---
    # COLOQUE A SUA STRING DE CONEXÃO ONLINE AQUI, COM A PASSWORD CORRETA
    MONGO_URI = "mongodb+srv://olatvcasa:abKdpjPB6dr7lcY@rollingrecipes.dkqabli.mongodb.net/rolling_recipes_db?retryWrites=true&w=majority/"
    DB_NAME = "rolling_recipes_db"
    COLLECTION_NAME = "receitas"

    try:
        print("A tentar conectar à base de dados MongoDB...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000) # Timeout de 5 segundos
        
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("Conexão com MongoDB estabelecida com sucesso.")

        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        print(f"A limpar a coleção '{COLLECTION_NAME}'...")
        collection.drop()
        
        recipes_data = get_recipes()
        print(f"A inserir {len(recipes_data)} novas receitas...")
        collection.insert_many(recipes_data)
        
        print("Base de dados populada com sucesso!")

    except ConnectionFailure as e:
        print(f"\nERRO: Não foi possível conectar ao MongoDB.")
        print("Por favor, verifique se o serviço MongoDB está a correr e acessível na porta 27017.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
