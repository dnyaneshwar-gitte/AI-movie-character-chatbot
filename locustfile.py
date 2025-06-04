from locust import HttpUser, task, between

class MovieChatUser(HttpUser):
    wait_time = between(1, 3)  # seconds to wait between tasks

    @task(3)
    def chat(self):
        self.client.post("/chat", json={
            "character": "iron man",
            "user_message": "What's your latest invention?"
        })

    @task(1)
    def scrape(self):
        self.client.post("/scrape", json={
            "url": "https://www.imsdb.com/scripts/avengers-endgame.html"
        })
