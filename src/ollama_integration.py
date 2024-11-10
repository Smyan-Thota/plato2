import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"

class LocalModel:
    def __init__(self, name):
        self.name = name
        self.api_url = OLLAMA_API_URL

    def query(self, prompt):
        """
        Query the local model with a prompt.
        """
        payload = {
            "model": self.name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            print(f"Error querying model: {e}")
            return None

def initialize_ollama_model(model_name):
    """
    Initialize the Ollama model.
    """
    return LocalModel(model_name)

def query_local_model(prompt):
    """
    Query the local model with a prompt.
    """
    model = LocalModel("openhermes")
    return model.query(prompt) 