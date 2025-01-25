from locust import HttpUser, task, between

class FlaskUser(HttpUser):
    wait_time = between(1, 3)  # Temps d'attente entre les requêtes

    @task
    def get_all_food_items(self):
        self.client.get("/api/food_items")  # Endpoint Flask à tester

    @task
    def add_food_item(self):
        self.client.post("/api/food_items", json={
            "name": "Pizza",
            "flavor": "salé",
            "type": "plat",
            "origin": "italien",
            "ingredients": "fromage, tomate"
        })

    @task
    def update_food_item(self):
        self.client.put("/api/food_items/677cb608e44e30ad7a7aa21d", json={
            "name": "Pizza 4 fromages"
        })

    @task
    def delete_food_item(self):
        self.client.delete("/api/food_items/677cb608e44e30ad7a7aa21d")
