from flask import current_app

# Fonction pour insérer un utilisateur dans la base de données
def create_user(email, password):
    user_collection = current_app.db["users"]  # Accès à la collection "users" dans la base de données
    try:
        # Vérifie si un utilisateur avec cet email existe déjà
        if user_collection.find_one({"email": email}):
            return {"error": "Cet email existe déjà."}, 400

        # Insère un nouvel utilisateur dans la collection
        user_collection.insert_one({
            "email": email,
            "password": password,
            "favorites": [],  # Liste vide pour les favoris
            "categories": []  # Liste vide pour les catégories personnalisées
        })
        return {"message": "Utilisateur créé avec succès."}, 201
    except Exception as e:
        # Journalise l'erreur et retourne un message d'erreur générique
        current_app.logger.error(f"Une erreur s'est produite lors de la création de l'utilisateur : {e}")
        return {"error": "Une erreur s'est produite lors de la création de l'utilisateur."}, 500


# Fonction pour rechercher un utilisateur dans la base de données
def find_user_by_email(email):
    user_collection = current_app.db["users"]  # Accès à la collection "users"
    try:
        # Recherche l'utilisateur avec l'email spécifié
        user = user_collection.find_one({"email": email})
        if user:
            return user
        # Retourne une erreur si l'utilisateur n'est pas trouvé
        return {"error": "Utilisateur introuvable."}, 404
    except Exception as e:
        # Journalise l'erreur et retourne un message d'erreur générique
        current_app.logger.error(f"Une erreur s'est produite lors de la recherche de l'utilisateur : {e}")
        return {"error": "Une erreur s'est produite lors de la recherche de l'utilisateur."}, 500


# Fonction pour récupérer les catégories d'un utilisateur
def get_user_categories(email):
    user_collection = current_app.db["users"]  # Accès à la collection "users"
    try:
        # Recherche les catégories d'un utilisateur en excluant l'_id
        user = user_collection.find_one({"email": email}, {"_id": 0, "categories": 1})
        if user and "categories" in user:
            return user["categories"]  # Retourne la liste des catégories
        # Retourne une erreur si l'utilisateur ou les catégories n'existent pas
        return {"error": "Utilisateur introuvable ou aucune catégorie disponible."}, 404
    except Exception as e:
        # Journalise l'erreur et retourne un message d'erreur générique
        current_app.logger.error(f"Une erreur s'est produite lors de la récupération des catégories : {e}")
        return {"error": "Une erreur s'est produite lors de la récupération des catégories."}, 500