"""
Civilization AI Models - Models IA únics per cada civilització

Cada civilització usa un model Ollama diferent per:
- Decisions diplomàtiques
- Generació d'esdeveniments històrics
- Cultura i art
- Demografia
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import random
from .ollama_client import get_ollama_client, OllamaClient


@dataclass
class CivilizationAIProfile:
    """
    Perfil IA d'una civilització amb model específic
    """
    civilization_name: str
    model_name: str  # Model d'Ollama assignat
    personality_bias: Dict[str, float]  # Biaixos de personalitat
    temperature: float = 0.8  # Temperatura per generació

    def to_dict(self) -> Dict:
        """Serialitza el perfil"""
        return {
            'civilization_name': self.civilization_name,
            'model_name': self.model_name,
            'personality_bias': self.personality_bias,
            'temperature': self.temperature
        }


class CivilizationAISystem:
    """
    Sistema que gestiona models IA per civilització

    Cada civilització té un model Ollama assignat que determina:
    - Estil de decisions diplomàtiques
    - Tipus d'esdeveniments culturals generats
    - Enfocament demogràfic
    - Personalitat única en interaccions
    """

    # Models d'Ollama disponibles (ordena per preferència)
    AVAILABLE_MODELS = [
        "llama3.2:3b",      # Model ràpid i eficient
        "llama3.2:1b",      # Model molt ràpid
        "qwen2.5:3b",       # Model alternatiu
        "phi3:3.8b",        # Model Microsoft
        "gemma2:2b",        # Model Google
        "mistral:7b",       # Model més gran si disponible
    ]

    def __init__(self):
        """Inicialitza el sistema"""
        self.ollama = get_ollama_client()
        self.profiles: Dict[str, CivilizationAIProfile] = {}
        self.available_models = self._detect_available_models()

    def _detect_available_models(self) -> List[str]:
        """
        Detecta models Ollama disponibles

        Returns:
            Llista de models disponibles (sempre retorna almenys els primers 3)
        """
        if not self.ollama or not self.ollama.available:
            # Retorna llista per defecte per fallback procedural
            return self.AVAILABLE_MODELS[:3]

        # Intenta obtenir llista de models (simplificat)
        # En producció faries una crida a l'API d'Ollama per llistar models
        available = []

        for model in self.AVAILABLE_MODELS:
            # Assumeix que si Ollama està disponible, almenys un model ho està
            available.append(model)

        # Si no trobem cap, retorna el per defecte
        if not available and self.ollama.model:
            available.append(self.ollama.model)

        return available if available else self.AVAILABLE_MODELS[:3]

    def assign_model_to_civilization(
        self,
        civilization_name: str,
        culture_traits: Dict,
        preferred_model: Optional[str] = None
    ) -> CivilizationAIProfile:
        """
        Assigna un model IA a una civilització

        Args:
            civilization_name: Nom de la civilització
            culture_traits: Trets culturals
            preferred_model: Model preferit (opcional)

        Returns:
            CivilizationAIProfile creat
        """
        # Si ja té model, retorna el mateix
        if civilization_name in self.profiles:
            return self.profiles[civilization_name]

        # Selecciona model
        if preferred_model and preferred_model in self.available_models:
            model = preferred_model
        else:
            # Assigna model diferent a cada civilització de forma rotatòria
            num_civs_assigned = len(self.profiles)
            model_index = num_civs_assigned % len(self.available_models)
            model = self.available_models[model_index]

        # Genera biaixos de personalitat basats en cultura
        personality_bias = self._generate_personality_bias(culture_traits, model)

        # Temperatura segons cultura
        # Cultures caòtiques → temperatura alta (més creativitat)
        # Cultures ordenades → temperatura baixa (més consistència)
        authoritarianism = culture_traits.get('authoritarianism', 50)
        temperature = 0.5 + (100 - authoritarianism) / 200.0  # 0.5-1.0

        # Crea perfil
        profile = CivilizationAIProfile(
            civilization_name=civilization_name,
            model_name=model,
            personality_bias=personality_bias,
            temperature=temperature
        )

        self.profiles[civilization_name] = profile

        return profile

    def _generate_personality_bias(
        self,
        culture_traits: Dict,
        model_name: str
    ) -> Dict[str, float]:
        """
        Genera biaixos de personalitat per al model

        Args:
            culture_traits: Trets culturals
            model_name: Nom del model

        Returns:
            Dict amb biaixos
        """
        # Biaixos basats en cultura
        bias = {
            'aggression': culture_traits.get('militarism', 50) / 100.0,
            'diplomacy': culture_traits.get('commerce', 50) / 100.0,
            'creativity': culture_traits.get('art', 50) / 100.0,
            'rationality': culture_traits.get('science', 50) / 100.0,
            'tradition': culture_traits.get('religion', 50) / 100.0,
        }

        # Ajusta segons model (cada model té "personalitat")
        if "llama" in model_name.lower():
            # Llama és més equilibrat
            pass
        elif "qwen" in model_name.lower():
            # Qwen és més analític
            bias['rationality'] += 0.1
            bias['creativity'] -= 0.05
        elif "phi" in model_name.lower():
            # Phi és més creatiu
            bias['creativity'] += 0.1
            bias['rationality'] -= 0.05
        elif "gemma" in model_name.lower():
            # Gemma és més diplomàtic
            bias['diplomacy'] += 0.1
            bias['aggression'] -= 0.05
        elif "mistral" in model_name.lower():
            # Mistral és més tradicional
            bias['tradition'] += 0.1

        # Normalitza a 0.0-1.0
        for key in bias:
            bias[key] = max(0.0, min(1.0, bias[key]))

        return bias

    def get_profile(self, civilization_name: str) -> Optional[CivilizationAIProfile]:
        """Obté perfil IA d'una civilització"""
        return self.profiles.get(civilization_name)

    def generate_with_civ_model(
        self,
        civilization_name: str,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Genera resposta JSON amb el model específic de la civilització

        Args:
            civilization_name: Nom de la civilització
            prompt: Prompt de generació
            system_prompt: Prompt de sistema (opcional)

        Returns:
            Dict amb resposta JSON o None
        """
        profile = self.get_profile(civilization_name)

        if not profile or not self.ollama or not self.ollama.available:
            return None

        # Crea client amb model específic
        civ_ollama = OllamaClient(
            host=self.ollama.host,
            model=profile.model_name,
            timeout=self.ollama.timeout
        )

        # Genera amb temperatura específica
        result = civ_ollama.generate_json(
            prompt=prompt,
            system=system_prompt,
            temperature=profile.temperature
        )

        return result

    def get_model_distribution(self) -> Dict[str, int]:
        """
        Obté distribució de models per civilitzacions

        Returns:
            Dict amb recompte per model
        """
        distribution = {}

        for profile in self.profiles.values():
            model = profile.model_name
            distribution[model] = distribution.get(model, 0) + 1

        return distribution

    def get_statistics(self) -> Dict:
        """Obté estadístiques del sistema"""
        return {
            'total_civilizations': len(self.profiles),
            'available_models': len(self.available_models),
            'models_list': self.available_models,
            'model_distribution': self.get_model_distribution(),
            'profiles': {name: profile.to_dict() for name, profile in self.profiles.items()}
        }
