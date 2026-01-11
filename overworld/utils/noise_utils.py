"""
Utilitats per generació de noise procedural (Perlin/Simplex)
"""
from perlin_noise import PerlinNoise
import numpy as np
from typing import Optional


class NoiseGenerator:
    """Generador de noise 2D per mapes procedurals"""

    def __init__(self, seed: Optional[int] = None):
        """
        Args:
            seed: Llavor per generació determinista. Si és None, usa aleatori.
        """
        if seed is None:
            seed = np.random.randint(0, 1000000)
        self.seed = seed

    def generate_2d(
        self,
        width: int,
        height: int,
        scale: float = 100.0,
        octaves: int = 6,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
        offset_x: float = 0.0,
        offset_y: float = 0.0
    ) -> np.ndarray:
        """
        Genera un mapa 2D de noise de Perlin

        Args:
            width: Amplada del mapa
            height: Alçada del mapa
            scale: Escala del noise (més gran = més suau)
            octaves: Nombre d'octaves (més = més detall)
            persistence: Com de ràpid decreix l'amplitud de les octaves
            lacunarity: Com de ràpid augmenta la freqüència de les octaves
            offset_x: Desplaçament X (per variar el patró)
            offset_y: Desplaçament Y

        Returns:
            Array 2D de numpy amb valors entre -1 i 1
        """
        if scale <= 0:
            scale = 0.0001

        # Crea el generador de Perlin amb el seed i octaves
        perlin = PerlinNoise(octaves=octaves, seed=self.seed)

        noise_map = np.zeros((height, width))

        for y in range(height):
            for x in range(width):
                # Normalitza les coordenades
                nx = (x + offset_x) / scale
                ny = (y + offset_y) / scale

                # Genera noise de Perlin (retorna entre -0.5 i 0.5)
                noise_value = perlin([nx, ny])

                # Escala a [-1, 1]
                noise_value *= 2

                noise_map[y][x] = noise_value

        return noise_map

    def generate_normalized(
        self,
        width: int,
        height: int,
        scale: float = 100.0,
        octaves: int = 6,
        **kwargs
    ) -> np.ndarray:
        """
        Genera noise normalitzat entre 0 i 1

        Returns:
            Array 2D amb valors entre 0 i 1
        """
        noise_map = self.generate_2d(width, height, scale, octaves, **kwargs)

        # Normalitza a [0, 1]
        min_val = np.min(noise_map)
        max_val = np.max(noise_map)

        if max_val - min_val > 0:
            noise_map = (noise_map - min_val) / (max_val - min_val)
        else:
            noise_map = np.zeros_like(noise_map)

        return noise_map

    def generate_island(
        self,
        width: int,
        height: int,
        scale: float = 100.0,
        island_factor: float = 1.2
    ) -> np.ndarray:
        """
        Genera un mapa amb forma d'illa (elevat al centre, baix als extrems)

        Args:
            island_factor: Intensitat de l'efecte d'illa (1.0-2.0)

        Returns:
            Array 2D amb valors entre 0 i 1, amb forma d'illa
        """
        noise_map = self.generate_normalized(width, height, scale)

        # Crea una màscara circular/el·líptica
        center_x = width / 2
        center_y = height / 2

        for y in range(height):
            for x in range(width):
                # Distància al centre (normalitzada)
                dx = (x - center_x) / (width / 2)
                dy = (y - center_y) / (height / 2)
                distance = np.sqrt(dx * dx + dy * dy)

                # Gradient radial (1 al centre, 0 als extrems)
                gradient = max(0, 1 - distance ** island_factor)

                # Multiplica el noise pel gradient
                noise_map[y][x] *= gradient

        return noise_map


def apply_redistribution_curve(values: np.ndarray, exponent: float = 2.0) -> np.ndarray:
    """
    Aplica una corba de redistribució per accentuar valors alts o baixos

    Args:
        values: Array amb valors entre 0 i 1
        exponent:
            - > 1: accentua valors alts (més muntanyes)
            - < 1: accentua valors baixos (més planes)
            - = 2: corba quadràtica (valor per defecte)

    Returns:
        Array modificat amb la corba aplicada
    """
    return np.power(values, exponent)


def combine_noise_maps(
    maps: list[np.ndarray],
    weights: list[float]
) -> np.ndarray:
    """
    Combina múltiples mapes de noise amb pesos

    Args:
        maps: Llista d'arrays de noise
        weights: Llista de pesos (haurien de sumar 1.0)

    Returns:
        Mapa combinat
    """
    if len(maps) != len(weights):
        raise ValueError("El nombre de mapes ha de coincidir amb el nombre de pesos")

    if not maps:
        raise ValueError("Cal proporcionar almenys un mapa")

    result = np.zeros_like(maps[0])

    for noise_map, weight in zip(maps, weights):
        result += noise_map * weight

    # Normalitza per seguretat
    result = np.clip(result, 0, 1)

    return result
