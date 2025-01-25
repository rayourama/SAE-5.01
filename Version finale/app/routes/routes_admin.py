from flask import Blueprint, render_template

# Création d'un blueprint pour gérer les routes principales
admin_routes = Blueprint('admin', __name__)

# Route principale pour afficher la page d'accueil
@admin_routes.route('/admin/')
def index():
    # Rend le template HTML principal
    return render_template('admin.html')

