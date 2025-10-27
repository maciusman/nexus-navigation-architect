"""
OpenRouter API Client
"""
import requests
from typing import List, Dict, Optional


class OpenRouterClient:
    """Klient do komunikacji z OpenRouter API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://nexus-navigation-architect.local",
            "X-Title": "Nexus Navigation Architect"
        }

    def list_models(self) -> List[Dict]:
        """Pobierz listę dostępnych modeli"""
        response = requests.get(
            f"{self.base_url}/models",
            headers=self.headers
        )
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])

    def chat_completion(
        self,
        model_id: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 4000,
        temperature: float = 0
    ) -> Dict:
        """Wykonaj chat completion"""
        payload = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def get_response_text(self, response: Dict) -> str:
        """Wyciągnij tekst odpowiedzi z response"""
        try:
            return response['choices'][0]['message']['content'].strip()
        except (KeyError, IndexError) as e:
            raise ValueError(f"Nieprawidłowa struktura odpowiedzi: {e}")

    def test_connection(self) -> bool:
        """Testuj połączenie z API"""
        try:
            self.list_models()
            return True
        except Exception:
            return False
