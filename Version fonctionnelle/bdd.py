import sqlite3

# nouvelle connexion à la base SQLite
conn = sqlite3.connect('food_items.db')
cursor = conn.cursor()

# création de la table FoodItems avec sucré/salé en texte
cursor.execute('''
CREATE TABLE IF NOT EXISTS FoodItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    name TEXT NOT NULL,  
    flavor TEXT NOT NULL,
    type TEXT NOT NULL,  
    origin TEXT, 
    ingredients TEXT, 
    image_path TEXT NOT NULL 
)
''')

# liste des aliments avec leurs informations
food_items = [
    ('Pizza Margherita', 'salé', 'plat', 'italien', 'tomate, mozzarella, basilic', '/static/images/pizza_margherita.jpg'),
    ('Sushi Saumon', 'salé', 'entrée', 'japonais', 'saumon, riz, algues', '/static/images/sushi_saumon.jpg'),
    ('Burger au Boeuf', 'salé', 'plat', 'américain', 'boeuf, pain, fromage, salade', '/static/images/burger_boeuf.jpg'),
    ('Salade César', 'salé', 'entrée', 'américain', 'poulet, salade romaine, parmesan, croûtons', '/static/images/salade_cesar.jpg'),
    ('Pâtes Carbonara', 'salé', 'plat', 'italien', 'spaghetti, lardons, oeufs, parmesan', '/static/images/pates_carbonara.jpg'),
]

# on insère ces aliments dans la table
cursor.executemany('''
INSERT INTO FoodItems (name, flavor, type, origin, ingredients, image_path)
VALUES (?, ?, ?, ?, ?, ?)
''', food_items)

# on sauvegarde et ferme la connexion
conn.commit()
conn.close()

print("Base de données créée et remplie avec succès.")