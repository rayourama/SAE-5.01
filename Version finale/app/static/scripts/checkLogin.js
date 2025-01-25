// Vérifie si l'utilisateur est connecté et met à jour l'interface utilisateur en conséquence
function checkLoginStatus() {
    // Envoie une requête pour vérifier l'état de connexion
    fetch('/check_login', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json()) // Convertit la réponse en JSON
    .then(data => {
        // Récupère les éléments interactifs de la page
        const filtersRight = document.getElementById('filters-right');
        const layout = document.getElementById('layout');
        const authButton = document.getElementById('auth-button'); // Bouton connexion/déconnexion
        const addToCategoryButton = document.getElementById('add-to-category-btn'); // Bouton "Ajouter à une catégorie"
        const favoriteStar = document.getElementById('favorite-star'); // Étoile de favori
        const emailButton = document.getElementById('user-email-button');

        if (data.loggedIn) {
            if (data.is_admin){
                window.location.href = `${BASE_URL}/admin`; // Redirige vers la page admin
                return;
            }

            // Si l'utilisateur est connecté
            console.log(`Connecté : ${data.email}`); // Affiche l'email de l'utilisateur connecté
            authButton.textContent = "Déconnexion"; // Change le texte du bouton en "Déconnexion"

            // Charge le mail de l'utilisateur
            if (emailButton) emailButton.textContent = data.email;

            // Affiche les filtres de droite
            if (filtersRight) filtersRight.style.display = 'block';
            if (layout) layout.className = "modified-layout"
            if (addToCategoryButton) addToCategoryButton.disabled = false;

            // Charge les catégories de l'utilisateur
            loadUserCategories().catch(error => {
                console.error('Erreur lors du chargement des catégories :', error);
            });

            // Active l'étoile de favori (cliquable et non grisée)
            if (favoriteStar) favoriteStar.style.pointerEvents = 'auto'; // Permet les clics
            if (favoriteStar) favoriteStar.style.opacity = '1'; // Affiche l'étoile normalement
        } else {
            // Si l'utilisateur n'est pas connecté
            console.log("Non connecté"); // Message dans la console
            authButton.textContent = "Connexion"; // Change le texte du bouton en "Connexion"

            // Masque les filtres de droites
            if (filtersRight) filtersRight.style.display = 'none';
            if (layout) layout.className = "layout";
            if (addToCategoryButton) addToCategoryButton.disabled = true;

            // Désactive l'étoile de favori (non cliquable et grisée)
            if (favoriteStar) favoriteStar.style.pointerEvents = 'none'; // Empêche les clics
            if (favoriteStar) favoriteStar.style.opacity = '0.5'; // Grise l'étoile
        }
    })
    .catch(error => {
        // Gère les erreurs de la requête réseau
        console.error('Erreur de vérification de connexion:', error);
    });
}

// Charge les catégories existantes de l'utilisateur
async function loadUserCategories() {
    const categoriesContainer = document.getElementById('user-categories-container');
    const userEmail = sessionStorage.getItem('user_email'); // Vérifie si l'utilisateur est connecté

    if (!userEmail) {
        categoriesContainer.style.display = 'none'; // Masquer le conteneur si l'utilisateur n'est pas connecté
        return;
    }

    // Si l'utilisateur est connecté, récupérer les catégories depuis le backend
    try {
        const response = await fetch('/categories', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Erreur lors du chargement des catégories.');
        }

        const data = await response.json();
        const categories = data.categories || []; // Récupérer les catégories ou une liste vide

        // Réinitialiser le conteneur pour les catégories
        categoriesContainer.innerHTML = '';

        // Afficher les catégories et ajouter les boutons correspondants
        categoriesContainer.style.display = 'block'; // Afficher le conteneur
        categories.forEach(category => {
            
            // Crée un conteneur pour chaque catégorie avec un bouton et une croix de suppression
            const categoryWrapper = document.createElement('div');
            categoryWrapper.className = 'category-wrapper';

            const categoryFlex = document.createElement('div');
            categoryFlex.className = 'category-flex';

            // Bouton pour sélectionner la catégorie
            const categoryButton = document.createElement('button');
            categoryButton.className = 'button';
            categoryButton.style = 'margin: 0; overflow-x: auto;'
            categoryButton.textContent = category.title;
            categoryButton.onclick = () => filterResults(`category:${category.title}`); // Filtrer les résultats pour cette catégorie

            // Croix pour supprimer la catégorie
            const deleteIcon = document.createElement('button');
            deleteIcon.className = 'button button-danger delete-category';
            deleteIcon.textContent = '✖'; // Symbole de croix
            deleteIcon.onclick = () => {
                openDeleteCategoryModal(category.title); // Ouvre la fenêtre modale pour confirmer la suppression
            };

            // Ajouter le bouton et la croix au conteneur
            categoryFlex.appendChild(categoryButton);
            categoryFlex.appendChild(deleteIcon);

            // Ajouter le conteneur complet au DOM
            categoryWrapper.appendChild(categoryFlex)
            categoriesContainer.appendChild(categoryWrapper);
        });

    } catch (error) {
        console.error('Erreur lors du chargement des catégories :', error);
    }
}

// Gère les clics sur le bouton d'authentification (connexion ou déconnexion)
function handleAuthButtonClick() {
    const authButton = document.getElementById('auth-button'); // Bouton connexion/déconnexion

    if (authButton.textContent === "Déconnexion") {
        // Si le bouton indique "Déconnexion", déconnecter l'utilisateur
        fetch('/logout', { method: 'GET' }) // Envoie une requête pour se déconnecter
        .then(response => response.json())
        .then(() => {
            sessionStorage.removeItem('user_email'); // Supprime l'email stocké dans sessionStorage
            sessionStorage.removeItem('user_is_admin');
            checkLoginStatus(); // Met à jour l'état de connexion
            window.location.reload(); // Recharge la page après la déconnexion
        })
        .catch(error => {
            // Gère les erreurs lors de la déconnexion
            console.error('Erreur de déconnexion:', error);
        });
    } else {
        // Si le bouton indique "Connexion", rediriger vers la page de connexion
        window.location.href = `${BASE_URL}/login`; // Redirection vers la page de connexion
    }
}

// Vérifie automatiquement l'état de connexion lors du chargement de la page
checkLoginStatus();