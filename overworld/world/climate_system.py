"""
Climate System - Sistema climàtic avançat

Simula cicle de l'aigua, vents, estacions i patrons meteorològics
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import random
import math


class Season(Enum):
    """Estacions de l'any"""
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"


class WindDirection(Enum):
    """Direccions del vent"""
    NORTH = "north"
    NORTHEAST = "northeast"
    EAST = "east"
    SOUTHEAST = "southeast"
    SOUTH = "south"
    SOUTHWEST = "southwest"
    WEST = "west"
    NORTHWEST = "northwest"


@dataclass
class AtmosphericCell:
    """
    Cel·la atmosfèrica (Hadley, Ferrel, Polar)
    """
    cell_type: str  # hadley, ferrel, polar
    latitude_min: float
    latitude_max: float
    rotation_direction: int  # 1 = horari, -1 = antihorari


@dataclass
class WeatherPattern:
    """
    Patró meteorològic en un tile
    """
    x: int
    y: int
    temperature: float  # °C
    precipitation: float  # mm/mes
    wind_speed: float  # km/h
    wind_direction: WindDirection
    cloud_cover: float  # 0.0-1.0
    humidity: float  # 0.0-1.0


@dataclass
class WaterCycle:
    """
    Dades del cicle de l'aigua per un tile
    """
    evaporation: float = 0.0  # mm/mes
    condensation: float = 0.0  # mm/mes
    precipitation: float = 0.0  # mm/mes
    runoff: float = 0.0  # mm/mes
    infiltration: float = 0.0  # mm/mes


