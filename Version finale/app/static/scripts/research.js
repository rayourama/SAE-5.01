let currentCategory = 'all'; // Par défaut, afficher tous les plats

// Fonction de recherche
// Lance une recherche basée sur la valeur de la barre de recherche ou un terme spécifique fourni
async function search(query = null) {
    const searchBar = document.getElementById('search-bar');
    if (query) {
        searchBar.value = query; // Remplit la barre de recherche avec le terme cliqué
    }
    const queryValue = searchBar.value; // Récupère la valeur saisie dans la barre de recherche
    fetchResults(queryValue, currentCategory); // Recherche les résultats dans la catégorie active
}

// Fonction pour filtrer les résultats par type ou catégorie
function filterResults(type) {
    const searchBar = document.getElementById('search-bar'); // Récupère la barre de recherche
    searchBar.value = ''; // Réinitialiser la valeur de la barre de recherche

    if (type.startsWith("category:")) {
        const categoryTitle = type.split(":")[1]; // Récupère le nom de la catégorie
        currentCategory = `category:${categoryTitle}`; // Met à jour la catégorie active
        fetchResults('', currentCategory); // Recherche les items dans la catégorie
    } else {
        currentCategory = type; // Met à jour la catégorie active (ex. 'favorites')
        fetchResults('', type); // Recherche les résultats dans ce type
    }
    toggleRemoveButton(); // Met à jour l'état du bouton "Supprimer de la catégorie"
}

// Fonction pour gérer les clics sur les catégories et les ingrédients
function handleCategoryClick(element) {
    const query = element.textContent.trim(); // Récupère le texte de l'élément cliqué
    search(query); // Lance une recherche avec ce texte
    closeItemModal(); // Ferme la fenêtre modale
}

// Fonction pour afficher les résultats sous forme de cartes
function displayResults(items, category) {
    const resultsContainer = document.getElementById('item-container');
    resultsContainer.innerHTML = ''; // Réinitialise les résultats affichés

    // Afficher un message si aucun résultat trouvé
    if (!Array.isArray(items) || items.length === 0) {
        resultsContainer.innerHTML = `<p>Aucun résultat trouvé dans la catégorie "${category}".</p>`;
        return;
    }

    // Crée une carte pour chaque item et l'ajoute au conteneur
    items.forEach(item => {
        const card = document.createElement('div');
        const imagePath = item.image_path.startsWith('http') ? item.image_path : `${BASE_URL}${item.image_path}`;

        card.className = 'item';
        card.onclick = () => openItemModal(
            imagePath,
            item.name,
            item.flavor,
            item.type,
            item.origin,
            item.ingredients
        ); // Définit un événement de clic pour ouvrir la fenêtre modale

        // Structure HTML de la carte
        card.innerHTML = `
            <img src="${imagePath}" alt="${item.name}" class="item-image">
            <div class="item-form">
                <h3>${item.name}</h3>
            </div>
        `;
        resultsContainer.appendChild(card); // Ajoute la carte au conteneur
    });
}

// Fonction pour récupérer les items en fonction de la catégorie ou du type sélectionné
async function fetchResults(query = '', filterType = 'all') {
    let url;

    // Construire l'URL appropriée en fonction du type ou de la catégorie sélectionnée
    switch (filterType) {
        case 'favorites': // Pour les favoris
            url = `${BASE_URL}/favorites?query=${encodeURIComponent(query)}`;
            break;

        case 'recommendations': // Pour les recommandations
            url = `${BASE_URL}/recommendations?query=${encodeURIComponent(query)}`;
            break;

        default:
            // Pour les catégories personnalisées
            if (filterType.startsWith("category:")) {
                const categoryTitle = filterType.split(":")[1]; // Récupère le titre de la catégorie
                url = `${BASE_URL}/categories/items?category=${encodeURIComponent(categoryTitle)}&query=${encodeURIComponent(query)}`;
            } else {
                // Cas par défaut (tous les plats)
                url = `${BASE_URL}/api/search?query=${encodeURIComponent(query)}&type=${encodeURIComponent(filterType)}`;
            }
            break;
    }

    try {
        const response = await fetch(url);

        // Gestion des erreurs HTTP (par exemple, utilisateur non connecté)
        if (!response.ok) {
            if (response.status === 401) {
                alert("Vous devez être connecté pour accéder à cette catégorie.");
                return;
            }
            throw new Error(`Erreur HTTP : ${response.status}`);
        }

        // Récupérer les données de la réponse
        const data = await response.json();
        const items = (filterType === 'favorites' || filterType === 'recommendations' || filterType.startsWith("category:"))
            ? (data.favorites || data.recommendations || data.items || [])
            : data;

        // Afficher les résultats
        displayResults(items, filterType);
    } catch (error) {
        // Afficher un message d'erreur en cas de problème
        console.error('Erreur lors de la récupération des résultats :', error);
        const resultsContainer = document.getElementById('item-container');
        resultsContainer.innerHTML = `<p>${error.message}</p>`;
    }
}

// Charger tous les plats par défaut lorsque la page est chargée
fetchResults();