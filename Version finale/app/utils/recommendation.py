def analyze_preferences(favorites_data):
    # Dictionnaire pour stocker les préférences de l'utilisateur
    preferences = {
        "flavor": {},    # Préférences pour les saveurs
        "type": {},      # Préférences pour les types
        "origin": {},    # Préférences pour les origines
        "ingredients": {} # Préférences pour les ingrédients spécifiques
    }

    # Parcourt chaque plat favori pour extraire les préférences
    for favorite in favorites_data:
        # Récupère et compte les saveurs
        flavor = favorite.get("flavor", "").lower()
        if flavor:
            preferences["flavor"][flavor] = preferences["flavor"].get(flavor, 0) + 1

        # Récupère et compte les types de plats
        type_ = favorite.get("type", "").lower()
        if type_:
            preferences["type"][type_] = preferences["type"].get(type_, 0) + 1

        # Récupère et compte les origines des plats
        origin = favorite.get("origin", "").lower()
        if origin:
            preferences["origin"][origin] = preferences["origin"].get(origin, 0) + 1

        # Récupère et compte les ingrédients en les séparant par ", "
        ingredients = favorite.get("ingredients", "").lower().split(", ")
        for ingredient in ingredients:
            preferences["ingredients"][ingredient] = preferences["ingredients"].get(ingredient, 0) + 1

    # Transforme les préférences en une liste triable
    ranked_preferences = []
    for category, items in preferences.items():
        for name, points in items.items():
            ranked_preferences.append({
                "category": category,
                "name": name,
                "points": points
            })

    # Trie les préférences par score décroissant
    ranked_preferences.sort(key=lambda x: x["points"], reverse=True)
    return ranked_preferences


def build_filter_criteria(ranked_preferences):
    return {
        "$or": [
            # Filtre pour les saveurs
            {"flavor": {"$in": [p["name"] for p in ranked_preferences if p["category"] == "flavor"]}},
            # Filtre pour les types de plats
            {"type": {"$in": [p["name"] for p in ranked_preferences if p["category"] == "type"]}},
            # Filtre pour les origines
            {"origin": {"$in": [p["name"] for p in ranked_preferences if p["category"] == "origin"]}},
            # Filtre pour les ingrédients (utilise une regex pour correspondre partiellement)
            {"ingredients": {"$regex": "|".join([p["name"] for p in ranked_preferences if p["category"] == "ingredients"]), "$options": "i"}}
        ]
    }


# On calcule le score de chaque item afin de mettre en avant les plats qui pourraient possiblement plaire à l'utilisateur
def calculate_scores(all_items, ranked_preferences, favorite_names):
    scored_items = []
    for item in all_items:
        # Ignore les plats déjà favoris
        if item['name'] in favorite_names:
            continue

        score = 0  # Initialise le score pour chaque plat

        # Ajoute des points en fonction des préférences
        for preference in ranked_preferences:
            if preference["category"] == "flavor" and preference["name"] == item.get("flavor", "").lower():
                score += preference["points"]
            if preference["category"] == "type" and preference["name"] == item.get("type", "").lower():
                score += preference["points"]
            if preference["category"] == "origin" and preference["name"] == item.get("origin", "").lower():
                score += preference["points"]
            if preference["category"] == "ingredients" and preference["name"] in item.get("ingredients", "").lower():
                score += preference["points"] * 2  # Multiplie les points des ingrédients par 2 pour leur donner plus d'importance

        # Ajoute le plat avec son score calculé
        scored_items.append({**item, "score": score})
    return scored_items