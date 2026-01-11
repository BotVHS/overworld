"""
Biome - Sistema de biomes del món

Defineix tots els biomes possibles i les seves característiques
"""
from enum import Enum
from typing import Dict, Tuple
from dataclasses import dataclass


class BiomeType(Enum):
    """Tipus de biomes disponibles"""
    # Aquàtics
    OCEAN_DEEP = "ocean_deep"
    OCEAN_SHALLOW = "ocean_shallow"
    COASTAL = "coastal"

    # Glacials
    GLACIER = "glacier"
    TUNDRA = "tundra"
    TAIGA = "taiga"

    # Temperats
    GRASSLAND = "grassland"
    TEMPERATE_FOREST = "temperate_forest"
    TEMPERATE_RAINFOREST = "temperate_rainforest"

    # Càlids i secs
    DESERT_HOT = "desert_hot"
    DESERT_COLD = "desert_cold"
    SAVANNA = "savanna"

    # Tropicals
    TROPICAL_RAINFOREST = "tropical_rainforest"
    TROPICAL_SEASONAL_FOREST = "tropical_seasonal_forest"
    JUNGLE = "jungle"

    # Muntanya
    MOUNTAIN_LOW = "mountain_low"
    MOUNTAIN_HIGH = "mountain_high"
    MOUNTAIN_PEAK = "mountain_peak"

    # Especials
    SWAMP = "swamp"
    MANGROVE = "mangrove"
    SHRUBLAND = "shrubland"
    STEPPE = "steppe"


@dataclass
class BiomeProperties:
    """Propietats d'un bioma"""
    name: str
    description: str
    color: Tuple[int, int, int]  # RGB per rendering

    # Rangs de condicions per aquest bioma
    altitude_range: Tuple[float, float]  # (min, max) 0-1
    temperature_range: Tuple[float, float]  # (min, max) 0-1
    humidity_range: Tuple[float, float]  # (min, max) 0-1

    # Recursos típics (probabilitats 0-1)
    wood_abundance: float = 0.0
    water_abundance: float = 0.0
    fertility: float = 0.5

    # Recursos minerals (probabilitats 0-1)
    gold_chance: float = 0.01
    silver_chance: float = 0.02
    iron_chance: float = 0.05
    copper_chance: float = 0.05
    uranium_chance: float = 0.005
    coal_chance: float = 0.03
    oil_chance: float = 0.01
    gas_chance: float = 0.01
    gems_chance: float = 0.01

    # Característiques
    hostility: float = 0.5  # 0-1
    biodiversity: float = 0.5  # 0-1


