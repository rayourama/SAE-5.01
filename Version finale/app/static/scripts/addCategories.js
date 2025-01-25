// Ouvre la fenêtre modale pour créer une catégorie
function openCategoryModal() {
    const modal = document.getElementById("modal-category");
    modal.style.display = "flex"; // Afficher la fenêtre modale
}

// Ferme la fenêtre modale pour créer une catégorie
function closeCategoryModal() {
    const modal = document.getElementById("modal-category");
    const titleInput = document.getElementById("modal-category-title");
    const messageContainer = document.getElementById("modal-category-message");

    // Réinitialise le champ de saisie et les messages
    titleInput.value = "";
    messageContainer.textContent = "";
    messageContainer.style.color = "";

    modal.style.display = "none"; // Fermer la fenêtre modale
}

// Ferme la fenêtre modale si l'utilisateur clique en dehors de celle-ci
function outsideClickCategoryModal(event) {
    const modal = document.getElementById('modal-category');
    const modalContent = document.querySelector('.modal-category-content');

    // Ferme la fenêtre si le clic est en dehors du contenu principal
    if (event.target === modal && !modalContent.contains(event.target)) {
        closeCategoryModal();
    }
}

// Supprime une catégorie existante
async function deleteCategory(categoryTitle) {
    try {
        const response = await fetch('/categories', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: categoryTitle }), // Envoyer le titre de la catégorie à supprimer
        });

        if (!response.ok) {
            throw new Error('Erreur lors de la suppression de la catégorie.');
        }

        const data = await response.json();
        console.log(data.message);

        // Si on était dans la catégorie supprimée, revenir à "all"
        if (currentCategory === `category:${categoryTitle}`) {
            currentCategory = 'all';
        }

        // Recharger les résultats et les catégories
        fetchResults('', currentCategory); // Réinitialise les éléments affichés
        await loadUserCategories(); // Recharge les catégories dans l'interface
    } catch (error) {
        console.error('Erreur lors de la suppression de la catégorie :', error);
    } finally {
        closeDeleteCategoryModal(); // Fermer la fenêtre de confirmation de suppression
    }
}

// Ouvre une fenêtre modale pour demander confirmation avant de supprimer une catégorie
function openDeleteCategoryModal(categoryTitle) {
    const modal = document.getElementById('delete-category-modal');
    const message = document.getElementById('delete-category-message');
    const confirmButton = document.getElementById('confirm-delete-category');

    // Met à jour le message de confirmation
    message.textContent = `Voulez-vous vraiment supprimer la catégorie "${categoryTitle}" ?`;
    confirmButton.onclick = () => deleteCategory(categoryTitle); // Associe la suppression au bouton "Confirmer"

    modal.style.display = 'flex'; // Affiche la fenêtre modale
}

// Ferme la fenêtre modale de confirmation de suppression
function closeDeleteCategoryModal() {
    const modal = document.getElementById('delete-category-modal');
    modal.style.display = 'none';
}

// Envoie une nouvelle catégorie depuis la fenêtre modale
async function submitCategoryFromModal() {
    const titleInput = document.getElementById("modal-category-title");
    const messageContainer = document.getElementById("modal-category-message");
    const title = titleInput.value.trim();

    // Réinitialise les messages avant validation
    messageContainer.textContent = "";
    messageContainer.style.color = "";

    // Charger les catégories existantes
    try {
        const response = await fetch('/categories', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error("Erreur lors de la récupération des catégories.");
        }

        const data = await response.json();
        const categories = data.categories || []; // Récupérer les catégories ou une liste vide

        // Vérifier si la limite est atteinte
        if (categories.length >= 5) {
            messageContainer.textContent = "Vous avez atteint la limite de 5 catégories. Supprimez une catégorie existante pour en créer une nouvelle.";
            messageContainer.style.color = "red";
            return;
        }
    } catch (error) {
        console.error('Erreur lors de la vérification des catégories existantes :', error);
        messageContainer.textContent = "Une erreur s'est produite lors de la vérification des catégories.";
        messageContainer.style.color = "red";
        return;
    }

    // Validation du titre
    if (!title) {
        messageContainer.textContent = "Veuillez entrer un titre pour la catégorie.";
        messageContainer.style.color = "red";
        return;
    }

    if (title.length > 20) { // Vérifie que le titre ne dépasse pas 20 caractères
        messageContainer.textContent = "Le titre de la catégorie ne peut pas dépasser 20 caractères.";
        messageContainer.style.color = "red";
        return;
    }

    try {
        const response = await fetch('/categories', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title }), // Envoie le titre de la nouvelle catégorie au backend
        });

        if (!response.ok) {
            const errorData = await response.json();
            if (errorData.error && errorData.error.includes("existe déjà")) {
                // Gérer le cas d'une catégorie déjà existante
                messageContainer.textContent = `La catégorie "${title}" existe déjà.`;
                messageContainer.style.color = "orange";
                return;
            }
        }

        // Confirmation de la création de la catégorie
        messageContainer.textContent = `Catégorie "${title}" créée avec succès !`;
        messageContainer.style.color = "green";

        closeCategoryModal(); // Fermer la fenêtre modale
        await loadUserCategories(); // Recharger les catégories pour inclure la nouvelle
    } catch (error) {
        console.error('Erreur lors de la création de la catégorie :', error);
        messageContainer.textContent = "Une erreur s'est produite lors de la création de la catégorie.";
        messageContainer.style.color = "red";
    }
}

