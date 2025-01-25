from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import os

def create_app():
    app = Flask(__name__)

    app.config['TESTING'] = True

    # Configuration JWT
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    if app.config['SECRET_KEY'] == None :
        app.config['SECRET_KEY'] = "secret"

    # Activer CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Connexion à la base de données MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    app.db = client.food_selector

    # Configuration des formats d'images acceptés
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    UPLOAD_FOLDER = 'static/images'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

    # Enregistrement des routes
    from app.routes.routes_items import main_routes  # Import des routes pour la recherche
    from app.routes.routes_users import users_routes   # Import des routes pour l'authentification
    from app.routes.routes_favorites import favorites_routes   # Import des routes pour les favoris
    from app.routes.routes_recommendations import recommendations_routes   # Import des routes pour les recommendations
    from app.routes.routes_categories import categories_routes  # Import des routes pour les recommendations
    from app.routes.routes_admin import admin_routes  # Import des routes pour l'espace administrateur
    from app.routes.routes_food_items import food_items_routes # Import des routes pour food_items (API)
    
    app.register_blueprint(main_routes)
    app.register_blueprint(users_routes)
    app.register_blueprint(favorites_routes)
    app.register_blueprint(recommendations_routes)
    app.register_blueprint(categories_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(food_items_routes)

    return app