# Definició de tots els biomes
BIOME_DEFINITIONS: Dict[BiomeType, BiomeProperties] = {
    # === AQUÀTICS ===
    BiomeType.OCEAN_DEEP: BiomeProperties(
        name="Oceà Profund",
        description="Aigües profundes lluny de la costa",
        color=(0, 50, 150),
        altitude_range=(0.0, 0.25),
        temperature_range=(0.0, 1.0),
        humidity_range=(0.0, 1.0),
        water_abundance=1.0,
        fertility=0.1,
        hostility=0.4,
        biodiversity=0.6,
        oil_chance=0.05,  # Petroli submarí
        gas_chance=0.04,
    ),

    BiomeType.OCEAN_SHALLOW: BiomeProperties(
        name="Oceà Poc Profund",
        description="Aigües costaneres poc profundes",
        color=(50, 100, 200),
        altitude_range=(0.25, 0.35),
        temperature_range=(0.0, 1.0),
        humidity_range=(0.0, 1.0),
        water_abundance=1.0,
        fertility=0.3,
        hostility=0.2,
        biodiversity=0.8,
        oil_chance=0.03,
    ),

    BiomeType.COASTAL: BiomeProperties(
        name="Costa",
        description="Zona costanera amb platges i penya-segats",
        color=(194, 178, 128),
        altitude_range=(0.35, 0.42),
        temperature_range=(0.0, 1.0),
        humidity_range=(0.4, 1.0),
        water_abundance=0.8,
        fertility=0.6,
        hostility=0.2,
        biodiversity=0.7,
        iron_chance=0.03,
    ),

    # === GLACIALS ===
    BiomeType.GLACIER: BiomeProperties(
        name="Glacera",
        description="Gel etern i temperatures extremes",
        color=(240, 250, 255),
        altitude_range=(0.0, 1.0),
        temperature_range=(0.0, 0.15),
        humidity_range=(0.0, 1.0),
        water_abundance=0.9,  # Gel = aigua congelada
        fertility=0.0,
        hostility=0.95,
        biodiversity=0.05,
        uranium_chance=0.01,  # Minerals a l'Àrtic
    ),

    BiomeType.TUNDRA: BiomeProperties(
        name="Tundra",
        description="Planures fredes amb vegetació escassa",
        color=(180, 200, 180),
        altitude_range=(0.35, 0.65),
        temperature_range=(0.1, 0.25),
        humidity_range=(0.2, 0.7),
        water_abundance=0.5,
        fertility=0.2,
        hostility=0.75,
        biodiversity=0.2,
        wood_abundance=0.1,
        oil_chance=0.04,
        gas_chance=0.06,  # Gas natural a la tundra
    ),

    BiomeType.TAIGA: BiomeProperties(
        name="Taiga",
        description="Bosc de coníferes en clima fred",
        color=(60, 100, 60),
        altitude_range=(0.35, 0.70),
        temperature_range=(0.2, 0.40),
        humidity_range=(0.4, 0.8),
        water_abundance=0.6,
        fertility=0.4,
        hostility=0.5,
        biodiversity=0.5,
        wood_abundance=0.8,
        iron_chance=0.08,
        coal_chance=0.06,
    ),

    # === TEMPERATS ===
    BiomeType.GRASSLAND: BiomeProperties(
        name="Praderia",
        description="Planes d'herba amb clima temperat",
        color=(120, 180, 80),
        altitude_range=(0.35, 0.60),
        temperature_range=(0.4, 0.7),
        humidity_range=(0.3, 0.6),
        water_abundance=0.5,
        fertility=0.85,  # Excel·lent per agricultura
        hostility=0.2,
        biodiversity=0.6,
        wood_abundance=0.2,
        iron_chance=0.06,
        copper_chance=0.06,
    ),

    BiomeType.TEMPERATE_FOREST: BiomeProperties(
        name="Bosc Temperat",
        description="Bosc caducifoli amb clima moderat",
        color=(34, 139, 34),
        altitude_range=(0.35, 0.70),
        temperature_range=(0.4, 0.7),
        humidity_range=(0.5, 0.8),
        water_abundance=0.7,
        fertility=0.75,
        hostility=0.3,
        biodiversity=0.8,
        wood_abundance=0.9,
        iron_chance=0.05,
        coal_chance=0.08,
    ),

    BiomeType.TEMPERATE_RAINFOREST: BiomeProperties(
        name="Bosc Pluvial Temperat",
        description="Bosc dens amb pluges constants",
        color=(20, 100, 50),
        altitude_range=(0.35, 0.65),
        temperature_range=(0.45, 0.65),
        humidity_range=(0.8, 1.0),
        water_abundance=0.95,
        fertility=0.8,
        hostility=0.4,
        biodiversity=0.9,
        wood_abundance=0.95,
    ),

    # === CÀLIDS I SECS ===
    BiomeType.DESERT_HOT: BiomeProperties(
        name="Desert Càlid",
        description="Sorra i calor extrema",
        color=(237, 201, 175),
        altitude_range=(0.35, 0.65),
        temperature_range=(0.75, 1.0),
        humidity_range=(0.0, 0.2),
        water_abundance=0.1,
        fertility=0.1,
        hostility=0.85,
        biodiversity=0.2,
        gold_chance=0.03,
        uranium_chance=0.015,
        oil_chance=0.08,  # Petroli al desert
    ),

    BiomeType.DESERT_COLD: BiomeProperties(
        name="Desert Fred",
        description="Desert d'altitud amb temperatures baixes",
        color=(200, 180, 150),
        altitude_range=(0.50, 0.75),
        temperature_range=(0.2, 0.4),
        humidity_range=(0.0, 0.2),
        water_abundance=0.15,
        fertility=0.1,
        hostility=0.8,
        biodiversity=0.15,
        copper_chance=0.08,
    ),

    BiomeType.SAVANNA: BiomeProperties(
        name="Sabana",
        description="Praderia tropical amb arbres dispersos",
        color=(167, 157, 100),
        altitude_range=(0.35, 0.60),
        temperature_range=(0.65, 0.85),
        humidity_range=(0.3, 0.6),
        water_abundance=0.4,
        fertility=0.6,
        hostility=0.5,  # Depredadors!
        biodiversity=0.85,  # Molt rica en vida
        wood_abundance=0.4,
        iron_chance=0.05,
    ),

    # === TROPICALS ===
    BiomeType.TROPICAL_RAINFOREST: BiomeProperties(
        name="Selva Tropical",
        description="Bosc tropical dens i humit",
        color=(0, 128, 0),
        altitude_range=(0.35, 0.65),
        temperature_range=(0.75, 0.95),
        humidity_range=(0.8, 1.0),
        water_abundance=0.95,
        fertility=0.7,  # Paradoxalment, sòl pobre
        hostility=0.6,  # Malalties, animals perillosos
        biodiversity=0.99,  # Màxima biodiversitat
        wood_abundance=0.99,
        gems_chance=0.03,  # Esmeraldas, etc.
    ),

    BiomeType.TROPICAL_SEASONAL_FOREST: BiomeProperties(
        name="Bosc Tropical Estacional",
        description="Bosc tropical amb estació seca",
        color=(107, 142, 35),
        altitude_range=(0.35, 0.65),
        temperature_range=(0.70, 0.90),
        humidity_range=(0.5, 0.8),
        water_abundance=0.7,
        fertility=0.75,
        hostility=0.5,
        biodiversity=0.85,
        wood_abundance=0.85,
    ),

    BiomeType.JUNGLE: BiomeProperties(
        name="Jungla",
        description="Vegetació tropical extremadament densa",
        color=(0, 100, 0),
        altitude_range=(0.40, 0.60),
        temperature_range=(0.80, 1.0),
        humidity_range=(0.85, 1.0),
        water_abundance=0.98,
        fertility=0.65,
        hostility=0.75,  # Molt perillós
        biodiversity=0.95,
        wood_abundance=0.95,
        gold_chance=0.02,
    ),

    # === MUNTANYA ===
    BiomeType.MOUNTAIN_LOW: BiomeProperties(
        name="Muntanya Baixa",
        description="Pendent muntanyós amb vegetació",
        color=(139, 137, 137),
        altitude_range=(0.65, 0.75),
        temperature_range=(0.3, 0.7),
        humidity_range=(0.3, 0.8),
        water_abundance=0.5,
        fertility=0.4,
        hostility=0.6,
        biodiversity=0.5,
        wood_abundance=0.6,
        iron_chance=0.12,
        copper_chance=0.10,
        coal_chance=0.10,
    ),

    BiomeType.MOUNTAIN_HIGH: BiomeProperties(
        name="Muntanya Alta",
        description="Alta muntanya amb vegetació escassa",
        color=(105, 105, 105),
        altitude_range=(0.75, 0.85),
        temperature_range=(0.1, 0.5),
        humidity_range=(0.2, 0.7),
        water_abundance=0.4,
        fertility=0.2,
        hostility=0.75,
        biodiversity=0.3,
        wood_abundance=0.3,
        gold_chance=0.05,
        silver_chance=0.06,
        iron_chance=0.15,
        copper_chance=0.12,
        gems_chance=0.04,
    ),

    BiomeType.MOUNTAIN_PEAK: BiomeProperties(
        name="Pic Muntanyós",
        description="Cim nevat i rocós",
        color=(255, 250, 250),
        altitude_range=(0.85, 1.0),
        temperature_range=(0.0, 0.3),
        humidity_range=(0.0, 0.6),
        water_abundance=0.3,
        fertility=0.0,
        hostility=0.95,
        biodiversity=0.05,
        wood_abundance=0.0,
        gold_chance=0.08,
        silver_chance=0.10,
        uranium_chance=0.03,
        gems_chance=0.06,  # Pedres precioses a l'alta muntanya
    ),

    # === ESPECIALS ===
    BiomeType.SWAMP: BiomeProperties(
        name="Aiguamoll",
        description="Terra pantanosa i humida",
        color=(76, 83, 32),
        altitude_range=(0.35, 0.45),
        temperature_range=(0.5, 0.8),
        humidity_range=(0.85, 1.0),
        water_abundance=0.95,
        fertility=0.5,
        hostility=0.7,  # Malalties
        biodiversity=0.75,
        wood_abundance=0.5,
        coal_chance=0.15,  # Torba → carbó
        oil_chance=0.08,
    ),

    BiomeType.MANGROVE: BiomeProperties(
        name="Manglars",
        description="Bosc costaner tropical",
        color=(85, 107, 47),
        altitude_range=(0.35, 0.42),
        temperature_range=(0.7, 0.95),
        humidity_range=(0.85, 1.0),
        water_abundance=0.9,
        fertility=0.6,
        hostility=0.5,
        biodiversity=0.9,
        wood_abundance=0.7,
    ),

    BiomeType.SHRUBLAND: BiomeProperties(
        name="Matoll",
        description="Arbustos i vegetació baixa",
        color=(153, 153, 102),
        altitude_range=(0.40, 0.65),
        temperature_range=(0.5, 0.8),
        humidity_range=(0.25, 0.5),
        water_abundance=0.3,
        fertility=0.45,
        hostility=0.4,
        biodiversity=0.5,
        wood_abundance=0.3,
    ),

    BiomeType.STEPPE: BiomeProperties(
        name="Estepa",
        description="Praderia semiàrida",
        color=(140, 130, 90),
        altitude_range=(0.35, 0.65),
        temperature_range=(0.45, 0.75),
        humidity_range=(0.2, 0.4),
        water_abundance=0.3,
        fertility=0.55,
        hostility=0.4,
        biodiversity=0.5,
        wood_abundance=0.15,
        coal_chance=0.05,
    ),
}


