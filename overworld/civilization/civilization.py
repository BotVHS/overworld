"""
Civilization - Civilitzacions intel·ligents

Representa civilitzacions amb cultura, ciutats i tecnologia
"""
from typing import Optional, List, Tuple
from dataclasses import dataclass, field
import uuid
import random
from .culture import CulturalTraits, CultureFactory, CulturalArchetype


@dataclass
class City:
    """Una ciutat dins d'una civilització"""
    name: str
    x: int
    y: int
    population: int = 100
    founded_year: int = 0

    def to_dict(self) -> dict:
        """Serialitza la ciutat"""
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'population': self.population,
            'founded_year': self.founded_year
        }


class TechLevel:
    """Nivells tecnològics"""
    STONE_AGE = 0      # Edat de pedra
    BRONZE_AGE = 1     # Edat del bronze
    IRON_AGE = 2       # Edat del ferro
    MEDIEVAL = 3       # Medieval
    GUNPOWDER = 4      # Pólvora
    INDUSTRIAL = 5     # Industrial
    ELECTRICAL = 6     # Elèctric
    INFORMATION = 7    # Informàtica
    BIOTECH = 8        # Biotecnologia


@dataclass
class Civilization:
    """
    Una civilització intel·ligent

    Representa una societat amb cultura, ciutats i tecnologia
    """
    id: str
    name: str
    color: Tuple[int, int, int]  # Color per renderització

    # Cultura
    culture: CulturalTraits

    # Ciutats i territori
    cities: List[City] = field(default_factory=list)
    capital: Optional[City] = None

    # Població
    total_population: int = 0

    # Tecnologia
    tech_level: int = TechLevel.STONE_AGE

    # Història
    founded_year: int = 0
    historical_events: List[str] = field(default_factory=list)

    # Estat
    is_extinct: bool = False

    def add_city(self, city: City):
        """Afegeix una ciutat"""
        self.cities.append(city)
        if self.capital is None:
            self.capital = city
        self.total_population += city.population

    def get_cultural_archetype(self) -> CulturalArchetype:
        """Obté l'arquetip cultural dominant"""
        return self.culture.get_archetype()

    def get_cultural_description(self) -> str:
        """Genera una descripció textual de la cultura"""
        archetype = self.get_cultural_archetype()

        descriptions = {
            CulturalArchetype.WARRIOR: "una cultura guerrera i espartana",
            CulturalArchetype.PEACEFUL: "una cultura pacífica i il·lustrada",
            CulturalArchetype.MARITIME: "una talassocràcia naval i exploradora",
            CulturalArchetype.JUNGLE: "una cultura xamànica de la jungla",
            CulturalArchetype.MOUNTAIN: "una cultura minera de muntanya",
            CulturalArchetype.DESERT: "una cultura del desert adaptada a la duresa",
            CulturalArchetype.NOMADIC: "una cultura nòmada de les estepes",
            CulturalArchetype.BALANCED: "una cultura equilibrada i adaptativa"
        }

        return descriptions.get(archetype, "una cultura única")

    def to_dict(self) -> dict:
        """Serialitza la civilització"""
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'culture': self.culture.to_dict(),
            'cities': [city.to_dict() for city in self.cities],
            'capital': self.capital.to_dict() if self.capital else None,
            'total_population': self.total_population,
            'tech_level': self.tech_level,
            'founded_year': self.founded_year,
            'historical_events': self.historical_events,
            'is_extinct': self.is_extinct
        }


