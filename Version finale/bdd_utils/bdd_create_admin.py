from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.food_selector
collection = db.users

email = "admin@gmail.com"
password = "123"
is_admin = True

hashed_password = generate_password_hash(password)

# Ajout de l'utilisateur à la base de données
try:
    collection.insert_one({
        "email": email,
        "password": hashed_password,
        "is_admin": is_admin,
        "favorites": [],  # Initialisation des favoris
        "categories": []  # Initialisation des catégories personnalisées
    })
    print("User added ...")
except Exception as e:
    print("Error : "+e)

