document.addEventListener('DOMContentLoaded', function() {

    // --- LÓGICA COMUM A VÁRIAS PÁGINAS ---

    // Script para fazer a mensagem flash desaparecer após 3 segundos
    const flashMessage = document.getElementById('flash-message');
    if (flashMessage) {
        setTimeout(() => {
            const alert = new bootstrap.Alert(flashMessage);
            alert.close();
        }, 3000);
    }

    // --- LÓGICA DA PÁGINA INICIAL (INDEX.HTML) ---
    // Verificamos se os elementos da página inicial existem antes de adicionar eventos
    const getRecipeBtn = document.getElementById('get-recipe-btn');
    if (getRecipeBtn) {
        const searchForm = document.getElementById('search-form');
        const isAuthenticated = document.body.dataset.isAuthenticated === 'true';
        let currentRecipeId = null;

        function populateIngredients(ingredients) {
            const ingredientsList = document.getElementById('recipe-ingredients');
            ingredientsList.innerHTML = '';
            ingredients.forEach(ingredient => {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                if (typeof ingredient === 'object' && ingredient !== null && ingredient.nome) {
                    const quantity = ingredient.quantidade ? `${ingredient.quantidade} ` : '';
                    li.textContent = `${quantity}${ingredient.nome}`;
                } else {
                    li.textContent = ingredient;
                }
                ingredientsList.appendChild(li);
            });
        }

        function populateInstructions(steps) {
            const instructionsList = document.getElementById('recipe-instructions');
            instructionsList.innerHTML = '';
            steps.forEach(step => {
                const li = document.createElement('li');
                li.textContent = step;
                instructionsList.appendChild(li);
            });
        }

        async function fetchAndDisplayRecipe(apiUrl, triggerButton) {
            const originalButtonText = triggerButton.textContent;
            const recipeDisplay = document.getElementById('recipe-display');
            const lottieLoader = document.getElementById('lottie-loader');
            const messageDisplay = document.getElementById('message-display');

            recipeDisplay.classList.add('d-none');
            messageDisplay.classList.add('d-none');
            lottieLoader.classList.remove('d-none');
            
            document.getElementById('get-recipe-btn').disabled = true;
            document.getElementById('search-recipe-btn').disabled = true;
            triggerButton.textContent = 'A sortear...';
            triggerButton.classList.add('is-sorting');

            try {
                const minimumDelay = new Promise(resolve => setTimeout(resolve, 4000));
                const [response] = await Promise.all([fetch(apiUrl), minimumDelay]);
                const data = await response.json();

                if (!response.ok) {
                    messageDisplay.textContent = data.error || 'Não foi possível obter a receita.';
                    messageDisplay.classList.remove('d-none');
                    lottieLoader.classList.add('d-none');
                    return;
                }

                const recipe = data;
                currentRecipeId = recipe._id.$oid || recipe._id;

                document.getElementById('recipe-title').textContent = recipe.nome;
                populateInstructions(recipe.instrucoes);
                populateIngredients(recipe.ingredientes);

                lottieLoader.classList.add('d-none');
                recipeDisplay.classList.remove('d-none');
                recipeDisplay.classList.add('fade-in');
                
                recipeDisplay.scrollIntoView({ behavior: 'smooth', block: 'start' });

            } catch (error) {
                console.error('Erro ao buscar receita:', error);
                messageDisplay.textContent = 'Ocorreu um erro de comunicação ao buscar a receita. Tente novamente.';
                messageDisplay.classList.remove('d-none');
                lottieLoader.classList.add('d-none');
            } finally {
                document.getElementById('get-recipe-btn').disabled = false;
                document.getElementById('search-recipe-btn').disabled = false;
                triggerButton.textContent = originalButtonText;
                triggerButton.classList.remove('is-sorting');
            }
        }

        getRecipeBtn.addEventListener('click', () => {
            fetchAndDisplayRecipe('/api/recipe/random', getRecipeBtn);
        });

        searchForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const ingredientInput = document.getElementById('ingredient-input');
            const searchBtn = document.getElementById('search-recipe-btn');
            const ingredient = ingredientInput.value.trim();

            if (!ingredient) {
                ingredientInput.setCustomValidity('Para filtrar, por favor preencha este campo.');
                ingredientInput.reportValidity();
                setTimeout(() => {
                    ingredientInput.setCustomValidity('');
                }, 2000);
                return;
            }

            let apiUrl = `/api/recipe/random?ingredient=${encodeURIComponent(ingredient)}`;
            fetchAndDisplayRecipe(apiUrl, searchBtn);
        });

        const favoriteBtn = document.getElementById('favorite-btn');
        favoriteBtn.addEventListener('click', async () => {
            if (!isAuthenticated) {
                alert('Para guardar receitas nos favoritos, precisa de entrar ou registar-se!');
                return;
            }

            if (!currentRecipeId) return;

            try {
                const response = await fetch('/api/user/favorites/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ recipe_id: currentRecipeId }),
                });
                const result = await response.json();

                if (response.ok) {
                    alert(result.message);
                } else {
                    throw new Error(result.error || 'Não foi possível adicionar aos favoritos.');
                }
            } catch (error) {
                console.error('Erro ao favoritar receita:', error);
                alert(error.message);
            }
        });

        const ingredientInput = document.getElementById('ingredient-input');
        ingredientInput.addEventListener('input', function () {
            const invalidCharsRegex = /[^A-Za-zÀ-ú\s-]/g;
            const currentValue = this.value;

            if (invalidCharsRegex.test(currentValue)) {
                this.setCustomValidity('Só são permitidas letras, espaços e hífens.');
                this.reportValidity();
                this.value = currentValue.replace(invalidCharsRegex, '');
                setTimeout(() => {
                    this.setCustomValidity('');
                }, 1500);
            }
        });
    }

    // --- LÓGICA DA PÁGINA DE SUGESTÕES (SUGGESTIONS.HTML) ---
    const suggestionForm = document.getElementById('suggestion-form');
    if (suggestionForm) {
        suggestionForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const submitButton = suggestionForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'A enviar...';

            const formData = new FormData(suggestionForm);
            const data = Object.fromEntries(formData.entries());

            if (!data.ingredientes.trim() || !data.instrucoes.trim()) {
                alert('Por favor, adicione pelo menos um ingrediente e uma instrução.');
                submitButton.disabled = false;
                submitButton.textContent = 'Enviar Sugestão';
                return;
            }

            try {
                const response = await fetch('/api/suggestions/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });
                const result = await response.json();

                if (response.ok) {
                    alert("Obrigado pela sua contribuição! A sua sugestão foi enviada com sucesso.");
                    suggestionForm.reset();
                } else {
                    alert(result.error || 'Não foi possível enviar a sugestão. Verifique os dados e tente novamente.');
                }
            } catch (error) {
                console.error('Erro ao enviar sugestão:', error);
                alert('Ocorreu um erro de comunicação. Por favor, verifique a sua ligação e tente novamente.');
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = 'Enviar Sugestão';
            }
        });

        const textareas = document.querySelectorAll('.auto-growing-textarea');
        textareas.forEach(textarea => {
            function autoGrow() {
                textarea.style.height = 'auto';
                textarea.style.height = (textarea.scrollHeight) + 'px';
            }
            textarea.addEventListener('input', autoGrow);
            autoGrow();
        });
    }

    // --- LÓGICA DA PÁGINA DE FAVORITOS (FAVORITES.HTML) ---
    const recipesDataElement = document.getElementById('recipes-data');
    if (recipesDataElement) {
        const recipesData = JSON.parse(recipesDataElement.textContent);
        const recipeModal = document.getElementById('recipeModal');
        const removeFavoriteBtn = document.getElementById('remove-favorite-btn');
        let currentRecipeId = null;

        async function removeRecipeFromFavorites(recipeId) {
            if (!confirm('Tem a certeza que quer remover esta receita dos favoritos?')) return;

            try {
                const response = await fetch('/api/user/favorites/remove', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ recipe_id: recipeId })
                });

                if (response.ok) {
                    const modalInstance = bootstrap.Modal.getInstance(recipeModal);
                    if (modalInstance && modalInstance._isShown) modalInstance.hide();
                    
                    const itemToRemove = document.getElementById(`recipe-item-${recipeId}`);
                    if (itemToRemove) itemToRemove.remove();
                    
                    const favoritesList = document.getElementById('favorites-list').querySelector('ul');
                    if (!favoritesList || favoritesList.children.length === 0) {
                        const noFavoritesMessage = document.getElementById('no-favorites-message');
                        if(noFavoritesMessage) noFavoritesMessage.classList.remove('d-none');
                    }
                } else {
                    const result = await response.json();
                    throw new Error(result.error || 'Não foi possível remover a receita.');
                }
            } catch (error) {
                console.error('Erro ao remover favorito:', error);
                alert(error.message);
            }
        }

        recipeModal.addEventListener('show.bs.modal', function (event) {
            const triggerElement = event.relatedTarget;
            currentRecipeId = triggerElement.dataset.id;
            const recipe = recipesData.find(r => r._id && r._id.$oid === currentRecipeId);
            if (!recipe) return;

            recipeModal.querySelector('.modal-title').textContent = recipe.nome || 'Receita sem nome';
            const modalIngredients = recipeModal.querySelector('#modal-ingredients');
            const modalInstructions = recipeModal.querySelector('#modal-instructions');

            modalIngredients.innerHTML = '';
            (recipe.ingredientes || []).forEach(ingredient => {
                const li = document.createElement('li');
                li.className = 'list-group-item px-0';
                if (typeof ingredient === 'object' && ingredient !== null && ingredient.nome) {
                    const quantity = ingredient.quantidade ? `${ingredient.quantidade} ` : '';
                    li.textContent = `${quantity}${ingredient.nome}`;
                } else {
                    li.textContent = ingredient;
                }
                modalIngredients.appendChild(li);
            });

            modalInstructions.innerHTML = '';
            (recipe.instrucoes || []).forEach(step => {
                const li = document.createElement('li');
                li.className = 'mb-1';
                li.textContent = step;
                modalInstructions.appendChild(li);
            });
        });

        removeFavoriteBtn.addEventListener('click', () => {
            if (currentRecipeId) removeRecipeFromFavorites(currentRecipeId);
        });

        document.querySelectorAll('.remove-favorite-list-btn').forEach(button => {
            button.addEventListener('click', (event) => {
                event.stopPropagation();
                const recipeId = event.currentTarget.dataset.id;
                removeRecipeFromFavorites(recipeId);
            });
        });

        document.querySelectorAll('.recipe-card.clickable').forEach(card => {
            card.addEventListener('click', function(event) {
                if (event.target.closest('button')) return;
                const recipeId = this.dataset.id;
                const modalTriggerButton = this.querySelector(`.view-recipe-btn[data-id="${recipeId}"]`);
                if (recipeModal && modalTriggerButton) {
                    new bootstrap.Modal(recipeModal).show(modalTriggerButton);
                }
            });
        });
    }
});