// Ouvre le menu déroulant pour afficher les catégories
function openCategoryDropdown() {
    const dropdown = document.getElementById("category-dropdown");
    const isVisible = dropdown.style.display === "block";

    // Basculer entre afficher et masquer le menu déroulant
    dropdown.style.display = isVisible ? "none" : "block";

    // Si le menu est ouvert, charger les catégories
    if (!isVisible) {
        populateCategoryDropdown(); // Récupère et affiche les catégories
    }
}

// Ferme le menu déroulant
function closeCategoryDropdown() {
    const dropdown = document.getElementById("category-dropdown");
    if (dropdown) {
        dropdown.style.display = "none"; // Masque le menu déroulant
    }
}

// Charge et affiche les noms des catégories dans le menu déroulant
async function populateCategoryDropdown() {
    const categoryList = document.getElementById("category-list");
    const dropdown = document.getElementById("category-dropdown");

    // Réinitialise la liste des catégories dans le dropdown
    categoryList.innerHTML = "";

    try {
        // Effectue une requête pour récupérer les catégories de l'utilisateur
        const response = await fetch('/categories', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error("Erreur lors de la récupération des catégories.");
        }

        const data = await response.json();
        const categories = data.categories || []; // Charge les catégories ou une liste vide si aucune

        if (categories.length === 0) {
            // Affiche un message si aucune catégorie n'est disponible
            const noCategoryItem = document.createElement("li");
            noCategoryItem.textContent = "Aucune catégorie disponible.";
            noCategoryItem.style.color = "gray";
            categoryList.appendChild(noCategoryItem);
            return;
        }

        // Ajoute chaque catégorie dans le menu déroulant
        categories.forEach(category => {
            const listItem = document.createElement("li");
            listItem.textContent = category.title; // Affiche le titre de la catégorie
            listItem.className = "category-item"; // Classe CSS pour le style
            listItem.onclick = () => {
                addItemToCategory(category.title); // Ajoute l'élément à la catégorie correspondante
                dropdown.style.display = "none"; // Masque le menu déroulant après sélection
            };
            categoryList.appendChild(listItem); // Ajoute l'élément à la liste
        });

    } catch (error) {
        console.error("Erreur lors de la récupération des catégories :", error);

        // Affiche un message d'erreur si la récupération échoue
        const errorItem = document.createElement("li");
        errorItem.textContent = "Erreur lors du chargement des catégories.";
        errorItem.style.color = "red";
        categoryList.appendChild(errorItem);
    }
}

// Ajoute un plat à une catégorie
async function addItemToCategory(categoryTitle) {
    const foodName = document.getElementById("modal-item-title").textContent; // Récupère le nom du plat
    const userEmail = sessionStorage.getItem("user_email"); // Récupère l'email de l'utilisateur connecté

    try {
        const response = await fetch(`/categories/add_item`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: userEmail, category: categoryTitle, item: foodName }),
        });

        const data = await response.json();
        if (response.ok) {
            // Confirme l'ajout et ferme la fenêtre modale
            console.log(`Le plat "${foodName}" a été ajouté à la catégorie "${categoryTitle}".`);
            closeItemModal();
        } else {
            // Affiche une alerte en cas d'erreur
            alert(data.error || "Erreur lors de l'ajout à la catégorie.");
        }
    } catch (error) {
        console.error("Erreur lors de l'ajout à la catégorie :", error);
    }
}

// Supprime un plat de la catégorie active
async function removeFromCurrentCategory() {
    const foodName = document.getElementById("modal-item-title").textContent; // Récupère le nom du plat
    const userEmail = sessionStorage.getItem("user_email"); // Récupère l'email de l'utilisateur connecté
    const categoryTitle = currentCategory.split(":")[1]; // Récupère le nom de la catégorie active

    try {
        const response = await fetch('/categories/remove_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: userEmail, category: categoryTitle, item: foodName }), // Envoie les données nécessaires
        });

        const data = await response.json();
        if (response.ok) {
            // Confirme la suppression, recharge les résultats, et ferme la fenêtre modale
            console.log(`Le plat "${foodName}" a été supprimé de la catégorie "${categoryTitle}".`);
            fetchResults('', currentCategory); // Rafraîchit les résultats pour refléter les changements
            closeItemModal(); // Ferme la fenêtre modale
        } else {
            // Affiche une alerte en cas d'erreur
            alert(data.error || "Erreur lors de la suppression de l'élément.");
        }
    } catch (error) {
        console.error("Erreur lors de la suppression de l'élément :", error);
    }
}

// Charger les catégories au chargement de la page
document.addEventListener("DOMContentLoaded", loadUserCategories);