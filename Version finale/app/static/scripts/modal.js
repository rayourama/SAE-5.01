// Suivi de l'état des favoris
const favoriteStatus = {}; // Objet pour suivre les plats favoris de l'utilisateur

// Fonction pour ouvrir la fenêtre modale
async function openItemModal(imagePath, name, flavor, type, origin, ingredients) {
    // Références des éléments dans la fenêtre modale
    const modal = document.getElementById('modal-item');
    const modalImage = document.getElementById('modal-item-image');
    const modalTitle = document.getElementById('modal-item-title');
    const modalFlavor = document.getElementById('modal-item-flavor');
    const modalType = document.getElementById('modal-item-type');
    const modalOrigin = document.getElementById('modal-item-origin');
    const modalIngredients = document.getElementById('modal-item-ingredients');
    const star = document.querySelector('.star-icon');

    // Mettre à jour les éléments de la modale avec les informations du plat
    modalImage.src = imagePath;
    modalTitle.textContent = name;
    modalFlavor.innerHTML = flavor.split(', ').map(f => `<span class="modal-item-category" onclick="handleCategoryClick(this)">${f}</span>`).join('');
    modalType.innerHTML = type.split(', ').map(t => `<span class="modal-item-category" onclick="handleCategoryClick(this)">${t}</span>`).join('');
    modalOrigin.innerHTML = origin.split(', ').map(o => `<span class="modal-item-category" onclick="handleCategoryClick(this)">${o}</span>`).join('');
    modalIngredients.innerHTML = ingredients.split(', ').map(ing => `<span class='modal-item-category' onclick="handleCategoryClick(this)">${ing}</span>`).join('');

    // Récupérer les favoris depuis le backend
    const userEmail = sessionStorage.getItem('user_email'); // Récupération de l'utilisateur connecté
    if (userEmail) {
        try {
            const response = await fetch(`${BASE_URL}/user/favorites?email=${userEmail}`);
            const data = await response.json();

            if (response.ok) {
                // Mettre à jour les favoris localement
                data.favorites.forEach(fav => {
                    favoriteStatus[fav] = true;
                });
            } else {
                console.error(data.error || 'Erreur lors de la récupération des favoris.');
            }
        } catch (error) {
            console.error('Erreur réseau lors de la récupération des favoris :', error);
        }
    }

    // Mettre à jour l'apparence de l'étoile en fonction du statut du favori
    if (favoriteStatus[name]) {
        star.src = '../static/images/star-yellow.png'; // Étoile jaune si le plat est favori
        star.classList.add('active');
    } else {
        star.src = '../static/images/star-gray.png'; // Étoile grise sinon
        star.classList.remove('active');
    }

    modal.style.display = 'flex'; // Afficher la fenêtre modale

    // Ajouter un gestionnaire de clic à l'étoile
    star.onclick = () => toggleStar(name);
}

// Fonction pour fermer la fenêtre modale
function closeItemModal() {
    const modal = document.getElementById('modal-item');
    modal.style.display = 'none'; // Cacher la fenêtre modale
    closeCategoryDropdown(); // Ferme également le menu déroulant s'il est ouvert
}

// Fonction pour fermer la fenêtre modale en cliquant en dehors de celle-ci
function outsideItemClick(event) {
    const modal = document.getElementById('modal-item');
    const modalContent = document.querySelector('.modal-item-container');

    // Ferme la modale si le clic est en dehors du contenu de la modale
    if (event.target === modal && !modalContent.contains(event.target)) {
        closeItemModal();
    }
}

// Fonction pour basculer entre l'étoile grise et l'étoile jaune (favori/non favori)
async function toggleStar(foodName) {
    const star = document.querySelector('.star-icon');
    const userEmail = sessionStorage.getItem('user_email'); // Email de l'utilisateur connecté

    // Basculer l'état localement
    const isFavorite = favoriteStatus[foodName];
    favoriteStatus[foodName] = !isFavorite;

    // Mettre à jour l'apparence de l'étoile
    if (isFavorite) {
        delete favoriteStatus[foodName]; // Supprimer des favoris
        star.src = '../static/images/star-gray.png';
        star.classList.remove('active');
    } else {
        favoriteStatus[foodName] = true; // Ajouter aux favoris
        star.src = '../static/images/star-yellow.png';
        star.classList.add('active');
    }

    // Envoyer l'état mis à jour au backend
    try {
        const response = await fetch(`${BASE_URL}/add_favorite`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: userEmail,
                item: foodName,
            }),
        });

        const data = await response.json();
        if (response.ok) {
            console.log(data.message); // Succès de la mise à jour des favoris
        } else {
            console.error(data.error || 'Erreur lors de la mise à jour des favoris.');
        }
    } catch (error) {
        console.error('Erreur réseau lors de la mise à jour des favoris :', error);
    }
}

// Met à jour le bouton pour supprimer un item d'une catégorie
function toggleRemoveButton() {
    const removeButton = document.getElementById("remove-from-category-btn");

    // Activer le bouton si dans une catégorie personnalisée
    if (currentCategory.startsWith("category:")) {
        removeButton.disabled = false; // Activer le bouton
    } else {
        removeButton.disabled = true; // Désactiver le bouton
    }
}