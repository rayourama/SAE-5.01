from flask import Blueprint, request, session, jsonify, current_app
from app.utils.recommendation import build_filter_criteria, calculate_scores, analyze_preferences
from app.models.models_items import search_in_database

# Création d'un blueprint pour les routes de recommandations
recommendations_routes = Blueprint('recommendations', __name__)

# Route pour récupérer les recommandations
@recommendations_routes.route('/recommendations', methods=['GET'])
def get_recommendations():
    # Vérifie si l'utilisateur est connecté
    if 'user_email' not in session:
        return jsonify({"error": "Vous devez être connecté pour accéder aux recommandations."}), 401

    email = session['user_email']  # Récupère l'email de l'utilisateur connecté
    query = request.args.get('query', '').lower()  # Requête de recherche facultative
    user_collection = current_app.db["users"]  # Collection MongoDB des utilisateurs
    food_collection = current_app.db["food_items"]  # Collection MongoDB des plats

    # Récupère l'utilisateur et ses favoris
    user = user_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "Utilisateur non trouvé."}), 404

    favorite_names = user.get('favorites', [])  # Liste des favoris de l'utilisateur
    if not favorite_names:
        # Si l'utilisateur n'a pas de favoris, renvoyer une liste vide
        return jsonify({"recommendations": []}), 200

    # Récupère les détails des plats favoris à partir de la collection "food_items"
    favorites_data = list(food_collection.find({"name": {"$in": favorite_names}}, {"_id": 0}))
    if not favorites_data:
        # Si aucun favori n'a été trouvé, renvoyer une liste vide
        return jsonify({"recommendations": []}), 200

    # Analyser les préférences de l'utilisateur basées sur ses favoris
    ranked_preferences = analyze_preferences(favorites_data)  # Renvoie un classement des préférences
    if not ranked_preferences:
        return jsonify({"recommendations": []}), 200

    # Construire des critères de filtrage basés sur les préférences analysées
    filter_criteria = build_filter_criteria(ranked_preferences)

    # Récupérer les plats pertinents selon les critères
    relevant_items = list(food_collection.find(filter_criteria, {"_id": 0}))

    # Calculer les scores des plats en fonction des préférences
    scored_items = calculate_scores(relevant_items, ranked_preferences, favorite_names)

    # Exclure les plats ayant un score de 0 (non pertinents)
    scored_items = [item for item in scored_items if item["score"] > 0]

    # Limiter les résultats à 30 plats maximum
    scored_items = scored_items[:30]

    # Rechercher dans les plats filtrés à l'aide de la fonction `search_in_database`
    filtered_recommendations = search_in_database(query, filter_type='all')
    scored_items = [item for item in scored_items if item['name'] in [r['name'] for r in filtered_recommendations]]

    # Trier les plats par score décroissant pour afficher les plus pertinents en premier
    scored_items.sort(key=lambda x: x['score'], reverse=True)

    # Retourner les recommandations finales
    return jsonify({"recommendations": scored_items}), 200