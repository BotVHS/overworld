"""
Ollama Client - Integració amb Ollama per generació procedural

Connecta amb Ollama local per generar contingut emergent
"""
import json
import requests
from typing import Dict, Optional, Any
import time


class OllamaClient:
    """
    Client per interactuar amb Ollama

    Usa l'API local d'Ollama per generar sistemes emergents
    """

    def __init__(
        self,
        host: str = "http://localhost:11434",
        model: str = "llama3.2:3b",
        timeout: int = 60
    ):
        """
        Args:
            host: Host d'Ollama (per defecte local)
            model: Model a usar (llama3.2:3b o llama3.1:8b)
            timeout: Timeout en segons
        """
        self.host = host
        self.model = model
        self.timeout = timeout
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Comprova si Ollama està disponible"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.8,
        max_retries: int = 3
    ) -> Optional[str]:
        """
        Genera text amb Ollama

        Args:
            prompt: Prompt per a la generació
            system: System prompt (opcional)
            temperature: Temperatura de generació (0-1)
            max_retries: Nombre màxim de reintents

        Returns:
            Text generat o None si falla
        """
        if not self.available:
            print("⚠️  Ollama no disponible, usant fallback")
            return None

        url = f"{self.host}/api/generate"

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        if system:
            data["system"] = system

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    json=data,
                    timeout=self.timeout
                )

                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "")
                else:
                    print(f"⚠️  Ollama error {response.status_code}: {response.text}")
                    time.sleep(1)

            except requests.exceptions.Timeout:
                print(f"⚠️  Ollama timeout (intent {attempt + 1}/{max_retries})")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️  Ollama error: {e}")
                time.sleep(1)

        return None

    def generate_json(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7
    ) -> Optional[Dict]:
        """
        Genera JSON estructurat amb Ollama

        Args:
            prompt: Prompt que demana JSON
            system: System prompt
            temperature: Temperatura

        Returns:
            Dict parseado del JSON o None si falla
        """
        # Afegeix instruccions explícites per JSON
        json_prompt = f"{prompt}\n\nRESPON NOMÉS AMB JSON VÀLID, SENSE EXPLICACIONS EXTRA."

        response = self.generate(json_prompt, system, temperature)

        if response is None:
            return None

        # Intenta extreure JSON de la resposta
        try:
            # Neteja la resposta (elimina markdown, etc.)
            cleaned = response.strip()

            # Elimina possibles markdown code blocks
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]

            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            # Parsea JSON
            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            print(f"⚠️  Error parseant JSON d'Ollama: {e}")
            print(f"Resposta rebuda: {response[:200]}...")
            return None


# Instància global (singleton)
_ollama_instance: Optional[OllamaClient] = None


def get_ollama_client(
    host: str = "http://localhost:11434",
    model: str = "llama3.2:3b"
) -> OllamaClient:
    """
    Obté la instància global del client Ollama

    Args:
        host: Host d'Ollama
        model: Model a usar

    Returns:
        Client d'Ollama
    """
    global _ollama_instance

    if _ollama_instance is None:
        _ollama_instance = OllamaClient(host=host, model=model)

    return _ollama_instance
