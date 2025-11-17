// Espera que o DOM esteja completamente carregado para executar o script
document.addEventListener('DOMContentLoaded', () => {

    // Elementos DOM
    const diceElement = document.getElementById('dice');
    const rollButton = document.getElementById('rollButton');
    const recipeResultElement = document.getElementById('recipeResult');

    let isRolling = false;

    async function rollDice() {
        if (isRolling) return;
        
        isRolling = true;
        rollButton.disabled = true;
        rollButton.textContent = "A GIRAR...";
    
        // Efeito de rotação
        diceElement.textContent = "🎲";
        diceElement.classList.add('rolling');
        recipeResultElement.innerHTML = '<p style="text-align: center;">🎲 A contactar a cozinha...</p>';
    
        try {
            // Faz o pedido à nossa API para obter uma receita aleatória
            const response = await fetch('/api/recipe/random');
            if (!response.ok) {
                throw new Error(`Erro na rede: ${response.statusText}`);
            }
            const recipe = await response.json();
    
            // Adiciona um pequeno atraso para a animação ser visível
            setTimeout(() => {
                // Parar animação
                diceElement.classList.remove('rolling');
                // Mostra um número aleatório no dado, apenas para efeito visual
                diceElement.textContent = Math.floor(Math.random() * 10) + 1;
                
                // Mostrar receita
                displayRecipe(recipe);
                
                isRolling = false;
                rollButton.disabled = false;
                rollButton.textContent = "🎲 GIRAR";
            }, 1000); // 1 segundo de atraso
    
        } catch (error) {
            console.error("Falha ao obter receita:", error);
            recipeResultElement.innerHTML = `<p style="text-align: center; color: red;">Não foi possível obter a receita. O servidor está a funcionar?</p>`;
            // Parar animação
            diceElement.classList.remove('rolling');
            diceElement.textContent = "?";
            isRolling = false;
            rollButton.disabled = false;
            rollButton.textContent = "🎲 GIRAR";
        }
    }

    function displayRecipe(recipe) {
        // Mapear dificuldade para cores
        const difficultyColors = {
            'Fácil': '#388e3c',   // Verde
            'Média': '#f57c00',   // Laranja
            'Difícil': '#d32f2f' // Vermelho
        };

        // Os campos 'dificuldade' e 'tempo_preparo' não estão no seed_data.py original.
        // Usamos valores padrão se não existirem.
        const dificuldade = recipe.dificuldade || 'N/A';
        const tempo_preparo = recipe.tempo_preparo || 'N/A';
        const difficultyColor = difficultyColors[dificuldade] || '#666';

        // Gerar HTML para os ingredientes e instruções
        const ingredientsHtml = recipe.ingredientes.map(ing => `<li>${ing}</li>`).join('');
        const instructionsHtml = recipe.instrucoes.map(step => `<li>${step}</li>`).join('');

        recipeResultElement.innerHTML = `
            <h3 style="color: #d27f1a; text-align: center; font-size: 1.5rem;">${recipe.nome}</h3>
            
            <div class="recipe-meta">
                <span class="category-tag">${recipe.categoria}</span>
                <span class="difficulty-tag" style="background: ${difficultyColor}20; color: ${difficultyColor};">
                    ${dificuldade}
                </span>
                <span class="time-tag">${tempo_preparo}</span>
            </div>
            
            <div class="ingredients-list">
                <h4>🍴 Ingredientes</h4>
                <ul>
                    ${ingredientsHtml}
                </ul>
            </div>
            
            <div class="instructions-list">
                <h4>👩‍🍳 Modo de Preparo</h4>
                <ol>
                    ${instructionsHtml}
                </ol>
            </div>
            
            <div class="dice-result">
                🎲 Bom apetite! 🍳
            </div>
        `;
    }

    // Event listeners
    rollButton.addEventListener('click', rollDice);
    diceElement.addEventListener('click', rollDice);

    // Ativar o botão com a tecla Enter
    document.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isRolling) {
            rollDice();
        }
    });

    console.log('🎲 Rolling Recipes carregado e pronto a usar!');
});