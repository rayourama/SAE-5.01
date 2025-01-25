from flask import Blueprint, request, jsonify, render_template
from .models import search_in_database

# Création d'un blueprint pour les routes principales
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return render_template('template.html')

@main_routes.route('/api/search', methods=['GET'])
def search_items():
    query = request.args.get('query', '').lower()
    filter_type = request.args.get('type', 'all').lower()
    results = search_in_database(query, filter_type)

    # Éliminer les doublons
    unique_results = {row['name']: row for row in results}.values()

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