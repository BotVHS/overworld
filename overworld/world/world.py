"""
Classe World: contenidor principal del món simulat
"""
from typing import List, Optional, Tuple
from .tile import Tile
from .world_generator import WorldGenerator


class World:
    """Representa el món sencer amb tots els seus sistemes"""

    def __init__(
        self,
        width: int = 500,
        height: int = 500,
        seed: Optional[int] = None
    ):
        """
        Args:
            width: Amplada del mapa
            height: Alçada del mapa
            seed: Llavor per generació determinista
        """
        self.width = width
        self.height = height
        self.seed = seed

        # Grid de tiles
        self.tiles: List[List[Tile]] = []

        # Generador
        self.generator: Optional[WorldGenerator] = None

    def generate(self, island_mode: bool = False, num_rivers: int = 15):
        """
        Genera el món proceduralment

        Args:
            island_mode: Si genera un mapa tipus illa
            num_rivers: Nombre de rius
        """
        self.generator = WorldGenerator(self.width, self.height, self.seed)
        self.tiles = self.generator.generate_full_world(
            island_mode=island_mode,
            num_rivers=num_rivers
        )

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        Obté un tile per coordenades

        Returns:
            Tile si les coordenades són vàlides, None altrament
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def get_neighbors(self, x: int, y: int, radius: int = 1) -> List[Tile]:
        """
        Obté els tiles veïns d'una posició

        Args:
            x, y: Coordenades del tile central
            radius: Radi de veïns (1 = 8 veïns immediats)

        Returns:
            Llista de tiles veïns
        """
        neighbors = []

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue

                tile = self.get_tile(x + dx, y + dy)
                if tile:
                    neighbors.append(tile)

        return neighbors

    def find_tiles_by_criteria(
        self,
        min_fertility: Optional[float] = None,
        max_hostility: Optional[float] = None,
        is_water: Optional[bool] = None,
        min_altitude: Optional[float] = None,
        max_altitude: Optional[float] = None
    ) -> List[Tile]:
        """
        Cerca tiles que compleixin certs criteris

        Returns:
            Llista de tiles que compleixen tots els criteris
        """
        results = []

        for row in self.tiles:
            for tile in row:
                # Comprova cada criteri
                if min_fertility is not None and tile.fertility_index < min_fertility:
                    continue
                if max_hostility is not None and tile.hostility > max_hostility:
                    continue
                if is_water is not None and tile.is_water != is_water:
                    continue
                if min_altitude is not None and tile.altitude < min_altitude:
                    continue
                if max_altitude is not None and tile.altitude > max_altitude:
                    continue

                results.append(tile)

        return results

    def get_statistics(self) -> dict:
        """
        Obté estadístiques del món

        Returns:
            Diccionari amb estadístiques diverses
        """
        total_tiles = self.width * self.height

        water_tiles = sum(1 for row in self.tiles for t in row if t.is_water)
        land_tiles = total_tiles - water_tiles
        river_tiles = sum(1 for row in self.tiles for t in row if t.is_river)

        fertile_land = sum(1 for row in self.tiles for t in row
                          if not t.is_water and t.fertility_index > 6)

        hostile_land = sum(1 for row in self.tiles for t in row
                          if not t.is_water and t.hostility > 7)

        avg_altitude = sum(t.altitude for row in self.tiles for t in row) / total_tiles
        avg_temp = sum(t.temperature for row in self.tiles for t in row) / total_tiles
        avg_humidity = sum(t.humidity for row in self.tiles for t in row) / total_tiles

        return {
            "total_tiles": total_tiles,
            "water_tiles": water_tiles,
            "land_tiles": land_tiles,
            "river_tiles": river_tiles,
            "water_percentage": (water_tiles / total_tiles) * 100,
            "fertile_land": fertile_land,
            "fertile_percentage": (fertile_land / land_tiles) * 100 if land_tiles > 0 else 0,
            "hostile_land": hostile_land,
            "hostile_percentage": (hostile_land / land_tiles) * 100 if land_tiles > 0 else 0,
            "avg_altitude": avg_altitude,
            "avg_temperature": avg_temp,
            "avg_humidity": avg_humidity
        }

    def __repr__(self) -> str:
        stats = self.get_statistics()
        return (
            f"World({self.width}x{self.height}, "
            f"water={stats['water_percentage']:.1f}%, "
            f"fertile={stats['fertile_percentage']:.1f}%)"
        )
