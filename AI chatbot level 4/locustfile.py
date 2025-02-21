from locust import HttpUser, task, between

class ChatbotLoadTest(HttpUser):
    wait_time = between(0.01, 0.05)  # Simulates heavy traffic

    @task
    def test_chat(self):
        self.client.post("/chat", json={"character": "iron man", "user_message": "Who are you?"})
