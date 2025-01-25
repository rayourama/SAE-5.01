import re
from flask import current_app
from Levenshtein import distance

def search_in_database(query, filter_type, max_distance=1): #la marge d'erreur peut etre changé avec le parametre "max_distance"

    collection = current_app.db["food_items"]

    #si la requête est vide on retourne tous les items
    if not query.strip():
        if filter_type == 'all':
            return list(collection.find({}, {"_id": 0}))
        else:
            return list(collection.find({"type": {"$regex": f"^{filter_type}", "$options": "i"}}, {"_id": 0}))

    #découpe la requête en mots
    query_words = re.split(r"\s+", query.strip().lower())

    search_filter = {
        "$or": [
            {"name": {"$exists": True}},
            {"flavor": {"$exists": True}},
            {"type": {"$exists": True}},
            {"origin": {"$exists": True}},
            {"ingredients": {"$exists": True}},
        ]
    }
    if filter_type != 'all':
        search_filter = {
            "$and": [
                search_filter,
                {"type": {"$regex": f"^{filter_type}", "$options": "i"}}
            ]
        }
    #récupérer les éléments de la base de données
    results = list(collection.find(search_filter, {"_id": 0}))

    #fonction pour vérifier si un mot correspond à un champ
    def is_match(query_word, field_value):
        field_words = re.split(r"\s+", field_value.lower())
        for field_word in field_words:
            #correspondance exacte par début de mot 
            if field_word.startswith(query_word):
                return True
            #vérifier la distance de Levenshtein entre le mot recherché et le mot dans la barre
            if distance(query_word, field_word) <= max_distance:
                return True
        return False

    #filtrer les résultats
    refined_results = []
    for item in results:
        all_words_matched = True  #tous les mots doivent correspondre
        for query_word in query_words:  #pour chaque mot dans la requête
            word_matched = False
            for field in ["name", "flavor", "type", "origin", "ingredients"]:
                field_value = str(item.get(field, "")).lower()
                if field_value and is_match(query_word, field_value):
                    word_matched = True
                    break
            if not word_matched:  #si un mot de la requête ne correspond pas on exclu l'élément
                all_words_matched = False
                break
        if all_words_matched:
            refined_results.append(item)

    return refined_results