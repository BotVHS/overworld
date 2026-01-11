"""
Species - Espècies animals i vegetals

Define espècies amb genomes i comportaments
"""
from typing import Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import random
import uuid
from .genome import Genome, ANIMAL_GENES, PLANT_GENES
from ..world.biome import BiomeType


class SpeciesType(Enum):
    """Tipus d'espècie"""
    ANIMAL = "animal"
    PLANT = "plant"
    MICROORGANISM = "microorganism"


class DietType(Enum):
    """Tipus de dieta per animals"""
    HERBIVORE = "herbivore"      # Només plantes
    CARNIVORE = "carnivore"      # Només carn
    OMNIVORE = "omnivore"        # Plantes i carn
    INSECTIVORE = "insectivore"  # Insectes


@dataclass
class Species:
    """
    Una espècie biològica

    Representa una espècie amb genoma base i característiques
    """
    id: str
    name: str
    species_type: SpeciesType
    base_genome: Genome

    # Preferències d'hàbitat
    preferred_biomes: List[BiomeType]
    min_temperature: float = 0.0  # 0-1
    max_temperature: float = 1.0
    min_humidity: float = 0.0
    max_humidity: float = 1.0

    # Atributs derivats del genoma
    base_population: int = 100  # Població inicial al món

    def is_habitable(self, biome: BiomeType, temperature: float, humidity: float) -> bool:
        """
        Comprova si aquesta espècie pot viure en un bioma

        Args:
            biome: Tipus de bioma
            temperature: Temperatura (0-1)
            humidity: Humitat (0-1)

        Returns:
            True si l'espècie pot viure aquí
        """
        # Comprova bioma
        if biome not in self.preferred_biomes:
            return False

        # Comprova temperatura
        if not (self.min_temperature <= temperature <= self.max_temperature):
            return False

        # Comprova humitat
        if not (self.min_humidity <= humidity <= self.max_humidity):
            return False

        return True

    def get_fitness(self, biome: BiomeType, temperature: float, humidity: float) -> float:
        """
        Calcula com de bé s'adapta l'espècie a un entorn

        Args:
            biome: Tipus de bioma
            temperature: Temperatura (0-1)
            humidity: Humitat (0-1)

        Returns:
            Fitness (0-1, 1 = òptim)
        """
        if not self.is_habitable(biome, temperature, humidity):
            return 0.0

        fitness = 1.0

        # Penalitza si no és el bioma preferit
        if biome != self.preferred_biomes[0]:
            fitness *= 0.7

        # Penalitza si la temperatura no és òptima
        temp_optimum = (self.min_temperature + self.max_temperature) / 2
        temp_distance = abs(temperature - temp_optimum)
        fitness *= (1.0 - temp_distance * 0.5)

        # Penalitza si la humitat no és òptima
        humidity_optimum = (self.min_humidity + self.max_humidity) / 2
        humidity_distance = abs(humidity - humidity_optimum)
        fitness *= (1.0 - humidity_distance * 0.5)

        return max(0.0, min(1.0, fitness))


class AnimalSpecies(Species):
    """Espècie animal amb comportament"""

    def __init__(
        self,
        name: str,
        base_genome: Optional[Genome] = None,
        preferred_biomes: Optional[List[BiomeType]] = None,
        diet: DietType = DietType.HERBIVORE,
        **kwargs
    ):
        if base_genome is None:
            base_genome = Genome.random(ANIMAL_GENES)

        if preferred_biomes is None:
            preferred_biomes = [BiomeType.GRASSLAND]

        super().__init__(
            id=str(uuid.uuid4()),
            name=name,
            species_type=SpeciesType.ANIMAL,
            base_genome=base_genome,
            preferred_biomes=preferred_biomes,
            **kwargs
        )

        self.diet = diet

    def get_diet_type(self) -> DietType:
        """Determina el tipus de dieta segons el genoma"""
        carnivore_gene = self.base_genome.get_trait('carnivore', 0.5)

        if carnivore_gene > 0.7:
            return DietType.CARNIVORE
        elif carnivore_gene < 0.3:
            return DietType.HERBIVORE
        else:
            return DietType.OMNIVORE

    def get_daily_food_need(self) -> float:
        """Calcula quanta menjar necessita per dia"""
        size = self.base_genome.get_trait('size', 0.5)
        # Animals més grans necessiten més menjar
        return 10 + size * 40  # 10-50 unitats/dia


class PlantSpecies(Species):
    """Espècie vegetal"""

    def __init__(
        self,
        name: str,
        base_genome: Optional[Genome] = None,
        preferred_biomes: Optional[List[BiomeType]] = None,
        **kwargs
    ):
        if base_genome is None:
            base_genome = Genome.random(PLANT_GENES)

        if preferred_biomes is None:
            preferred_biomes = [BiomeType.GRASSLAND]

        super().__init__(
            id=str(uuid.uuid4()),
            name=name,
            species_type=SpeciesType.PLANT,
            base_genome=base_genome,
            preferred_biomes=preferred_biomes,
            **kwargs
        )

    def get_growth_time(self) -> int:
        """Temps de creixement en dies"""
        growth_rate = self.base_genome.get_trait('growth_rate', 0.5)
        # Ràpid: 30 dies, Lent: 365 dies
        return int(30 + (1.0 - growth_rate) * 335)

    def get_seed_production(self) -> int:
        """Nombre de llavors produïdes per cicle"""
        seed_gene = self.base_genome.get_trait('seed_production', 0.5)
        return int(10 + seed_gene * 490)  # 10-500 llavors


