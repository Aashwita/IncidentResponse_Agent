import requests
from src.config import HINDSIGHT_API_KEY, HINDSIGHT_BASE_URL

class HindsightMemoryClient:
    def __init__(self):
        self.api_key = HINDSIGHT_API_KEY
        self.base_url = HINDSIGHT_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def add_memory(self, text_content: str, metadata: dict = None):
        endpoint = f"{self.base_url}/memories"
        payload = {
            "content": text_content,
            "metadata": metadata or {}
        }
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[Warning] Failed to write to Hindsight memory: {e}")
            return None

    def recall_memory(self, query: str, limit: int = 3):
        endpoint = f"{self.base_url}/memories/search"
        payload = {
            "query": query,
            "limit": limit
        }
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json().get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"[Warning] Failed to query Hindsight memory: {e}")
            return []