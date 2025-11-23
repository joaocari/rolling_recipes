# rolling_recipes
# 🎲 Rolling Recipes

Bem-vindo ao **Rolling Recipes**, uma aplicação web moderna e interativa desenhada para o ajudar a descobrir a sua próxima receita portuguesa favorita. Se alguma vez se sentiu indeciso sobre o que cozinhar, esta é a solução perfeita para si!

## ✨ Sobre o Projeto

O Rolling Recipes nasceu da ideia de tornar a descoberta de novas receitas uma experiência divertida e surpreendente. Com um simples clique, pode "rolar os dados" e receber uma sugestão de receita aleatória da nossa coleção cuidadosamente selecionada.

A aplicação permite não só encontrar inspiração, mas também filtrar receitas por ingredientes específicos, guardar as suas favoritas para mais tarde e até contribuir para a nossa base de dados, sugerindo as suas próprias receitas.

---

## 🚀 Funcionalidades Principais

*   **Sorteador de Receitas**: Obtenha uma receita aleatória com um clique.
*   **Filtro por Ingrediente**: Quer usar aquele frango que tem no frigorífico? Filtre o sorteio para receber apenas receitas que o contenham.
*   **Autenticação de Utilizador**: Crie uma conta, faça login e tenha uma experiência personalizada.
*   **Sistema de Favoritos**: Guarde as receitas que mais gosta numa lista pessoal para acesso rápido.
*   **Sugestão de Receitas**: Tem uma receita incrível para partilhar? Envie-a através do nosso formulário e ajude a comunidade a crescer!
*   **Design Responsivo**: Aceda ao site a partir de qualquer dispositivo, seja ele um computador, tablet ou telemóvel.

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com uma combinação de tecnologias modernas para garantir uma experiência robusta e fluida:

*   **Backend**:
    *   **Python**: A linguagem de programação principal.
    *   **Flask**: Um micro-framework leve e poderoso para a lógica do servidor.
    *   **Flask-PyMongo**: Para a integração perfeita com a base de dados MongoDB.
    *   **Flask-Login**: Para gerir as sessões e autenticação dos utilizadores.

*   **Base de Dados**:
    *   **MongoDB**: Uma base de dados NoSQL flexível, ideal para armazenar as nossas receitas.

*   **Frontend**:
    *   **HTML5**: Para a estrutura semântica das páginas.
    *   **CSS3**: Para a estilização e o design moderno, incluindo Flexbox e animações.
    *   **Bootstrap 5**: Para criar um layout responsivo e componentes de interface consistentes.
    *   **JavaScript**: Para a interatividade dinâmica, como o sorteio de receitas e a comunicação com o backend.

---

## ⚙️ Como Executar o Projeto Localmente

Para executar o Rolling Recipes no seu próprio computador, siga estes passos:

1.  **Clonar o Repositório**
    ```bash
    git clone https://github.com/seu-usuario/rolling-recipes.git
    cd rolling-recipes
    ```

2.  **Criar e Ativar um Ambiente Virtual**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar as Dependências**
    Crie um ficheiro `requirements.txt` com o conteúdo abaixo e depois execute o comando de instalação.
    ```
    # requirements.txt
    Flask
    Flask-PyMongo
    Flask-Login
    Werkzeug
    pymongo[srv]
    ```
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar a Base de Dados**
    *   Certifique-se de que tem o MongoDB instalado e a correr localmente ou tenha uma string de conexão para uma base de dados na nuvem (como no MongoDB Atlas).
    *   **Para popular a base de dados com as receitas iniciais**, edite o ficheiro `data/seed_data.py`, insira a sua string de conexão na variável `MONGO_URI` e execute o script:
        ```bash
        python data/seed_data.py
        ```


    

---

## ✨ Agradecimentos

Este projeto é o resultado de muito trabalho, criatividade e colaboração.

### Criadores

Um enorme obrigado aos talentosos criadores por detrás do Rolling Recipes:

*   **João**
*   **Joana**

A sua visão e dedicação foram fundamentais para dar vida a esta aplicação.

### Recursos Externos

A experiência visual do nosso sorteador de receitas não seria a mesma sem a fantástica animação do dado. Gostaríamos de expressar a nossa gratidão ao **Mohsen Ghasem Zadeh**, o criador da animação "Dice" que encontrámos e utilizámos a partir do LottieFiles. O seu trabalho adicionou um toque de magia ao nosso projeto!

---

*&copy; 2025 Rolling Recipes. Todos os direitos reservados.*


