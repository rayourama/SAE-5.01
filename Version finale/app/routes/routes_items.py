from flask import Blueprint, request, jsonify, render_template
from ..models.models_items import search_in_database

# Création d'un blueprint pour gérer les routes principales
main_routes = Blueprint('main', __name__)

# Route principale pour afficher la page d'accueil
@main_routes.route('/')
def index():
    # Rend le template HTML principal
    return render_template('template.html')

# Route API pour rechercher des items
@main_routes.route('/api/search', methods=['GET'])
def search_items():
    # Récupérer les paramètres de requête : `query` pour la recherche et `type` pour le filtre
    query = request.args.get('query', '').lower()  # Normaliser la recherche en minuscule
    filter_type = request.args.get('type', 'all').lower()  # Filtre par défaut : 'all'

    # Appeler la fonction de recherche dans la base de données
    results = search_in_database(query, filter_type)

    # Éliminer les doublons des résultats (par exemple, si plusieurs entrées ont le même nom)
    unique_results = {row['name']: row for row in results}.values()

    # Retourner les résultats sous forme de liste JSON
    return jsonify([
        {
            'name': row['name'],
            'flavor': row['flavor'],
            'type': row['type'],
            'origin': row['origin'],
            'ingredients': row['ingredients'],
            'image_path': row['image_path']
        } for row in unique_results
    ])