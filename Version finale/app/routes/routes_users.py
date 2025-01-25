from flask import Blueprint, request, session, jsonify, current_app, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Création du blueprint pour les routes utilisateur
users_routes = Blueprint('users', __name__)

# Route pour afficher la page d'inscription
@users_routes.route('/register')
def register_page():
    return render_template('register.html')  # Renvoie le fichier HTML pour l'inscription

# Route pour afficher la page de connexion
@users_routes.route('/login')
def login_page():
    return render_template('login.html')  # Renvoie le fichier HTML pour la connexion

# Route pour gérer l'inscription
@users_routes.route('/register', methods=['POST'])
def register():
    data = request.json  # Données envoyées depuis le frontend
    email = data.get('email')  # Récupérer l'email
    password = data.get('password')  # Récupérer le mot de passe
    is_admin = data.get('is_admin'); # Récupérer l'attribut is_admin

    # Vérification des champs obligatoires
    if not email or not password:
        return jsonify({"error": "L'email et le mot de passe sont requis."}), 400

    # Validation du format de l'email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return jsonify({"error": "L'adresse email est invalide."}), 400

    user_collection = current_app.db["users"]  # Collection MongoDB des utilisateurs

    # Vérification si l'email existe déjà
    if user_collection.find_one({"email": email}):
        return jsonify({"error": "Cet email existe déjà."}), 400

    # Hachage du mot de passe pour la sécurité
    hashed_password = generate_password_hash(password)

    # Ajout de l'utilisateur à la base de données
    try:
        user_collection.insert_one({
            "email": email,
            "password": hashed_password,
            "is_admin": bool(is_admin),
            "favorites": [],  # Initialisation des favoris
            "categories": []  # Initialisation des catégories personnalisées
        })
        return jsonify({"message": "Utilisateur enregistré avec succès."}), 201
    except Exception as e:
        # Journalisation des erreurs
        current_app.logger.error(f"Une erreur s'est produite : {str(e)}")
        return jsonify({"error": f"Une erreur s'est produite : {str(e)}"}), 500

# Route pour gérer la connexion
@users_routes.route('/login', methods=['POST'])
def login():
    data = request.json  # Données envoyées depuis le frontend
    email = data.get('email')  # Récupérer l'email
    password = data.get('password')  # Récupérer le mot de passe

    # Vérification des champs obligatoires
    if not email or not password:
        return jsonify({"error": "L'email et le mot de passe sont requis."}), 400

    user_collection = current_app.db["users"]  # Collection MongoDB des utilisateurs

    # Rechercher l'utilisateur dans la base de données
    user = user_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "Nous n'avons pas trouvé cette adresse e-mail. Veuillez réessayer ou inscrivez-vous"}), 401

    # Vérification du mot de passe
    if not check_password_hash(user['password'], password):
        return jsonify({"error": "Le mot de passe est incorrect."}), 401

    # Stocker l'email dans la session pour maintenir la connexion
    session['user_email'] = email
    return jsonify({ "is_admin": user["is_admin"], "message": "Connexion réussie."}), 200

# Route pour déconnecter l'utilisateur
@users_routes.route('/logout', methods=['GET'])
def logout():
    session.pop('user_email', None)  # Supprime l'email de la session
    return jsonify({"message": "Déconnexion réussie."}), 200

# Route pour vérifier si l'utilisateur est connecté
@users_routes.route('/check_login', methods=['GET'])
def check_login():
    if 'user_email' in session:  # Vérifie si l'email est stocké dans la session
        user_collection = current_app.db["users"]

        # Récupérer les informations utilisateur
        user = user_collection.find_one({"email": session['user_email']})
        favorites = []
        is_admin = False
        if user:
            favorites = user["favorites"]  # Récupère les favoris
            is_admin = user["is_admin"]

        return jsonify({
            "loggedIn": True,
            "email": session['user_email'],  # Renvoie l'
            "is_admin": is_admin,
            "favorites": favorites  # Renvoie les favoris si l'utilisateur est connecté
        })

    # Si l'utilisateur n'est pas connecté
    return jsonify({"loggedIn": False})