# Factory per crear espècies predefinides
class SpeciesFactory:
    """Fàbrica per crear espècies comunes"""

    @staticmethod
    def create_deer() -> AnimalSpecies:
        """Crea una espècie de cérvol"""
        genome = Genome()
        genome.set_gene('size', 0.6, 0.7)           # Mida mitjana-gran
        genome.set_gene('speed', 0.7, 0.8)          # Ràpid
        genome.set_gene('strength', 0.4, 0.5)       # Força moderada
        genome.set_gene('intelligence', 0.5, 0.6)   # Intel·ligent
        genome.set_gene('aggression', 0.2, 0.3)     # Poc agressiu
        genome.set_gene('sociability', 0.7, 0.8)    # Social (viu en ramats)
        genome.set_gene('carnivore', 0.0, 0.1)      # Herbívor

        return AnimalSpecies(
            name="Cérvol",
            base_genome=genome,
            preferred_biomes=[BiomeType.TEMPERATE_FOREST, BiomeType.GRASSLAND],
            diet=DietType.HERBIVORE,
            min_temperature=0.3,
            max_temperature=0.7,
            min_humidity=0.4,
            max_humidity=0.9,
            base_population=150
        )

    @staticmethod
    def create_wolf() -> AnimalSpecies:
        """Crea una espècie de llop"""
        genome = Genome()
        genome.set_gene('size', 0.5, 0.6)
        genome.set_gene('speed', 0.8, 0.9)
        genome.set_gene('strength', 0.7, 0.8)
        genome.set_gene('intelligence', 0.7, 0.8)
        genome.set_gene('aggression', 0.7, 0.8)
        genome.set_gene('sociability', 0.8, 0.9)    # Molt social (caces en grup)
        genome.set_gene('carnivore', 0.9, 1.0)      # Carnívor

        return AnimalSpecies(
            name="Llop",
            base_genome=genome,
            preferred_biomes=[BiomeType.TAIGA, BiomeType.TEMPERATE_FOREST],
            diet=DietType.CARNIVORE,
            min_temperature=0.2,
            max_temperature=0.6,
            base_population=50
        )

    @staticmethod
    def create_rabbit() -> AnimalSpecies:
        """Crea una espècie de conill"""
        genome = Genome()
        genome.set_gene('size', 0.2, 0.3)           # Petit
        genome.set_gene('speed', 0.6, 0.7)
        genome.set_gene('fertility', 0.9, 1.0)      # Molt fèrtil
        genome.set_gene('aggression', 0.1, 0.2)     # No agressiu
        genome.set_gene('sociability', 0.6, 0.7)
        genome.set_gene('carnivore', 0.0, 0.0)      # Herbívor

        return AnimalSpecies(
            name="Conill",
            base_genome=genome,
            preferred_biomes=[BiomeType.GRASSLAND, BiomeType.SHRUBLAND],
            diet=DietType.HERBIVORE,
            min_temperature=0.3,
            max_temperature=0.8,
            base_population=300
        )

    @staticmethod
    def create_oak_tree() -> PlantSpecies:
        """Crea una espècie de roure"""
        genome = Genome()
        genome.set_gene('height', 0.8, 0.9)         # Alt
        genome.set_gene('growth_rate', 0.2, 0.3)    # Creixement lent
        genome.set_gene('seed_production', 0.6, 0.7)
        genome.set_gene('root_depth', 0.7, 0.8)     # Arrels profundes
        genome.set_gene('cold_resistance', 0.6, 0.7)

        return PlantSpecies(
            name="Roure",
            base_genome=genome,
            preferred_biomes=[BiomeType.TEMPERATE_FOREST],
            min_temperature=0.3,
            max_temperature=0.7,
            min_humidity=0.5,
            max_humidity=0.9,
            base_population=500
        )

    @staticmethod
    def create_grass() -> PlantSpecies:
        """Crea una espècie d'herba"""
        genome = Genome()
        genome.set_gene('height', 0.1, 0.2)         # Baixa
        genome.set_gene('growth_rate', 0.8, 0.9)    # Creixement ràpid
        genome.set_gene('seed_production', 0.9, 1.0) # Moltes llavors
        genome.set_gene('drought_resistance', 0.6, 0.7)

        return PlantSpecies(
            name="Herba",
            base_genome=genome,
            preferred_biomes=[BiomeType.GRASSLAND, BiomeType.SAVANNA],
            min_temperature=0.3,
            max_temperature=0.9,
            min_humidity=0.3,
            max_humidity=0.9,
            base_population=2000
        )

    @staticmethod
    def create_cactus() -> PlantSpecies:
        """Crea una espècie de cactus"""
        genome = Genome()
        genome.set_gene('height', 0.4, 0.5)
        genome.set_gene('growth_rate', 0.1, 0.2)    # Molt lent
        genome.set_gene('drought_resistance', 0.9, 1.0)  # Molt resistent
        genome.set_gene('cold_resistance', 0.3, 0.4)     # Poc resistent al fred

        return PlantSpecies(
            name="Cactus",
            base_genome=genome,
            preferred_biomes=[BiomeType.DESERT_HOT],
            min_temperature=0.6,
            max_temperature=1.0,
            min_humidity=0.0,
            max_humidity=0.3,
            base_population=300
        )
