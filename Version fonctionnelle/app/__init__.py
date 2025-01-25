from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Activer CORS pour l'application
    CORS(app)  # Autorise toutes les origines

    # Enregistrer les blueprints pour les routes
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app