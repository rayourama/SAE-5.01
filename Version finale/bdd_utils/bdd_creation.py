from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.food_selector
collection = db.food_items

# Supprimer la collection si elle existe déjà
collection.drop()

# Données à insérer
food_items = [
    {
        "name": "Pizza Margherita",
        "flavor": "salé",
        "type": "plat",
        "origin": "italien",
        "ingredients": "tomate, mozzarella, basilic",
        "image_path": "/static/images/pizza_margherita.jpg"
    },
    {
        "name": "Sushi Saumon",
        "flavor": "salé",
        "type": "entrée",
        "origin": "japonais",
        "ingredients": "saumon, riz, algues",
        "image_path": "/static/images/sushi_saumon.jpg"
    },
    {
        "name": "Burger au Boeuf",
        "flavor": "salé",
        "type": "plat",
        "origin": "américain",
        "ingredients": "boeuf, pain, fromage, salade",
        "image_path": "/static/images/burger_boeuf.jpg"
    },
    {
        "name": "Salade César",
        "flavor": "salé",
        "type": "entrée",
        "origin": "américain",
        "ingredients": "poulet, salade romaine, parmesan, croûtons",
        "image_path": "/static/images/salade_cesar.jpg"
    },
    {
        "name": "Pâtes Carbonara",
        "flavor": "salé",
        "type": "plat",
        "origin": "italien",
        "ingredients": "spaghetti, lardons, œufs, parmesan",
        "image_path": "/static/images/pates_carbonara.jpg"
    },
    {
        "name": "Crème brûlée",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "crème, œufs, sucre, vanille",
        "image_path": "/static/images/creme_brulee.jpg"
    },
    {
        "name": "Tiramisu",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "italien",
        "ingredients": "mascarpone, café, biscuits, cacao, œufs",
        "image_path": "/static/images/tiramisu.png"
    },
    {
        "name": "Fraisier",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "génoise, fraises, crème mousseline, pâte d'amande",
        "image_path": "/static/images/fraisier.png"
    },
    {
        "name": "Compote de Pommes",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "pommes, sucre, cannelle",
        "image_path": "/static/images/compotes_pommes.jpg"
    },
    {
        "name": "Fondant au Chocolat",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "chocolat noir, beurre, œufs, sucre, farine",
        "image_path": "/static/images/fondant_choco.jpg"
    },
    {
        "name": "Éclair au Chocolat",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "pâte à choux, chocolat, crème pâtissière",
        "image_path": "/static/images/eclair_choco.jpg"
    },
    {
        "name": "Mousse au Chocolat",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "chocolat, œufs, sucre, crème fraîche",
        "image_path": "/static/images/mousse_choco.jpg"
    },
    {
        "name": "Mille-feuilles",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "pâte feuilletée, crème pâtissière, sucre glace",
        "image_path": "/static/images/mille_feuilles.jpg"
    },
    {
        "name": "Île flottante",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "blancs d'œufs, sucre, vanille, crème anglaise",
        "image_path": "/static/images/ile_flottante.jpg"
    },
    {
        "name": "Paris-Brest",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "pâte à choux, crème pralinée, amandes",
        "image_path": "/static/images/paris_brest.jpg"
    },
    {
        "name": "Trianon au Chocolat",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "mousse au chocolat, dacquoise, praliné",
        "image_path": "/static/images/trianon_chocolat.jpg"
    },
    {
        "name": "Tarte Tatin",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "pommes, pâte brisée, sucre, beurre",
        "image_path": "/static/images/tarte_tatin.jpg"
    },
    {
        "name": "Riz au Lait",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "riz, lait, sucre, vanille",
        "image_path": "/static/images/riz_au_lait.jpg"
    },
    {
        "name": "Crumble aux Pommes",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "anglais",
        "ingredients": "pommes, sucre, farine, beurre, cannelle",
        "image_path": "/static/images/crumble_pommes.jpg"
    },
    {
        "name": "Brioche Perdue",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "brioche, œufs, lait, sucre, cannelle",
        "image_path": "/static/images/brioche_perdue.jpg"
    },
    {
        "name": "Cornes de Gazelle",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "marocain",
        "ingredients": "pâte d'amande, fleur d'oranger, cannelle, sucre glace",
        "image_path": "/static/images/cornes_gazelles.jpg"
    },
    {
        "name": "Mochi",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "japonais",
        "ingredients": "riz gluant, sucre, pâte de haricots rouges",
        "image_path": "/static/images/mochi.jpg"
    },
    {
        "name": "Donuts Sucrés au Sucre",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "américain",
        "ingredients": "farine, sucre, levure, œufs, lait, huile",
        "image_path": "/static/images/donuts.jpg"
    },
    {
        "name": "Msemen au Nutella",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "marocain",
        "ingredients": "farine, beurre, Nutella, sucre",
        "image_path": "/static/images/msemen_nutella.jpg"
    },
    {
        "name": "Bounty Cake",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "pacifique sud",
        "ingredients": "chocolat, noix de coco, sucre, farine, œufs",
        "image_path": "/static/images/bounty_cake.jpg"
    },
    {
        "name": "Flan Coco",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "caraïbes",
        "ingredients": "lait de coco, sucre, œufs, vanille",
        "image_path": "/static/images/flan_coco.jpg"
    },
    {
        "name": "Churros",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "amérique latine",
        "ingredients": "farine, sucre, sel, huile, cannelle",
        "image_path": "/static/images/churros.jpg"
    },
    {
        "name": "Açaí Bowl",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "brésilien",
        "ingredients": "açaí, fruits frais, granola, miel",
        "image_path": "/static/images/açai_bowl.jpg"
    },
    {
        "name": "Sago Pudding",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "asie du sud-est",
        "ingredients": "sago, lait de coco, sucre, vanille",
        "image_path": "/static/images/sago_pudding.jpg"
    },
    {
        "name": "Feijoada",
        "flavor": "salé",
        "type": "plat",
        "origin": "brésilien",
        "ingredients": "haricots noirs, viande de porc, riz",
        "image_path": "/static/images/feijoada.jpg"
    },
    {
        "name": "Paella",
        "flavor": "salé",
        "type": "plat",
        "origin": "espagnol",
        "ingredients": "riz, fruits de mer, safran, légumes",
        "image_path": "/static/images/paella.jpg"
    },
    {
        "name": "Colombo de Poulet",
        "flavor": "salé",
        "type": "plat",
        "origin": "antillais",
        "ingredients": "poulet, curry, légumes, riz",
        "image_path": "/static/images/colombo_poulet.jpg"
    },
    {
        "name": "Tajine d'Agneau",
        "flavor": "salé",
        "type": "plat",
        "origin": "marocain",
        "ingredients": "agneau, abricots secs, amandes, épices",
        "image_path": "/static/images/tajine_agneau.jpg"
    },
    {
        "name": "Osso Buco",
        "flavor": "salé",
        "type": "plat",
        "origin": "italien",
        "ingredients": "jarret de veau, tomate, citron, vin blanc",
        "image_path": "/static/images/osso_buco.jpg"
    },
    {
        "name": "Yakitori de Poulet",
        "flavor": "salé",
        "type": "plat",
        "origin": "japonais",
        "ingredients": "poulet, sauce soja, saké, sucre",
        "image_path": "/static/images/yakitori_poulet.jpg"
    },
    {
        "name": "Fish and Chips",
        "flavor": "salé",
        "type": "plat",
        "origin": "britannique",
        "ingredients": "poisson frit, frites, sauce tartare",
        "image_path": "/static/images/fish_chips.jpg"
    },
    {
        "name": "Curry Vert Thaï",
        "flavor": "salé",
        "type": "plat",
        "origin": "thaïlandais",
        "ingredients": "lait de coco, poulet, curry vert, légumes",
        "image_path": "/static/images/curry_vert_thai.jpg"
    },
    {
        "name": "Poulet Tikka Masala",
        "flavor": "salé",
        "type": "plat",
        "origin": "indien",
        "ingredients": "poulet, épices, sauce tomate",
        "image_path": "/static/images/poulet_tikka_masala.png"
    },
    {
        "name": "Biryani de Poulet",
        "flavor": "salé",
        "type": "plat",
        "origin": "indien",
        "ingredients": "riz, poulet, épices, yaourt",
        "image_path": "/static/images/biryani_poulet.jpg"
    },
    {
        "name": "Raclette Savoyarde",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "fromage, pommes de terre, charcuterie",
        "image_path": "/static/images/raclette.jpg"
    },
    {
        "name": "Poutine",
        "flavor": "salé",
        "type": "plat",
        "origin": "canadien",
        "ingredients": "frites, fromage en grains, sauce brune",
        "image_path": "/static/images/poutine.jpg"
    },
    {
        "name": "Bibimbap",
        "flavor": "salé",
        "type": "plat",
        "origin": "coréen",
        "ingredients": "riz, légumes, bœuf, œuf, sauce gochujang",
        "image_path": "/static/images/bibimbap.jpg"
    },
    {
        "name": "Enchiladas",
        "flavor": "salé",
        "type": "plat",
        "origin": "mexicain",
        "ingredients": "tortillas, poulet, sauce tomate, fromage",
        "image_path": "/static/images/enchiladas.jpg"
    },
    {
        "name": "Bruschetta",
        "flavor": "salé",
        "type": "entrée",
        "origin": "italien",
        "ingredients": "pain grillé, tomates, basilic, ail",
        "image_path": "/static/images/bruschetta.jpg"
    },
    {
        "name": "Gyoza",
        "flavor": "salé",
        "type": "entrée",
        "origin": "japonais",
        "ingredients": "farce de porc, pâte fine, sauce soja",
        "image_path": "/static/images/gyoza.jpg"
    },
    {
        "name": "Houmous",
        "flavor": "salé",
        "type": "entrée",
        "origin": "moyen-orient",
        "ingredients": "pois chiches, tahini, citron, ail",
        "image_path": "/static/images/houmous.jpg"
    },
    {
        "name": "Carpaccio de Bœuf",
        "flavor": "salé",
        "type": "entrée",
        "origin": "italien",
        "ingredients": "bœuf cru, parmesan, roquette, citron",
        "image_path": "/static/images/carpaccio_boeuf.jpg"
    },
    {
        "name": "Salade Caprese",
        "flavor": "salé",
        "type": "entrée",
        "origin": "italien",
        "ingredients": "tomates, mozzarella, basilic, huile d'olive",
        "image_path": "/static/images/salade_caprese.jpg"
    },
    {
        "name": "Oeuf Mimosa",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "œufs durs, mayonnaise, moutarde",
        "image_path": "/static/images/oeuf_mimosa.jpg"
    },
    {
        "name": "Ceviche de Poisson",
        "flavor": "salé",
        "type": "entrée",
        "origin": "péruvien",
        "ingredients": "poisson cru, citron vert, coriandre, oignons",
        "image_path": "/static/images/ceviche_poisson.jpg"
    },
    {
        "name": "Soupe à l’Oignon",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "oignons, bouillon, pain, fromage",
        "image_path": "/static/images/soupe_oignon.jpg"
    },
    {
        "name": "Tartare de Saumon",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "saumon cru, citron, câpres, herbes",
        "image_path": "/static/images/tartare_saumon.jpg"
    },
    {
        "name": "Samoussa Légumes",
        "flavor": "salé",
        "type": "entrée",
        "origin": "indien",
        "ingredients": "pâte fine, légumes, épices",
        "image_path": "/static/images/samoussa_legumes.jpg"
    },
    {
        "name": "Guacamole",
        "flavor": "salé",
        "type": "entrée",
        "origin": "mexicain",
        "ingredients": "avocat, citron vert, oignons, tomates",
        "image_path": "/static/images/guacamole.jpg"
    },
    {
        "name": "Foie Gras",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "foie gras, pain, confit d'oignons",
        "image_path": "/static/images/foie_gras.jpg"
    },
    {
        "name": "Borek",
        "flavor": "salé",
        "type": "entrée",
        "origin": "turc",
        "ingredients": "pâte filo, fromage, épinards",
        "image_path": "/static/images/borek.jpg"
    },
    {
        "name": "Falafels",
        "flavor": "salé",
        "type": "entrée",
        "origin": "moyen-orient",
        "ingredients": "pois chiches, herbes, épices",
        "image_path": "/static/images/falafels.jpg"
    },
    {
        "name": "Gaspacho",
        "flavor": "salé",
        "type": "entrée",
        "origin": "espagnol",
        "ingredients": "tomates, poivrons, concombre, ail",
        "image_path": "/static/images/gaspacho.jpg"
    },
    {
        "name": "Salade de Quinoa",
        "flavor": "salé",
        "type": "entrée",
        "origin": "péruvien",
        "ingredients": "quinoa, légumes, citron, huile d'olive",
        "image_path": "/static/images/salade_quinoa.jpg"
    },
    {
        "name": "Rouleaux de Printemps",
        "flavor": "salé",
        "type": "entrée",
        "origin": "vietnamien",
        "ingredients": "riz, crevettes, légumes, sauce nuoc-mâm",
        "image_path": "/static/images/rouleaux_printemps.jpg"
    },
    {
        "name": "Blinis au Saumon",
        "flavor": "salé",
        "type": "entrée",
        "origin": "russe",
        "ingredients": "blinis, saumon fumé, crème fraîche",
        "image_path": "/static/images/blinis_saumon.jpg"
    },
    {
        "name": "Calamars Frits",
        "flavor": "salé",
        "type": "entrée",
        "origin": "méditerranéen",
        "ingredients": "calamars, chapelure, citron, épices",
        "image_path": "/static/images/calamars_frits.jpg"
    },
    {
        "name": "Salade de Lentilles",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "lentilles, carottes, vinaigrette, herbes",
        "image_path": "/static/images/salade_lentilles.jpg"
    },
    {
        "name": "Cassoulet",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "haricots blancs, saucisses, confit de canard, porc",
        "image_path": "/static/images/cassoulet.jpg"
    },
    {
        "name": "Kebab",
        "flavor": "salé",
        "type": "plat",
        "origin": "turc",
        "ingredients": "viande grillée, pain pita, légumes, sauce",
        "image_path": "/static/images/kebab.jpg"
    },
    {
        "name": "Coq au Vin",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "poulet, vin rouge, champignons, lardons",
        "image_path": "/static/images/coq_au_vin.jpg"
    },
    {
        "name": "Poulet Basquaise",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "poulet, tomates, poivrons, piment",
        "image_path": "/static/images/poulet_basquaise.jpg"
    },
    {
        "name": "Hachis Parmentier",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "purée de pommes de terre, bœuf haché, oignons",
        "image_path": "/static/images/hachis_parmentier.jpg"
    },
    {
        "name": "Lasagnes",
        "flavor": "salé",
        "type": "plat",
        "origin": "italien",
        "ingredients": "pâtes, sauce bolognaise, béchamel, fromage",
        "image_path": "/static/images/lasagnes.jpg"
    },
    {
        "name": "Poulet Rôti et Pommes de Terre",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "poulet rôti, pommes de terre, herbes",
        "image_path": "/static/images/poulet_roti.jpg"
    },
    {
        "name": "Ratatouille",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "courgettes, aubergines, tomates, poivrons, herbes",
        "image_path": "/static/images/ratatouille.jpg"
    },
    {
        "name": "Steak Frites",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "steak de bœuf, frites, sauce au choix",
        "image_path": "/static/images/steak_frites.jpg"
    },
    {
        "name": "Couscous Royal",
        "flavor": "salé",
        "type": "plat",
        "origin": "maghrébin",
        "ingredients": "semoule, légumes, agneau, merguez, épices",
        "image_path": "/static/images/couscous_royal.jpg"
    },
    {
        "name": "Tajine de Poulet aux Citrons Confits",
        "flavor": "salé",
        "type": "plat",
        "origin": "marocain",
        "ingredients": "poulet, citrons confits, olives, épices",
        "image_path": "/static/images/tajine_citron.jpg"
    },
    {
        "name": "Boeuf Bourguignon",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "bœuf, vin rouge, champignons, carottes, oignons",
        "image_path": "/static/images/boeuf_bourguignon.jpg"
    },
    {
        "name": "Chili con Carne",
        "flavor": "salé",
        "type": "plat",
        "origin": "mexicain",
        "ingredients": "bœuf haché, haricots rouges, tomates, piments",
        "image_path": "/static/images/chili_con_carne.jpg"
    },
    {
        "name": "Carbonade Flamande",
        "flavor": "salé",
        "type": "plat",
        "origin": "belge",
        "ingredients": "bœuf, bière, oignons, pain d'épices",
        "image_path": "/static/images/carbonade.jpg"
    },
    {
        "name": "Poulet Curry",
        "flavor": "salé",
        "type": "plat",
        "origin": "indien",
        "ingredients": "poulet, lait de coco, curry, épices",
        "image_path": "/static/images/poulet_curry.jpg"
    },
    {
        "name": "Canelones",
        "flavor": "salé",
        "type": "plat",
        "origin": "espagnol",
        "ingredients": "pâtes, viande hachée, sauce béchamel, fromage",
        "image_path": "/static/images/canelones.jpg"
    },
    {
        "name": "Rôti de Porc aux Pommes",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "porc, pommes, thym, sauce au cidre",
        "image_path": "/static/images/roti_porc.jpg"
    },
    {
        "name": "Fajitas",
        "flavor": "salé",
        "type": "plat",
        "origin": "mexicain",
        "ingredients": "tortillas, poulet ou bœuf, légumes, épices",
        "image_path": "/static/images/fajitas.jpg"
    },
    {
        "name": "Soupe Pho",
        "flavor": "salé",
        "type": "plat",
        "origin": "vietnamien",
        "ingredients": "nouilles de riz, bœuf ou poulet, bouillon, herbes",
        "image_path": "/static/images/pho.jpg"
    },
    {
        "name": "Quiche Lorraine",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "pâte brisée, lardons, œufs, crème",
        "image_path": "/static/images/quiche_lorraine.jpg"
    },
    {
        "name": "Goulash",
        "flavor": "salé",
        "type": "plat",
        "origin": "hongrois",
        "ingredients": "bœuf, paprika, pommes de terre, légumes",
        "image_path": "/static/images/goulash.jpg"
    },
    {
        "name": "Risotto aux Champignons",
        "flavor": "salé",
        "type": "plat",
        "origin": "italien",
        "ingredients": "riz arborio, champignons, parmesan, vin blanc",
        "image_path": "/static/images/risotto_champignons.jpg"
    },
    {
        "name": "Tartiflette",
        "flavor": "salé",
        "type": "plat",
        "origin": "français",
        "ingredients": "pommes de terre, reblochon, lardons, oignons",
        "image_path": "/static/images/tartiflette.jpg"
    },
    {
        "name": "Soupe de Poisson",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "poisson, tomate, ail, safran, croûtons",
        "image_path": "/static/images/soupe_poisson.jpg"
    },
    {
        "name": "Croustillants de Chèvre au Miel",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "fromage de chèvre, miel, feuilles de brick",
        "image_path": "/static/images/croustillants_chevre.jpg"
    },
    {
        "name": "Caprese aux Fraises",
        "flavor": "salé-sucré",
        "type": "entrée",
        "origin": "italien",
        "ingredients": "mozzarella, fraises, basilic, vinaigre balsamique",
        "image_path": "/static/images/caprese_fraises.jpg"
    },
    {
        "name": "Houmous à la Betterave",
        "flavor": "salé",
        "type": "entrée",
        "origin": "moyen-orient",
        "ingredients": "pois chiches, betterave, tahini, citron",
        "image_path": "/static/images/houmous_betterave.jpg"
    },
    {
        "name": "Tartare de Dorade",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "dorade, citron vert, coriandre, huile d'olive",
        "image_path": "/static/images/tartare_dorade.jpg"
    },
    {
        "name": "Caviar d'Aubergines",
        "flavor": "salé",
        "type": "entrée",
        "origin": "méditerranéen",
        "ingredients": "aubergines, ail, huile d'olive, citron",
        "image_path": "/static/images/caviar_aubergines.jpg"
    },
    {
        "name": "Brochettes de Crevettes Marinées",
        "flavor": "salé",
        "type": "entrée",
        "origin": "méditerranéen",
        "ingredients": "crevettes, ail, citron, persil",
        "image_path": "/static/images/brochettes_crevettes.jpg"
    },
    {
        "name": "Velouté de Courgettes à la Menthe",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "courgettes, crème, menthe, oignons",
        "image_path": "/static/images/veloute_courgettes.jpg"
    },
    {
        "name": "Salade Thaï aux Crevettes",
        "flavor": "salé-épicé",
        "type": "entrée",
        "origin": "thaïlandais",
        "ingredients": "crevettes, coriandre, citronnelle, chili",
        "image_path": "/static/images/salade_thai_crevettes.jpg"
    },
    {
        "name": "Beignets de Morue",
        "flavor": "salé",
        "type": "entrée",
        "origin": "portugais",
        "ingredients": "morue, pommes de terre, ail, persil",
        "image_path": "/static/images/beignets_morue.jpg"
    },
    {
        "name": "Taboulé Libanais",
        "flavor": "salé",
        "type": "entrée",
        "origin": "libanais",
        "ingredients": "persil, menthe, boulgour, tomates",
        "image_path": "/static/images/taboule_libanais.jpg"
    },
    {
        "name": "Carpaccio de Saint-Jacques",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "coquilles Saint-Jacques, citron, huile d'olive, aneth",
        "image_path": "/static/images/carpaccio_stjacques.jpg"
    },
    {
        "name": "Avocat Feta Grenade",
        "flavor": "salé",
        "type": "entrée",
        "origin": "méditerranéen",
        "ingredients": "avocat, feta, graines de grenade, huile d'olive",
        "image_path": "/static/images/avocat_feta_grenade.jpg"
    },
    {
        "name": "Tartare de Tomates et Basilic",
        "flavor": "salé",
        "type": "entrée",
        "origin": "italien",
        "ingredients": "tomates, basilic, huile d'olive, pignons de pin",
        "image_path": "/static/images/tartare_tomates_basilic.jpg"
    },
    {
        "name": "Salade de Pois Chiches et Épinards",
        "flavor": "salé",
        "type": "entrée",
        "origin": "méditerranéen",
        "ingredients": "pois chiches, épinards, citron, cumin",
        "image_path": "/static/images/salade_pois_chiches_epinards.jpg"
    },
    {
        "name": "Crème de Potiron au Lait de Coco",
        "flavor": "salé-doux",
        "type": "entrée",
        "origin": "fusion",
        "ingredients": "potiron, lait de coco, gingembre, coriandre",
        "image_path": "/static/images/creme_potiron_coco.jpg"
    },
    {
        "name": "Tartine aux Rillettes de Saumon",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "saumon, fromage frais, aneth, citron",
        "image_path": "/static/images/tartine_rillettes_saumon.jpg"
    },
    {
        "name": "Choux Farcis Miniatures",
        "flavor": "salé",
        "type": "entrée",
        "origin": "européen",
        "ingredients": "chou, viande hachée, riz, épices",
        "image_path": "/static/images/choux_farcis_miniatures.jpg"
    },
    {
        "name": "Ravioles au Fromage et à la Truffe",
        "flavor": "salé",
        "type": "entrée",
        "origin": "italien",
        "ingredients": "pâtes fraîches, ricotta, truffe, beurre",
        "image_path": "/static/images/ravioles_truffe.jpg"
    },
    {
        "name": "Gaspacho Vert",
        "flavor": "salé",
        "type": "entrée",
        "origin": "espagnol",
        "ingredients": "concombre, avocat, basilic, citron vert",
        "image_path": "/static/images/gaspacho_vert.jpg"
    },
    {
        "name": "Œufs Cocotte aux Épinards",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "œufs, épinards, crème, noix de muscade",
        "image_path": "/static/images/oeufs_cocotte_epinards.jpg"
    },
    {
        "name": "Tartelette aux Champignons",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "pâte feuilletée, champignons, crème, persil",
        "image_path": "/static/images/tartelette_champignons.jpg"
    },
    {
        "name": "Gratin de Fenouil au Parmesan",
        "flavor": "salé",
        "type": "entrée",
        "origin": "italien",
        "ingredients": "fenouil, parmesan, crème, muscade",
        "image_path": "/static/images/gratin_fenouil_parmesan.jpg"
    },
    {
        "name": "Tempura de Légumes",
        "flavor": "salé",
        "type": "entrée",
        "origin": "japonais",
        "ingredients": "carottes, courgettes, pâte à tempura, huile",
        "image_path": "/static/images/tempura_legumes.jpg"
    },
    {
        "name": "Rouleaux de Saumon Fumé au Fromage Frais",
        "flavor": "salé",
        "type": "entrée",
        "origin": "fusion",
        "ingredients": "saumon fumé, fromage frais, ciboulette, citron",
        "image_path": "/static/images/rouleaux_saumon_fume.jpg"
    },
    {
        "name": "Tarte Fine à l'Oignon",
        "flavor": "salé",
        "type": "entrée",
        "origin": "français",
        "ingredients": "pâte feuilletée, oignons, crème, thym",
        "image_path": "/static/images/tarte_fine_oignon.jpg"
    },
    {
        "name": "Salade de Mangue et Crevettes",
        "flavor": "salé-doux",
        "type": "entrée",
        "origin": "fusion",
        "ingredients": "mangue, crevettes, menthe, vinaigrette",
        "image_path": "/static/images/salade_mangue_crevettes.jpg"
    },
    {
        "name": "Cheesecake",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "américain",
        "ingredients": "fromage à la crème, biscuits, sucre, vanille",
        "image_path": "/static/images/cheesecake.jpg"
    },
    {
        "name": "Pavlova",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "australien",
        "ingredients": "meringue, crème fouettée, fruits frais",
        "image_path": "/static/images/pavlova.jpg"
    },
    {
        "name": "Baklava",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "moyen-orient",
        "ingredients": "pâte phyllo, noix, miel, cannelle",
        "image_path": "/static/images/baklava.png"
    },
    {
        "name": "Brownie",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "américain",
        "ingredients": "chocolat, beurre, sucre, farine, noix",
        "image_path": "/static/images/brownie.jpg"
    },
    {
        "name": "Flan",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "espagnol",
        "ingredients": "lait, sucre, œufs, caramel",
        "image_path": "/static/images/flan.jpg"
    },
    {
        "name": "Profiteroles",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "pâte à choux, glace, chocolat fondu",
        "image_path": "/static/images/profiteroles.jpg"
    },
    {
        "name": "Macarons",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "poudre d'amande, sucre glace, blancs d'œufs, ganache",
        "image_path": "/static/images/macarons.jpg"
    },
    {
        "name": "Panna Cotta",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "italien",
        "ingredients": "crème, sucre, gélatine, vanille",
        "image_path": "/static/images/panna_cotta.jpg"
    },
    {
        "name": "Tarte au Citron Meringuée",
        "flavor": "sucré",
        "type": "dessert",
        "origin": "français",
        "ingredients": "pâte sablée, citron, sucre, meringue",
        "image_path": "/static/images/tarte_citron.jpg"
    }

]

#reinsérer les documents dans la collection
collection.insert_many(food_items)
print("Base de données MongoDB créée et remplie avec succès.")
