import os
from flask import current_app, Blueprint, request, jsonify
from bson import ObjectId
from werkzeug.utils import secure_filename

food_items_routes = Blueprint('food_items_routes', __name__)

# Fonction pour vérifier l'extension de fichier
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Récupérer tous les plats
@food_items_routes.route('/api/food_items', methods=['GET'])
def get_food_items():
    collection = current_app.db["food_items"]
    food_items = list(collection.find({}, {"_id": 1, "name": 1, "flavor": 1, "type": 1, "origin": 1, "ingredients": 1, "image_path": 1}))
    for item in food_items:
        item['_id'] = str(item['_id'])
    return jsonify(food_items)

# Récupérer un plat par ID
@food_items_routes.route('/api/food_items/<id>', methods=['GET'])
def get_food_item_by_id(id):
    collection = current_app.db["food_items"]
    try:
        food_item = collection.find_one({"_id": ObjectId(id)}, {"_id": 1, "name": 1, "flavor": 1, "type": 1, "origin": 1, "ingredients": 1, "image_path": 1})
        if food_item:
            food_item['_id'] = str(food_item['_id'])  # Convertir l'ObjectId en chaîne de caractères
            return jsonify(food_item), 200
        else:
            return jsonify({"error": "Plat non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération du plat: {str(e)}"}), 400

# Ajouter un plat
@food_items_routes.route('/api/food_items', methods=['POST'])
def add_food_item():
    collection = current_app.db["food_items"]
    name = request.form.get('name')
    flavor = request.form.get('flavor')
    type = request.form.get('type')
    origin = request.form.get('origin')
    ingredients = request.form.get('ingredients')
    image = request.files.get('image')

    image_path = None
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        # print("Répertoire du script:", script_dir)

        image_path = os.path.join(script_dir+"/../"+current_app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        image_path = f'/static/images/{filename}'

    food_item = {
        "name": name,
        "flavor": flavor,
        "type": type,
        "origin": origin,
        "ingredients": ingredients,
        "image_path": image_path
    }

    collection.insert_one(food_item)
    return jsonify({"message": "Plat ajouté avec succès"}), 201

# Modifier un plat
@food_items_routes.route('/api/food_items/<id>', methods=['PUT'])
def update_food_item(id):
    collection = current_app.db["food_items"]
    name = request.form.get('name')
    flavor = request.form.get('flavor')
    type = request.form.get('type')
    origin = request.form.get('origin')
    ingredients = request.form.get('ingredients')
    image = request.files.get('image')

    update_fields = {
        "name": name,
        "flavor": flavor,
        "type": type,
        "origin": origin,
        "ingredients": ingredients,
    }

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        update_fields["image_path"] = f'/static/images/{filename}'

    collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
    return jsonify({"message": "Plat mis à jour"}), 200

# Supprimer un plat
@food_items_routes.route('/api/food_items/<id>', methods=['DELETE'])
def delete_food_item(id):
    collection = current_app.db["food_items"]
    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Plat supprimé"}), 200
