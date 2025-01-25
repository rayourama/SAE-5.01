import sqlite3

#fonction pour se connecter à la base de données
def get_db_connection():
    conn = sqlite3.connect('food_items.db')
    conn.row_factory = sqlite3.Row
    return conn

#fonction pour effectuer la recherche dans la base de données
def search_in_database(query):
    query = query.lower()  #convertir la requête en minuscule
    conn = get_db_connection()
    cursor = conn.cursor()

    #ajuster la recherche pour matcher les débuts de mots
    cursor.execute('''
        SELECT name, flavor, type, origin, ingredients, image_path
        FROM FoodItems
        WHERE 
            LOWER(name) LIKE ? || '%' OR
            LOWER(name) LIKE '% ' || ? || '%' OR
            LOWER(flavor) LIKE ? || '%' OR
            LOWER(flavor) LIKE '% ' || ? || '%' OR
            LOWER(type) LIKE ? || '%' OR
            LOWER(type) LIKE '% ' || ? || '%' OR
            LOWER(origin) LIKE ? || '%' OR
            LOWER(origin) LIKE '% ' || ? || '%' OR
            LOWER(ingredients) LIKE ? || '%' OR
            LOWER(ingredients) LIKE '% ' || ? || '%'
    ''', (query, query, query, query, query, query, query, query, query, query))
    
    results = cursor.fetchall()
    conn.close()
    return results
