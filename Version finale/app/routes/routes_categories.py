from flask import Blueprint, request, session, jsonify, current_app
from app.models.models_users import get_user_categories
from app.models.models_items import search_in_database

categories_routes = Blueprint('categories', __name__)

# Récupérer toutes les catégories de l'utilisateur connecté
@categories_routes.route('/categories', methods=['GET'])
def get_user_categories_route():
    # Vérifie si l'utilisateur est connecté
    if 'user_email' not in session:
        return jsonify({"error": "Vous devez être connecté pour voir vos catégories."}), 401
    
    # Appelle la fonction pour récupérer les catégories de l'utilisateur
    categories = get_user_categories(session['user_email'])
    return jsonify({"categories": categories}), 200


# Créer une nouvelle catégorie pour l'utilisateur
@categories_routes.route('/categories', methods=['POST'])
def create_category():
    # Vérifie si l'utilisateur est connecté
    if 'user_email' not in session:
        return jsonify({"error": "Vous devez être connecté pour créer une catégorie."}), 401
    
    data = request.json
    title = data.get('title', '').strip().lower()  # Normalise le titre en minuscule
    
    # Vérifie que le titre n'est pas vide
    if not title:
        return jsonify({"error": "Le titre de la catégorie est requis."}), 400

    # Vérifie que le titre ne dépasse pas 20 caractères
    if len(title) > 20:
        return jsonify({"error": "Le titre de la catégorie ne peut pas dépasser 20 caractères."}), 400

    user_collection = current_app.db["users"]
    user = user_collection.find_one({"email": session['user_email']})

    # Vérifier la limite de catégories
    if len(user.get('categories', [])) >= 5:
        return jsonify({"error": "Limite de catégories atteinte"}), 400

    # Vérifie si l'utilisateur existe
    if not user:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    # Vérifie si une catégorie avec le même titre existe déjà
    if any(cat["title"].lower() == title for cat in user.get("categories", [])):
        return jsonify({"error": "Cette catégorie existe déjà."}), 409

    # Ajoute la nouvelle catégorie avec une liste vide d'items
    new_category = {"title": title, "items": []}
    user_collection.update_one(
        {"email": session['user_email']},
        {"$push": {"categories": new_category}}
    )

    return jsonify({"message": f"La catégorie '{title}' a été créée avec succès."}), 201


# Supprimer une catégorie existante
@categories_routes.route('/categories', methods=['DELETE'])
def delete_category():
    # Vérifie si l'utilisateur est connecté
    if 'user_email' not in session:
        return jsonify({"error": "Vous devez être connecté pour supprimer une catégorie."}), 401
    
    data = request.json
    title = data.get('title', '').strip().lower()  # Normalise le titre
    
    # Vérifie que le titre est fourni
    if not title:
        return jsonify({"error": "Le titre de la catégorie est requis."}), 400

    user_collection = current_app.db["users"]
    user = user_collection.find_one({"email": session['user_email']})

    # Vérifie si l'utilisateur existe
    if not user:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    # Supprime la catégorie correspondante
    user_collection.update_one(
        {"email": session['user_email']},
        {"$pull": {"categories": {"title": title}}}
    )

    return jsonify({"message": f"La catégorie '{title}' a été supprimée avec succès."}), 200


# Ajouter un item à une catégorie
@categories_routes.route('/categories/add_item', methods=['POST'])
def add_item_to_category():
    # Vérifie si l'utilisateur est connecté
    if 'user_email' not in session:
        return jsonify({"error": "Vous devez être connecté pour ajouter un plat à une catégorie."}), 401
    
    data = request.json
    email = data.get("email")
    category_title = data.get("category")
    item_name = data.get("item")

    # Vérifie que toutes les données requises sont fournies
    if not email or not category_title or not item_name:
        return jsonify({"error": "Données incomplètes."}), 400

    user = current_app.db["users"].find_one({"email": email})

    # Vérifie si l'utilisateur existe
    if not user:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    # Vérifie si la catégorie existe
    categories = user.get("categories", [])
    category = next((cat for cat in categories if cat["title"] == category_title), None)
    if not category:
        return jsonify({"error": "Catégorie introuvable."}), 404

    # Ajoute l'item s'il n'est pas déjà présent
    if item_name in category.get("items", []):
        return jsonify({"error": "Cet item est déjà dans la catégorie."}), 409

    category["items"].append(item_name)
    current_app.db["users"].update_one(
        {"email": email, "categories.title": category_title},
        {"$set": {"categories.$.items": category["items"]}}
    )

    return jsonify({"message": f"Item '{item_name}' ajouté à la catégorie '{category_title}'."}), 200


# Récupérer les items d'une catégorie
@categories_routes.route('/categories/items', methods=['GET'])
def get_items_by_category():
    category_title = request.args.get("category", "").strip().lower()
    query = request.args.get("query", "").strip().lower()
    email = session.get("user_email")

    # Vérifie si l'utilisateur est connecté
    if not email:
        return jsonify({"error": "Vous devez être connecté pour accéder aux catégories."}), 401

    user = current_app.db["users"].find_one({"email": email})

    # Vérifie si l'utilisateur existe
    if not user:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    # Trouve la catégorie correspondant au titre
    categories = user.get("categories", [])
    category = next((cat for cat in categories if cat["title"].lower() == category_title), None)
    if not category:
        return jsonify({"error": "Catégorie introuvable."}), 404

    # Filtre les items si une requête de recherche est fournie
    item_names = category.get("items", [])
    if query:
        item_names = [item for item in item_names if query in item.lower()]

    # Enrichit les items avec leurs détails
    enriched_items = search_in_database(query="", filter_type="all")
    filtered_items = [item for item in enriched_items if item["name"] in item_names]

    return jsonify({"items": filtered_items}), 200


# Supprimer un item d'une catégorie
@categories_routes.route('/categories/remove_item', methods=['POST'])
def remove_item_from_category():
    # Vérifie si l'utilisateur est connecté
    if 'user_email' not in session:
        return jsonify({"error": "Vous devez être connecté pour supprimer un item d'une catégorie."}), 401
    
    data = request.json
    email = data.get("email")
    category_title = data.get("category")
    item_name = data.get("item")

    # Vérifie que toutes les données requises sont fournies
    if not email or not category_title or not item_name:
        return jsonify({"error": "Données incomplètes."}), 400

    user = current_app.db["users"].find_one({"email": email})

    # Vérifie si l'utilisateur existe
    if not user:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    # Vérifie si la catégorie existe
    categories = user.get("categories", [])
    category = next((cat for cat in categories if cat["title"] == category_title), None)
    if not category:
        return jsonify({"error": "Catégorie introuvable."}), 404

    # Vérifie si l'item existe dans la catégorie
    if item_name not in category.get("items", []):
        return jsonify({"error": "Cet item n'existe pas dans la catégorie."}), 404

    # Supprime l'item de la catégorie
    category["items"].remove(item_name)
    current_app.db["users"].update_one(
        {"email": email, "categories.title": category_title},
        {"$set": {"categories.$.items": category["items"]}}
    )

    return jsonify({"message": f"L'item '{item_name}' a été supprimé de la catégorie '{category_title}'."}), 200