class CivilizationManager:
    """
    Gestiona totes les civilitzacions del món

    Crea i distribueix civilitzacions pel mapa
    """

    def __init__(self, world):
        """
        Args:
            world: Món on col·locar les civilitzacions
        """
        self.world = world
        self.civilizations: List[Civilization] = []
        self.current_year = 0

    def spawn_civilization(
        self,
        x: int,
        y: int,
        name: Optional[str] = None
    ) -> Optional[Civilization]:
        """
        Crea una nova civilització en una ubicació

        Args:
            x, y: Coordenades del tile
            name: Nom de la civilització (generat si None)

        Returns:
            Civilització creada o None si la ubicació no és vàlida
        """
        tile = self.world.get_tile(x, y)

        # Comprova que no sigui aigua
        if tile.is_water:
            return None

        # Comprova que tingui fertilitat mínima
        if tile.fertility_index < 5:
            return None

        # Genera nom si no es proporciona
        if name is None:
            name = self._generate_civilization_name()

        # Genera cultura segons l'entorn
        from ..world.biome import BiomeType

        is_coastal = self._is_coastal(x, y)
        is_mountain = tile.altitude > 0.7
        is_desert = tile.biome in [BiomeType.DESERT_HOT, BiomeType.DESERT_COLD]
        is_jungle = tile.biome == BiomeType.JUNGLE

        culture = CultureFactory.create_from_environment(
            hostility=tile.hostility,
            fertility=tile.fertility_index,
            is_coastal=is_coastal,
            is_mountain=is_mountain,
            is_desert=is_desert,
            is_jungle=is_jungle,
            temperature=tile.temperature,
            humidity=tile.humidity
        )

        # Crea civilització
        civ = Civilization(
            id=str(uuid.uuid4()),
            name=name,
            color=self._generate_color(),
            culture=culture,
            founded_year=self.current_year
        )

        # Crea ciutat capital
        city_name = f"{name} Capital"
        capital = City(
            name=city_name,
            x=x,
            y=y,
            population=1000,
            founded_year=self.current_year
        )

        civ.add_city(capital)
        civ.historical_events.append(
            f"Any {self.current_year}: Fundació de {name} a ({x}, {y})"
        )

        self.civilizations.append(civ)

        return civ

    def _is_coastal(self, x: int, y: int) -> bool:
        """Comprova si un tile és costaner"""
        neighbors = self.world.get_neighbors(x, y, radius=1)
        for neighbor_tile in neighbors:
            if neighbor_tile.is_water:
                return True
        return False

    def _generate_civilization_name(self) -> str:
        """Genera un nom procedural per una civilització"""
        prefixes = [
            "Aen", "Kal", "Mor", "Zar", "Vel", "Thal", "Nor", "Syr",
            "Drak", "Elv", "Fey", "Gor", "Hal", "Ith", "Jar", "Khor"
        ]
        suffixes = [
            "dor", "mar", "thar", "dran", "quin", "ven", "kar", "lon",
            "rath", "sil", "tor", "var", "wyn", "xar", "yan", "zor"
        ]

        return random.choice(prefixes) + random.choice(suffixes)

    def _generate_color(self) -> Tuple[int, int, int]:
        """Genera un color aleatori per la civilització"""
        # Colors vius per visualització
        colors = [
            (255, 50, 50),    # Vermell
            (50, 50, 255),    # Blau
            (50, 255, 50),    # Verd
            (255, 255, 50),   # Groc
            (255, 50, 255),   # Magenta
            (50, 255, 255),   # Cian
            (255, 150, 50),   # Taronja
            (150, 50, 255),   # Porpra
            (50, 255, 150),   # Verd clar
            (255, 50, 150),   # Rosa
        ]
        return random.choice(colors)

    def spawn_multiple_civilizations(self, count: int = 5):
        """
        Crea múltiples civilitzacions distribuïdes pel món

        Args:
            count: Nombre de civilitzacions a crear
        """
        print(f"Creant {count} civilitzacions...")

        attempts = 0
        max_attempts = count * 50

        while len(self.civilizations) < count and attempts < max_attempts:
            # Tria ubicació aleatòria
            x = random.randint(0, self.world.width - 1)
            y = random.randint(0, self.world.height - 1)

            # Intenta crear civilització
            civ = self.spawn_civilization(x, y)

            if civ:
                print(f"  ✓ {civ.name} fundada a ({x}, {y})")
                print(f"    Cultura: {civ.get_cultural_description()}")
                print(f"    Arquetip: {civ.get_cultural_archetype().value}")
                archetype_str = civ.get_cultural_archetype().value
                print(f"    Valors: {', '.join(civ.culture.core_values)}")

            attempts += 1

        print(f"\nTotal civilitzacions creades: {len(self.civilizations)}")

    def get_statistics(self) -> dict:
        """Obté estadístiques globals de les civilitzacions"""
        total_pop = sum(civ.total_population for civ in self.civilizations)
        total_cities = sum(len(civ.cities) for civ in self.civilizations)

        # Arquetips culturals
        archetypes = {}
        for civ in self.civilizations:
            archetype = civ.get_cultural_archetype()
            archetypes[archetype.value] = archetypes.get(archetype.value, 0) + 1

        return {
            'total_civilizations': len(self.civilizations),
            'total_population': total_pop,
            'total_cities': total_cities,
            'archetypes': archetypes,
            'civilizations': [
                {
                    'name': civ.name,
                    'population': civ.total_population,
                    'cities': len(civ.cities),
                    'archetype': civ.get_cultural_archetype().value,
                    'tech_level': civ.tech_level
                }
                for civ in self.civilizations
            ]
        }


def create_civilizations(world, count: int = 5) -> CivilizationManager:
    """
    Crea un gestor de civilitzacions amb civilitzacions inicials

    Args:
        world: Món on crear les civilitzacions
        count: Nombre de civilitzacions a crear

    Returns:
        CivilizationManager amb civilitzacions creades
    """
    manager = CivilizationManager(world)
    manager.spawn_multiple_civilizations(count)
    return manager