class ClimateSystem:
    """
    Sistema climàtic avançat amb cicle de l'aigua i vents
    """

    def __init__(self, world_width: int, world_height: int):
        """
        Args:
            world_width: Amplada del món
            world_height: Alçada del món
        """
        self.world_width = world_width
        self.world_height = world_height
        self.current_season = Season.SPRING
        self.current_month = 3  # Març
        self.atmospheric_cells: List[AtmosphericCell] = []
        self.weather_patterns: Dict[Tuple[int, int], WeatherPattern] = {}
        self.water_cycles: Dict[Tuple[int, int], WaterCycle] = {}

        self._initialize_atmospheric_cells()

    def _initialize_atmospheric_cells(self):
        """Inicialitza cel·les atmosfèriques (Hadley, Ferrel, Polar)"""
        # Hemisferi nord
        self.atmospheric_cells = [
            # Polar nord (60°-90°)
            AtmosphericCell("polar", 0.67, 1.0, 1),
            # Ferrel nord (30°-60°)
            AtmosphericCell("ferrel", 0.33, 0.67, -1),
            # Hadley nord (0°-30°)
            AtmosphericCell("hadley", 0.0, 0.33, 1),
        ]

    def advance_season(self):
        """Avança a la següent estació"""
        self.current_month = (self.current_month % 12) + 1

        # Determina estació segons mes
        if self.current_month in [3, 4, 5]:
            self.current_season = Season.SPRING
        elif self.current_month in [6, 7, 8]:
            self.current_season = Season.SUMMER
        elif self.current_month in [9, 10, 11]:
            self.current_season = Season.AUTUMN
        else:
            self.current_season = Season.WINTER

    def calculate_weather_patterns(
        self,
        world_tiles: Dict[Tuple[int, int], any]
    ) -> Dict[Tuple[int, int], WeatherPattern]:
        """
        Calcula patrons meteorològics per tots els tiles

        Args:
            world_tiles: Tiles del món amb altitud, temperatura, humitat

        Returns:
            Dict de patrons meteorològics per posició
        """
        patterns = {}

        for (x, y), tile in world_tiles.items():
            # Temperatura base (segons latitud i estació)
            latitude = y / self.world_height  # 0.0 (equador) a 1.0 (pol)
            base_temp = self._calculate_temperature(latitude, tile.altitude)

            # Ajusta temperatura segons estació
            seasonal_temp = self._adjust_for_season(base_temp, latitude)

            # Precipitació segons humitat i temperatura
            precipitation = self._calculate_precipitation(
                tile.humidity,
                seasonal_temp,
                tile.altitude,
                tile.is_water
            )

            # Vent segons cel·la atmosfèrica i altitud
            wind_speed, wind_direction = self._calculate_wind(latitude, tile.altitude)

            # Coberta de núvols segons humitat i precipitació
            cloud_cover = min(1.0, tile.humidity * 0.7 + precipitation / 200.0)

            pattern = WeatherPattern(
                x=x,
                y=y,
                temperature=seasonal_temp,
                precipitation=precipitation,
                wind_speed=wind_speed,
                wind_direction=wind_direction,
                cloud_cover=cloud_cover,
                humidity=tile.humidity
            )

            patterns[(x, y)] = pattern
            self.weather_patterns[(x, y)] = pattern

        return patterns

    def _calculate_temperature(self, latitude: float, altitude: float) -> float:
        """
        Calcula temperatura base

        Args:
            latitude: Latitud normalitzada (0.0-1.0)
            altitude: Altitud normalitzada (0.0-1.0)

        Returns:
            Temperatura en °C
        """
        # Temperatura base segons latitud (més fred als pols)
        # Equador: 25-30°C, Pols: -40°C
        base_temp = 30.0 - (latitude * 70.0)

        # Ajusta segons altitud (-6.5°C per cada 1000m)
        # Assumim altitud 1.0 = 5000m
        altitude_adjustment = -(altitude * 5.0) * 6.5

        return base_temp + altitude_adjustment

    def _adjust_for_season(self, base_temp: float, latitude: float) -> float:
        """Ajusta temperatura segons estació"""
        # Variació estacional més gran a latituds mitjanes/altes
        seasonal_variation = latitude * 15.0  # Fins a 15°C de variació

        if self.current_season == Season.SUMMER:
            return base_temp + seasonal_variation
        elif self.current_season == Season.WINTER:
            return base_temp - seasonal_variation
        elif self.current_season == Season.SPRING:
            return base_temp + seasonal_variation * 0.3
        else:  # AUTUMN
            return base_temp - seasonal_variation * 0.3

    def _calculate_precipitation(
        self,
        humidity: float,
        temperature: float,
        altitude: float,
        is_water: bool
    ) -> float:
        """
        Calcula precipitació mensual

        Args:
            humidity: Humitat (0.0-1.0)
            temperature: Temperatura (°C)
            altitude: Altitud (0.0-1.0)
            is_water: Si és aigua

        Returns:
            Precipitació en mm/mes
        """
        if is_water:
            return 50.0  # Aigua no rep precipitació directa

        # Base segons humitat
        base_precip = humidity * 200.0  # 0-200mm

        # Ajusta segons temperatura (més calor = més evaporació/precipitació)
        if temperature > 0:
            temp_factor = 1.0 + (temperature / 30.0) * 0.5
        else:
            temp_factor = 0.3  # Menys precipitació si fa molt fred

        # Ajusta segons altitud (muntanyes reben més precipitació)
        altitude_factor = 1.0 + altitude * 0.8

        precip = base_precip * temp_factor * altitude_factor

        # Variació estacional
        if self.current_season in [Season.SPRING, Season.AUTUMN]:
            precip *= 1.2  # Més pluja a primavera i tardor
        elif self.current_season == Season.WINTER:
            precip *= 0.8

        return max(0.0, min(500.0, precip))  # Limita 0-500mm

    def _calculate_wind(self, latitude: float, altitude: float) -> Tuple[float, WindDirection]:
        """
        Calcula vent segons cel·la atmosfèrica

        Args:
            latitude: Latitud (0.0-1.0)
            altitude: Altitud (0.0-1.0)

        Returns:
            Tuple (velocitat km/h, direcció)
        """
        # Determina cel·la atmosfèrica
        cell = None
        for c in self.atmospheric_cells:
            if c.latitude_min <= latitude < c.latitude_max:
                cell = c
                break

        if not cell:
            cell = self.atmospheric_cells[0]

        # Velocitat base segons cel·la
        if cell.cell_type == "hadley":
            base_speed = 20.0  # Alisis (vents moderats)
        elif cell.cell_type == "ferrel":
            base_speed = 30.0  # Vents de l'oest (més forts)
        else:  # polar
            base_speed = 25.0  # Vents polars (moderats-forts)

        # Ajusta segons altitud (més vent a l'altura)
        speed = base_speed * (1.0 + altitude * 0.5)

        # Direcció segons rotació de cel·la i latitud
        if cell.cell_type == "hadley":
            # Alisis (NE a l'hemisferi nord)
            direction = WindDirection.NORTHEAST if latitude < 0.17 else WindDirection.SOUTHWEST
        elif cell.cell_type == "ferrel":
            # Vents de l'oest
            direction = WindDirection.WEST
        else:  # polar
            # Vents de l'est
            direction = WindDirection.EAST

        return speed, direction

    def simulate_water_cycle(
        self,
        world_tiles: Dict[Tuple[int, int], any]
    ) -> Dict[Tuple[int, int], WaterCycle]:
        """
        Simula cicle de l'aigua per tots els tiles

        Args:
            world_tiles: Tiles del món

        Returns:
            Dict de cicles d'aigua per posició
        """
        cycles = {}

        for (x, y), tile in world_tiles.items():
            weather = self.weather_patterns.get((x, y))
            if not weather:
                continue

            cycle = WaterCycle()

            # 1. Evaporació (més en aigua i calor)
            if tile.is_water:
                # Aigua evapora més
                evap_rate = 150.0 if weather.temperature > 0 else 30.0
                cycle.evaporation = evap_rate * (1.0 + weather.temperature / 30.0)
            else:
                # Terra evapora segons humitat
                evap_rate = 50.0 if weather.temperature > 0 else 10.0
                cycle.evaporation = evap_rate * tile.humidity * (1.0 + weather.temperature / 40.0)

            # 2. Condensació (vapor → núvols)
            cycle.condensation = cycle.evaporation * weather.cloud_cover

            # 3. Precipitació (núvols → terra/aigua)
            cycle.precipitation = weather.precipitation

            # 4. Infiltració (aigua → terra)
            if not tile.is_water and cycle.precipitation > 0:
                # Part de la precipitació s'infiltra
                infiltration_rate = 0.6 if tile.altitude < 0.5 else 0.3  # Menys en muntanyes
                cycle.infiltration = cycle.precipitation * infiltration_rate
            else:
                cycle.infiltration = 0.0

            # 5. Escorrentia (aigua → rius/mar)
            if not tile.is_water:
                cycle.runoff = cycle.precipitation - cycle.infiltration
            else:
                cycle.runoff = 0.0

            cycles[(x, y)] = cycle
            self.water_cycles[(x, y)] = cycle

        return cycles

    def get_season_name(self) -> str:
        """Obté nom de l'estació actual"""
        names = {
            Season.SPRING: "Primavera",
            Season.SUMMER: "Estiu",
            Season.AUTUMN: "Tardor",
            Season.WINTER: "Hivern"
        }
        return names.get(self.current_season, "Desconegut")

    def get_climate_classification(self, x: int, y: int) -> str:
        """
        Obté classificació climàtica (Köppen simplificat)

        Args:
            x, y: Coordenades

        Returns:
            Tipus climàtic
        """
        weather = self.weather_patterns.get((x, y))
        if not weather:
            return "Desconegut"

        temp = weather.temperature
        precip = weather.precipitation

        # Classificació simplificada Köppen
        if temp < -3:
            # Climes freds
            if precip > 50:
                return "Subarctic" if temp > -10 else "Tundra"
            else:
                return "Polar"
        elif temp < 18:
            # Climes temperats
            if precip > 100:
                return "Oceanic" if precip > 150 else "Humid Continental"
            else:
                return "Mediterranean" if precip > 50 else "Steppe"
        else:
            # Climes càlids
            if precip > 150:
                return "Tropical Rainforest" if precip > 250 else "Tropical Monsoon"
            elif precip > 50:
                return "Tropical Savanna"
            else:
                return "Desert" if precip < 25 else "Arid"

    def get_statistics(self) -> Dict:
        """Obté estadístiques climàtiques"""
        if not self.weather_patterns:
            return {
                'current_season': self.get_season_name(),
                'current_month': self.current_month,
                'total_weather_patterns': 0
            }

        avg_temp = sum(w.temperature for w in self.weather_patterns.values()) / len(self.weather_patterns)
        avg_precip = sum(w.precipitation for w in self.weather_patterns.values()) / len(self.weather_patterns)
        avg_wind = sum(w.wind_speed for w in self.weather_patterns.values()) / len(self.weather_patterns)
        avg_cloud = sum(w.cloud_cover for w in self.weather_patterns.values()) / len(self.weather_patterns)

        # Distribució de climes
        climate_distribution = {}
        for (x, y) in self.weather_patterns.keys():
            climate = self.get_climate_classification(x, y)
            climate_distribution[climate] = climate_distribution.get(climate, 0) + 1

        # Cicle de l'aigua global
        total_evap = sum(c.evaporation for c in self.water_cycles.values())
        total_precip = sum(c.precipitation for c in self.water_cycles.values())
        total_runoff = sum(c.runoff for c in self.water_cycles.values())

        return {
            'current_season': self.get_season_name(),
            'current_month': self.current_month,
            'total_weather_patterns': len(self.weather_patterns),
            'average_temperature': avg_temp,
            'average_precipitation': avg_precip,
            'average_wind_speed': avg_wind,
            'average_cloud_cover': avg_cloud,
            'climate_distribution': climate_distribution,
            'water_cycle': {
                'total_evaporation': total_evap,
                'total_precipitation': total_precip,
                'total_runoff': total_runoff
            }
        }
