from flask import Blueprint, request, session, jsonify, current_app
from app.models.models_items import search_in_database

# Création d'un blueprint pour gérer les routes liées aux favoris
favorites_routes = Blueprint('favorite', __name__)

# Route pour ajouter ou retirer un item des favoris
@favorites_routes.route('/add_favorite', methods=['POST'])
def add_favorite():
    # Vérifier si l'utilisateur est connecté
    if 'user_email' not in session:
        return jsonify({"error": "Vous devez être connecté pour gérer vos favoris."}), 401

    # Récupérer les données de la requête
    email = request.json.get('email')
    item = request.json.get('item')

    # Vérifier que les champs requis sont fournis
    if not email or not item:
        return jsonify({"error": "Les champs 'email' et 'item' sont requis."}), 400

    user_collection = current_app.db["users"]

    # Trouver l'utilisateur dans la base de données
    user = user_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    # Ajouter ou retirer un favori
    if item in user.get('favorites', []):
        # Si l'item est déjà dans les favoris, le retirer
        user_collection.update_one(
            {"email": email},
            {"$pull": {"favorites": item}}
        )
        return jsonify({"message": f"'{item}' a été retiré des favoris."}), 200
    else:
        # Sinon, l'ajouter aux favoris
        user_collection.update_one(
            {"email": email},
            {"$push": {"favorites": item}}
        )
        return jsonify({"message": f"'{item}' a été ajouté aux favoris."}), 200

# Route pour récupérer les noms des favoris d'un utilisateur
@favorites_routes.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    # Récupérer l'email depuis les paramètres de la requête
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "L'email est requis."}), 400

    user_collection = current_app.db["users"]

    # Rechercher l'utilisateur et récupérer ses favoris
    user = user_collection.find_one({"email": email}, {"_id": 0, "favorites": 1})
    if not user:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    # Retourner les favoris sous forme JSON
    return jsonify({"favorites": user.get("favorites", [])}), 200

# Route pour récupérer les détails des plats favoris d'un utilisateur connecté
@favorites_routes.route('/favorites', methods=['GET'])
def get_favorites():
    # Vérifier si l'utilisateur est connecté
    if 'user_email' not in session:
        return jsonify({"error": "Vous devez être connecté pour accéder aux favoris."}), 401

    # Récupérer l'email de l'utilisateur connecté et la requête de recherche
    email = session['user_email']
    query = request.args.get('query', '').lower()  # Recherche en minuscule
    user_collection = current_app.db["users"]

    # Récupérer les favoris de l'utilisateur
    user = user_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    favorite_names = user.get('favorites', [])
    if not favorite_names:
        return jsonify({"favorites": []}), 200

    # Rechercher les plats favoris dans la base de données
    all_favorites = search_in_database(query, filter_type='all')

    # Filtrer les plats qui sont dans la liste des favoris
    filtered_favorites = [f for f in all_favorites if f['name'] in favorite_names]

    # Retourner les favoris filtrés
    return jsonify({"favorites": filtered_favorites}), 200