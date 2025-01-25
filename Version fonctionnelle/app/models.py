import sqlite3
import re


#fonction pour se connecter à la base de données
def get_db_connection():
    conn = sqlite3.connect('food_items.db')
    conn.row_factory = sqlite3.Row
    return conn

#fonction pour effectuer la recherche dans la base de données
def search_in_database(query, filter_type):
    query = query.lower()  # Convertir la requête en minuscule
    conn = get_db_connection()
    cursor = conn.cursor()

    # pour les ingéridents
    keywords = re.split(r"[ ,;:-]+", query.strip())

    conditions = []
    for word in keywords:
        conditions.append(f"LOWER(ingredients) LIKE '%{word.lower()}%'")

    # Combine les conditions avec 'AND'
    conditionsIngredients = " AND ".join(conditions)

    # Construire la requête SQL en fonction de l'argument 'filter_type'
    requete = '''
        SELECT name, flavor, type, origin, ingredients, image_path
        FROM FoodItems
        WHERE 
            (LOWER(name) LIKE ? || '%' OR
            LOWER(flavor) LIKE ? || '%' OR
            LOWER(type) LIKE ? || '%' OR
            LOWER(origin) LIKE ? || '%' OR
                ( '''+ conditionsIngredients +''' )
            )
    '''

    # si un filtre est donné, on ajoute une condition supplémentaire pour filtrer par type
    if filter_type != 'all':
        requete += ' AND LOWER(type) = ?'

    # Exécuter la requête
    params = (query, query, query, query)
    if filter_type != 'all':
        params += (filter_type,)

    cursor.execute(requete, params)
    results = cursor.fetchall()
    conn.close()

    return results


