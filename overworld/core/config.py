"""
Configuració global del simulador
"""
from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class WorldConfig:
    """Configuració del món"""
    # Mida del mapa
    width: int = 500
    height: int = 500

    # Generació procedural
    seed: int = None  # None = aleatori

    # Biomes
    num_biomes: int = 15

    # Tectònica
    num_plates: int = 8  # Entre 5-12
    plate_speed: float = 0.05  # cm/any (simulat)

    # Temps
    days_per_year: int = 365
    seasons: int = 4


@dataclass
class SimulationConfig:
    """Configuració de la simulació"""
    # Velocitat
    initial_speed: int = 1  # 1x
    max_speed: int = 10000  # 10000x

    # Tick (1 tick = 1 dia)
    tick_duration: float = 0.016  # segons en temps real (per defecte)

    # Autosave
    autosave_enabled: bool = True
    autosave_interval: int = 365  # dies simulats


@dataclass
class GraphicsConfig:
    """Configuració gràfica"""
    # Finestra
    window_width: int = 1280
    window_height: int = 720
    fullscreen: bool = False

    # Rendering
    tile_size: int = 2  # píxels per tile
    fps_target: int = 60

    # Capes visuals
    default_layer: str = "biomes"


@dataclass
class OllamaConfig:
    """Configuració d'Ollama"""
    enabled: bool = True
    host: str = "http://localhost:11434"
    model: str = "llama3.2:3b"  # o "llama3.1:8b"
    timeout: int = 30  # segons

    # Optimització
    cache_enabled: bool = True
    batch_decisions: bool = True


@dataclass
class GameConfig:
    """Configuració completa del joc"""
    world: WorldConfig = field(default_factory=WorldConfig)
    simulation: SimulationConfig = field(default_factory=SimulationConfig)
    graphics: GraphicsConfig = field(default_factory=GraphicsConfig)
    ollama: OllamaConfig = field(default_factory=OllamaConfig)

    def to_dict(self) -> Dict[str, Any]:
        """Converteix la configuració a diccionari"""
        return {
            "world": self.world.__dict__,
            "simulation": self.simulation.__dict__,
            "graphics": self.graphics.__dict__,
            "ollama": self.ollama.__dict__
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameConfig':
        """Crea una configuració des d'un diccionari"""
        return cls(
            world=WorldConfig(**data.get("world", {})),
            simulation=SimulationConfig(**data.get("simulation", {})),
            graphics=GraphicsConfig(**data.get("graphics", {})),
            ollama=OllamaConfig(**data.get("ollama", {}))
        )


# Configuració per defecte
DEFAULT_CONFIG = GameConfig()
