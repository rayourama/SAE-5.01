// Fonction pour créer un compte
async function registerUser() {
    // Récupération des valeurs des champs de saisie
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    const messageDiv = document.getElementById('register-message'); // Élément pour afficher les messages

    // Vérification que les mots de passe correspondent
    if (password !== confirmPassword) {
        messageDiv.style.color = 'red'; // Message en rouge pour signaler une erreur
        messageDiv.textContent = 'Les mots de passe ne correspondent pas.';
        return; // Arrête la fonction si les mots de passe ne correspondent pas
    }

    try {
        // Envoie une requête POST au serveur pour enregistrer un nouvel utilisateur
        const response = await fetch(`${BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Spécifie que les données sont au format JSON
            },
            body: JSON.stringify({
                email: email,
                password: password,
                is_admin: false
            }) // Les données envoyées au serveur
        });

        const data = await response.json(); // Récupère la réponse du serveur

        if (response.ok) {
            // Si la création de compte réussit
            messageDiv.style.color = 'green'; // Message en vert pour succès
            messageDiv.textContent = data.message; // Affiche le message de succès
            window.location.href = `${BASE_URL}/login`; // Redirige vers la page de connexion
        } else {
            // Si le serveur retourne une erreur
            messageDiv.style.color = 'red';
            messageDiv.textContent = data.message || data.error; // Affiche l'erreur retournée
        }
    } catch (error) {
        // Gestion des erreurs réseau ou autres exceptions
        console.error('Erreur:', error);
        messageDiv.style.color = 'red';
        messageDiv.textContent = 'Erreur lors de la création du compte.';
    }
}

// Fonction pour se connecter à son compte
async function loginUser(email, password) {
    const messageDiv = document.getElementById('login-message'); // Élément pour afficher les messages d'erreur

    // Vérification locale des champs requis
    if (!email || !password) {
        messageDiv.style.color = 'red'; // Message en rouge pour signaler une erreur
        messageDiv.textContent = 'Veuillez remplir tous les champs.';
        return; // Arrête la fonction si des champs sont vides
    }

    try {
        // Envoie une requête POST au serveur pour se connecter
        const response = await fetch(`${BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }, // Spécifie que les données sont au format JSON
            body: JSON.stringify({ email, password }) // Les données envoyées au serveur
        });

        const data = await response.json(); // Récupère la réponse du serveur

        if (response.ok) {
            // Si la connexion réussit
            sessionStorage.setItem('user_email', email); // Stocke l'email de l'utilisateur dans le stockage de session
            sessionStorage.setItem('user_is_admin', data.is_admin); // Stocke l'email de l'utilisateur dans le stockage de session

            console.log('Connexion réussie pour l\'email suivant :', sessionStorage.getItem('user_email'));

            if (data.is_admin == false){
                window.location.href = '/'; // Redirige vers la page principale
            }
            else{
                window.location.href = '/admin'; // Redirige vers la page admin
            }
        } else {
            // Si le serveur retourne une erreur
            messageDiv.style.color = 'red';
            messageDiv.textContent = data.error; // Affiche l'erreur retournée
        }
    } catch (error) {
        // Gestion des erreurs réseau ou autres exceptions
        console.error('Erreur:', error);
        messageDiv.style.color = 'red';
        messageDiv.textContent = 'Erreur lors de la connexion au serveur.';
    }
}