"""
Classe Tile: representa una casella del mapa
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Tile:
    """Una casella del mapa amb totes les seves propietats"""

    # Coordenades
    x: int
    y: int

    # Propietats geogràfiques (0-1 normalitzat)
    altitude: float = 0.5  # 0 = oceà profund, 1 = muntanya alta
    humidity: float = 0.5  # 0 = desert sec, 1 = aiguamoll
    temperature: float = 0.5  # 0 = glacial, 1 = tropical

    # Bioma (assignat després segons altitud/humitat/temperatura)
    biome: Optional[str] = None

    # Recursos naturals (quantitat, 0-100)
    resources: Dict[str, float] = field(default_factory=lambda: {
        "minerals": 0.0,  # Minerals genèrics
        "gold": 0.0,
        "silver": 0.0,
        "iron": 0.0,
        "copper": 0.0,
        "uranium": 0.0,
        "wood": 0.0,
        "water": 0.0,
        "fertility": 0.0,  # Qualitat del sòl
        "oil": 0.0,
        "coal": 0.0,
        "gas": 0.0
    })

    # Propietats derivades
    is_water: bool = False  # Oceà, llac, riu
    is_river: bool = False  # Té un riu
    river_flow: float = 0.0  # Intensitat del flux del riu

    # Tectònica (afegit després)
    plate_id: Optional[int] = None  # ID de la placa tectònica
    is_plate_boundary: bool = False

    # Índexs calculats
    hostility: float = 0.0  # 0-10, segons clima extrem i depredadors
    fertility_index: float = 0.0  # 0-10, qualitat per agricultura

    # Propietats dinàmiques (canvien amb el temps)
    erosion_level: float = 0.0  # Nivell d'erosió acumulada
    vegetation_density: float = 0.0  # Densitat de vegetació (0-1)

    # Civilització (afegit després)
    owner_civ_id: Optional[int] = None  # ID de la civilització propietària
    population: int = 0  # Població en aquesta casella
    has_city: bool = False

    def __post_init__(self):
        """Inicialitza propietats derivades"""
        # Determina si és aigua basant-se en l'altitud
        self.update_water_status()

    def update_water_status(self, water_level: float = 0.35):
        """
        Actualitza si la casella és aigua

        Args:
            water_level: Nivell d'altitud per sota del qual és aigua
        """
        self.is_water = self.altitude < water_level

        if self.is_water:
            # Aigua té més "aigua" com a recurs
            self.resources["water"] = 100.0
            self.resources["wood"] = 0.0
        else:
            # Terra té aigua segons humitat
            self.resources["water"] = self.humidity * 50.0

    def calculate_hostility(self) -> float:
        """
        Calcula l'índex d'hostilitat de la casella

        Factors:
        - Temperatura extrema (massa fred o massa calor)
        - Altitud extrema (muntanyes altes)
        - Baixa humitat (deserts)
        - Aigua (no habitable directament)

        Returns:
            Valor entre 0 (paradís) i 10 (inhabititable)
        """
        hostility = 0.0

        # Aigua és hostil per viure (tret de ciutats portuàries)
        if self.is_water:
            hostility += 8.0
        else:
            # Temperatura extrema
            if self.temperature < 0.2:  # Molt fred
                hostility += (0.2 - self.temperature) * 20  # Fins a +4
            elif self.temperature > 0.8:  # Molt calor
                hostility += (self.temperature - 0.8) * 20  # Fins a +4

            # Altitud alta (muntanyes)
            if self.altitude > 0.7:
                hostility += (self.altitude - 0.7) * 10  # Fins a +3

            # Deserts (baixa humitat)
            if self.humidity < 0.3:
                hostility += (0.3 - self.humidity) * 10  # Fins a +3

        self.hostility = min(10.0, hostility)
        return self.hostility

    def calculate_fertility(self) -> float:
        """
        Calcula l'índex de fertilitat (aptitud per agricultura)

        Factors:
        - Humitat moderada-alta
        - Temperatura moderada
        - Altitud baixa-moderada
        - Aigua disponible

        Returns:
            Valor entre 0 (estèril) i 10 (terra excel·lent)
        """
        if self.is_water:
            self.fertility_index = 0.0
            return 0.0

        fertility = 0.0

        # Humitat òptima: 0.4-0.7
        if 0.4 <= self.humidity <= 0.7:
            fertility += 3.0
        elif 0.3 <= self.humidity <= 0.8:
            fertility += 2.0
        elif self.humidity > 0.2:
            fertility += 1.0

        # Temperatura òptima: 0.4-0.7
        if 0.4 <= self.temperature <= 0.7:
            fertility += 3.0
        elif 0.3 <= self.temperature <= 0.8:
            fertility += 2.0
        elif self.temperature > 0.2:
            fertility += 1.0

        # Altitud òptima: 0.35-0.6 (planes i turons baixos)
        if 0.35 <= self.altitude <= 0.6:
            fertility += 3.0
        elif 0.3 <= self.altitude <= 0.7:
            fertility += 1.5

        # Bonus per rius
        if self.is_river:
            fertility += 1.0

        self.fertility_index = min(10.0, fertility)
        self.resources["fertility"] = self.fertility_index * 10  # Escala a 0-100
        return self.fertility_index

    def to_dict(self) -> Dict[str, Any]:
        """Serialitza la casella a diccionari"""
        return {
            "x": self.x,
            "y": self.y,
            "altitude": self.altitude,
            "humidity": self.humidity,
            "temperature": self.temperature,
            "biome": self.biome,
            "resources": self.resources.copy(),
            "is_water": self.is_water,
            "is_river": self.is_river,
            "hostility": self.hostility,
            "fertility_index": self.fertility_index
        }

    def __repr__(self) -> str:
        return f"Tile({self.x},{self.y} | {self.biome or 'Unknown'} | H:{self.hostility:.1f} F:{self.fertility_index:.1f})"