class BiomeClassifier:
    """
    Classifica tiles en biomes segons les seves condicions
    """

    @staticmethod
    def classify(altitude: float, temperature: float, humidity: float) -> BiomeType:
        """
        Classifica un tile en un bioma segons les seves condicions

        Args:
            altitude: Altitud del tile (0-1)
            temperature: Temperatura (0-1)
            humidity: Humitat (0-1)

        Returns:
            BiomeType corresponent
        """
        # Prioritat 1: Aigua
        if altitude < 0.35:
            if altitude < 0.25:
                return BiomeType.OCEAN_DEEP
            else:
                return BiomeType.OCEAN_SHALLOW

        # Prioritat 2: Costa
        if 0.35 <= altitude < 0.42 and humidity > 0.7:
            if temperature > 0.7:
                return BiomeType.MANGROVE
            return BiomeType.COASTAL

        # Prioritat 3: Muntanyes (altitud alta)
        if altitude >= 0.85:
            return BiomeType.MOUNTAIN_PEAK
        elif altitude >= 0.75:
            return BiomeType.MOUNTAIN_HIGH
        elif altitude >= 0.65:
            return BiomeType.MOUNTAIN_LOW

        # Prioritat 4: Glacials (temperatura baixa)
        if temperature < 0.15:
            return BiomeType.GLACIER
        elif temperature < 0.25:
            return BiomeType.TUNDRA
        elif temperature < 0.40:
            return BiomeType.TAIGA

        # Prioritat 5: Deserts (humitat baixa)
        if humidity < 0.2:
            if temperature > 0.75:
                return BiomeType.DESERT_HOT
            elif temperature < 0.4:
                return BiomeType.DESERT_COLD
            else:
                return BiomeType.STEPPE

        # Prioritat 6: Biomes per temperatura i humitat

        # Tropicals (calor alta)
        if temperature > 0.75:
            if humidity > 0.85:
                if altitude > 0.45:
                    return BiomeType.JUNGLE
                return BiomeType.TROPICAL_RAINFOREST
            elif humidity > 0.5:
                return BiomeType.TROPICAL_SEASONAL_FOREST
            else:
                return BiomeType.SAVANNA

        # Temperats
        if 0.4 <= temperature <= 0.75:
            if humidity > 0.85:
                return BiomeType.SWAMP
            elif humidity > 0.8:
                return BiomeType.TEMPERATE_RAINFOREST
            elif humidity > 0.5:
                return BiomeType.TEMPERATE_FOREST
            elif humidity > 0.3:
                return BiomeType.GRASSLAND
            else:
                return BiomeType.SHRUBLAND

        # Default: Matoll
        return BiomeType.SHRUBLAND

    @staticmethod
    def get_properties(biome_type: BiomeType) -> BiomeProperties:
        """Obté les propietats d'un bioma"""
        return BIOME_DEFINITIONS[biome_type]
