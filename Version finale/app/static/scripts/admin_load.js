const API_URL = "/api/food_items";
const URL = `${BASE_URL}${API_URL}`

function check_is_admin(){
    // Envoie une requête pour vérifier l'état de connexion
    fetch('/check_login', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json()) // Convertit la réponse en JSON
    .then(async data => {
        if (data.loggedIn) {
            if (!data.is_admin) {
                window.location.href = `${BASE_URL}/`; // Redirige vers la page admin
                return;
            }
            else{
                document.querySelector("#root").style.display = "block";
                loadFoodItems();
            }
        } else {
            window.location.href = `${BASE_URL}/`; // Redirige vers la page admin
        }
    })
    .catch(error => {
        console.error('Erreur de vérification de connexion:', error);
    });
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
            window.location.href = `${BASE_URL}/`; // Recharge la page après la déconnexion
        })
        .catch(error => {
            // Gère les erreurs lors de la déconnexion
            console.error('Erreur de déconnexion:', error);
            window.location.href = `${BASE_URL}/`;
        });
    }
}

// Charger et afficher les plats
async function loadFoodItems() {
    try {
        const response = await fetch(`${URL}`);
        // Gestion des erreurs HTTP (par exemple, utilisateur non connecté)
        if (!response.ok) {
            if (response.status === 401) {
                alert("Erreur lors de la récupération de la liste des plats ...");
                return;
            }
            throw new Error(`Erreur HTTP : ${response.status}`);
        }

        // Récupérer les données de la réponse
        const foodItems = await response.json();
        displayResults( foodItems );

    } catch (error) {
        // Afficher un message d'erreur en cas de problème
        console.error('Erreur lors de la récupération des résultats :', error);
        const resultsContainer = document.getElementById('item-container');
        resultsContainer.innerHTML = `<p>${error.message}</p>`;
    }
}

function displayResults(foodItems) {
    const tableBody = document.querySelector("#food-table tbody");
    tableBody.innerHTML = ""; // Vider la table avant de recharger

    foodItems.forEach((item) => {
        const row = `
            <tr>
                <td>${item.name}</td>
                <td>${item.flavor}</td>
                <td>${item.type}</td>
                <td>${item.origin}</td>
                <td>${item.ingredients}</td>
                <td><img src="${item.image_path}" width="50"></td>
                <td>
                    <button onclick="editFood('${item._id}')">Modifier</button>
                    <button onclick="deleteFood('${item._id}')">Supprimer</button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

// Ajouter ou modifier un plat
async function saveFood() {
    /*
    const id = document.getElementById("food-id").value;
    const foodData = {
        name: document.getElementById("food-name").value,
        flavor: document.getElementById("food-flavor").value,
        type: document.getElementById("food-type").value,
        origin: document.getElementById("food-origin").value,
        ingredients: document.getElementById("food-ingredients").value,
        image_path: document.getElementById("food-image-path").value
    };

    if (id) {
        await fetch(`${URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(foodData),
        });
    } else {
        await fetch(URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(foodData),
        });
    }

    closeModal();
    loadFoodItems();
    */

    const id = document.getElementById('food-id').value;
    const name = document.getElementById('food-name').value;
    const flavor = document.getElementById('food-flavor').value;
    const type = document.getElementById('food-type').value;
    const origin = document.getElementById('food-origin').value;
    const ingredients = document.getElementById('food-ingredients').value;
    const imageFile = document.getElementById('food-image').files[0];

    const formData = new FormData();
    formData.append('name', name);
    formData.append('flavor', flavor);
    formData.append('type', type);
    formData.append('origin', origin);
    formData.append('ingredients', ingredients);

    if (imageFile) {
        formData.append('image', imageFile);
    }
    else if (!id) {
        alert("Veuillez sélectionner une photo / image pour le plat ...")
        return;
    }

    const url = id ? `${URL}/${id}` : '/api/food_items';
    const method = id ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            body: formData,  // Envoi en tant que formulaire multipart
        });

        if (response.ok) {
            alert('Plat enregistré avec succès');
            closeModal();
            location.reload();
        } else {
            alert('Erreur lors de l\'enregistrement');
        }
    } catch (error) {
        console.error('Erreur:', error);
    }
}

// Supprimer un plat
async function deleteFood(id) {
    if (confirm("Voulez-vous vraiment supprimer ce plat ?")) {
        await fetch(`${URL}/${id}`, { method: "DELETE" });
        loadFoodItems();
    }
}

// Pré-remplir les champs pour la modification
async function editFood(id) {
    const response = await fetch(`${URL}/${id}`);
    const item = await response.json();

    document.getElementById("food-id").value = item._id;
    document.getElementById("food-name").value = item.name;
    document.getElementById("food-flavor").value = item.flavor;
    document.getElementById("food-type").value = item.type;
    document.getElementById("food-origin").value = item.origin;
    document.getElementById("food-ingredients").value = item.ingredients;
    //document.getElementById("food-image-path").value = item.image_path;

    openModal("Modifier le plat");
}

// Ouvrir/fermer le modal
function openAddModal() {
    document.getElementById("food-id").value = "";
    document.getElementById("modal-title").innerText = "Ajouter un plat";

    document.getElementById("food-id").value = "";
    document.getElementById("food-name").value = "";
    document.getElementById("food-flavor").value = "";
    document.getElementById("food-type").value = "";
    document.getElementById("food-origin").value = "";
    document.getElementById("food-ingredients").value = "";
    //document.getElementById("food-image-path").value = "";

    openModal();
}

function openModal(title) {
    document.getElementById("modal-title").innerText = title || "Ajouter un plat";
    document.getElementById("modal").style.display = "block";
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

// Charger les plats au chargement de la page
window.onload = check_is_admin; //loadFoodItems;
