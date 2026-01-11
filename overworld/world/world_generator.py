"""
Generador procedural de mons
"""
import numpy as np
from typing import Optional, List
from ..utils.noise_utils import NoiseGenerator, apply_redistribution_curve
from .tile import Tile
from .biome import BiomeClassifier, BiomeType, BIOME_DEFINITIONS


class WorldGenerator:
    """Genera un món procedural complet"""

    def __init__(self, width: int, height: int, seed: Optional[int] = None):
        """
        Args:
            width: Amplada del mapa
            height: Alçada del mapa
            seed: Llavor per generació determinista
        """
        self.width = width
        self.height = height
        self.seed = seed

        self.noise_gen = NoiseGenerator(seed)

        # Mapes generats
        self.altitude_map: Optional[np.ndarray] = None
        self.humidity_map: Optional[np.ndarray] = None
        self.temperature_map: Optional[np.ndarray] = None

        # Grid de tiles
        self.tiles: List[List[Tile]] = []

    def generate_altitude(
        self,
        scale: float = 150.0,
        octaves: int = 6,
        island_mode: bool = False
    ) -> np.ndarray:
        """
        Genera el mapa d'altitud

        Args:
            scale: Escala del noise (més gran = més suau)
            octaves: Detall del noise
            island_mode: Si True, genera un mapa amb forma d'illa

        Returns:
            Mapa d'altitud normalitzat (0-1)
        """
        print(f"  Generant altitud (scale={scale}, octaves={octaves}, island={island_mode})...")

        if island_mode:
            altitude_map = self.noise_gen.generate_island(
                self.width,
                self.height,
                scale=scale,
                island_factor=1.5
            )
        else:
            altitude_map = self.noise_gen.generate_normalized(
                self.width,
                self.height,
                scale=scale,
                octaves=octaves
            )

        # Aplica corba per fer més dramàtiques les muntanyes
        altitude_map = apply_redistribution_curve(altitude_map, exponent=1.8)

        self.altitude_map = altitude_map
        return altitude_map

    def generate_humidity(
        self,
        scale: float = 200.0,
        octaves: int = 4
    ) -> np.ndarray:
        """
        Genera el mapa d'humitat

        Factors:
        - Noise base
        - Proximitat a aigua (afegit després)
        - Altitud (muntanyes altes són més seques)

        Returns:
            Mapa d'humitat normalitzat (0-1)
        """
        print(f"  Generant humitat (scale={scale}, octaves={octaves})...")

        # Noise base per humitat
        humidity_map = self.noise_gen.generate_normalized(
            self.width,
            self.height,
            scale=scale,
            octaves=octaves,
            offset_x=1000  # Offset per no correlacionar amb altitud
        )

        # Modificació per altitud (muntanyes més seques)
        if self.altitude_map is not None:
            for y in range(self.height):
                for x in range(self.width):
                    altitude = self.altitude_map[y][x]

                    # Muntanyes altes (>0.7) redueixen humitat
                    if altitude > 0.7:
                        humidity_map[y][x] *= (1.0 - (altitude - 0.7) * 1.5)

                    # Aigua (oceà) té màxima humitat
                    if altitude < 0.35:
                        humidity_map[y][x] = 1.0

        # Normalitza
        humidity_map = np.clip(humidity_map, 0, 1)

        self.humidity_map = humidity_map
        return humidity_map

    def generate_temperature(
        self,
        scale: float = 300.0,
        octaves: int = 3,
        equator_temp: float = 0.9,
        pole_temp: float = 0.1
    ) -> np.ndarray:
        """
        Genera el mapa de temperatura

        Factors:
        - Latitud (equador càlid, pols freds)
        - Altitud (muntanyes més fredes)
        - Noise per variació local

        Args:
            equator_temp: Temperatura a l'equador (0-1)
            pole_temp: Temperatura als pols (0-1)

        Returns:
            Mapa de temperatura normalitzat (0-1)
        """
        print(f"  Generant temperatura (latitud {pole_temp}-{equator_temp})...")

        # Gradient latitudinal (equador al centre)
        temperature_map = np.zeros((self.height, self.width))

        for y in range(self.height):
            # Distància a l'equador (0 a l'equador, 1 als pols)
            distance_to_equator = abs(y - self.height / 2) / (self.height / 2)

            # Temperatura base segons latitud
            base_temp = pole_temp + (equator_temp - pole_temp) * (1 - distance_to_equator)

            temperature_map[y, :] = base_temp

        # Afegeix variació local amb noise
        noise_variation = self.noise_gen.generate_normalized(
            self.width,
            self.height,
            scale=scale,
            octaves=octaves,
            offset_x=2000
        )

        # Combina (80% latitud, 20% noise)
        temperature_map = temperature_map * 0.8 + noise_variation * 0.2

        # Modificació per altitud (muntanyes més fredes)
        if self.altitude_map is not None:
            for y in range(self.height):
                for x in range(self.width):
                    altitude = self.altitude_map[y][x]

                    # Cada 0.1 d'altitud per sobre de 0.5 redueix temperatura en 0.1
                    if altitude > 0.5:
                        temperature_map[y][x] -= (altitude - 0.5) * 0.4

        # Normalitza
        temperature_map = np.clip(temperature_map, 0, 1)

        self.temperature_map = temperature_map
        return temperature_map

    def generate_rivers(self, num_rivers: int = 10, min_length: int = 20):
        """
        Genera rius seguint gradients d'altitud

        Args:
            num_rivers: Nombre de rius a generar
            min_length: Longitud mínima d'un riu
        """
        print(f"  Generant {num_rivers} rius...")

        if self.altitude_map is None or not self.tiles:
            return

        rivers_created = 0

        for _ in range(num_rivers * 3):  # Intenta més vegades per aconseguir els desitjats
            if rivers_created >= num_rivers:
                break

            # Punt d'inici: zona alta (muntanya)
            start_x = np.random.randint(0, self.width)
            start_y = np.random.randint(0, self.height)

            if self.altitude_map[start_y][start_x] < 0.6:
                continue  # Només comença des de zones altes

            # Segueix el gradient cap avall
            river_path = []
            x, y = start_x, start_y
            visited = set()

            for step in range(500):  # Màxim 500 passos
                if (x, y) in visited:
                    break  # Bucle detectat

                visited.add((x, y))
                river_path.append((x, y))

                # Si arriba a l'oceà, para
                if self.tiles[y][x].is_water:
                    break

                # Busca el veí amb menor altitud
                neighbors = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if (nx, ny) not in visited:
                            neighbors.append((nx, ny, self.altitude_map[ny][nx]))

                if not neighbors:
                    break

                # Tria el veí amb menor altitud
                next_x, next_y, _ = min(neighbors, key=lambda n: n[2])
                x, y = next_x, next_y

            # Marca el riu als tiles si és prou llarg
            if len(river_path) >= min_length:
                for rx, ry in river_path:
                    if not self.tiles[ry][rx].is_water:
                        self.tiles[ry][rx].is_river = True
                        self.tiles[ry][rx].river_flow = 1.0
                        self.tiles[ry][rx].resources["water"] = 100.0
                rivers_created += 1

        print(f"    {rivers_created} rius generats correctament")

    def create_tiles(self):
        """Crea el grid de tiles a partir dels mapes generats"""
        print(f"  Creant grid de {self.width}x{self.height} tiles...")

        self.tiles = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = Tile(
                    x=x,
                    y=y,
                    altitude=self.altitude_map[y][x],
                    humidity=self.humidity_map[y][x],
                    temperature=self.temperature_map[y][x]
                )

                # Calcula índexs
                tile.calculate_hostility()
                tile.calculate_fertility()

                row.append(tile)
            self.tiles.append(row)

        print(f"    {self.width * self.height} tiles creats")

    def assign_biomes(self):
        """
        Assigna biomes a tots els tiles segons les seves condicions
        """
        print(f"  Assignant biomes...")

        biome_counts = {}

        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]

                # Classifica el bioma
                biome_type = BiomeClassifier.classify(
                    tile.altitude,
                    tile.temperature,
                    tile.humidity
                )

                tile.biome = biome_type

                # Compta biomes per estadístiques
                biome_counts[biome_type] = biome_counts.get(biome_type, 0) + 1

        # Mostra estadístiques
        print(f"    {len(biome_counts)} biomes diferents:")
        for biome_type, count in sorted(biome_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            biome_props = BIOME_DEFINITIONS[biome_type]
            pct = (count / (self.width * self.height)) * 100
            print(f"      - {biome_props.name}: {count} tiles ({pct:.1f}%)")

    def generate_resources(self):
        """
        Genera recursos naturals per cada tile segons el seu bioma
        """
        print(f"  Generant recursos naturals...")

        total_resources = {
            "gold": 0,
            "silver": 0,
            "iron": 0,
            "copper": 0,
            "uranium": 0,
            "coal": 0,
            "oil": 0,
            "gas": 0,
            "gems": 0,
        }

        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]

                if tile.biome is None:
                    continue

                biome_props = BIOME_DEFINITIONS[tile.biome]

                # Fusta
                tile.resources["wood"] = biome_props.wood_abundance * 100

                # Aigua (ja està assignada per rius i oceà)
                if tile.resources["water"] < biome_props.water_abundance * 100:
                    tile.resources["water"] = biome_props.water_abundance * 100

                # Fertilitat del sòl
                tile.resources["fertility"] = biome_props.fertility * 100

                # Minerals (probabilístics)
                if np.random.random() < biome_props.gold_chance:
                    amount = np.random.uniform(20, 100)
                    tile.resources["gold"] = amount
                    total_resources["gold"] += 1

                if np.random.random() < biome_props.silver_chance:
                    amount = np.random.uniform(30, 100)
                    tile.resources["silver"] = amount
                    total_resources["silver"] += 1

                if np.random.random() < biome_props.iron_chance:
                    amount = np.random.uniform(40, 100)
                    tile.resources["iron"] = amount
                    total_resources["iron"] += 1

                if np.random.random() < biome_props.copper_chance:
                    amount = np.random.uniform(40, 100)
                    tile.resources["copper"] = amount
                    total_resources["copper"] += 1

                if np.random.random() < biome_props.uranium_chance:
                    amount = np.random.uniform(10, 60)
                    tile.resources["uranium"] = amount
                    total_resources["uranium"] += 1

                if np.random.random() < biome_props.coal_chance:
                    amount = np.random.uniform(50, 100)
                    tile.resources["coal"] = amount
                    total_resources["coal"] += 1

                if np.random.random() < biome_props.oil_chance:
                    amount = np.random.uniform(30, 100)
                    tile.resources["oil"] = amount
                    total_resources["oil"] += 1

                if np.random.random() < biome_props.gas_chance:
                    amount = np.random.uniform(30, 100)
                    tile.resources["gas"] = amount
                    total_resources["gas"] += 1

                if np.random.random() < biome_props.gems_chance:
                    amount = np.random.uniform(10, 80)
                    tile.resources["gems"] = amount
                    total_resources["gems"] += 1

        # Estadístiques de recursos
        print(f"    Recursos generats:")
        for resource, count in total_resources.items():
            if count > 0:
                print(f"      - {resource.capitalize()}: {count} dipòsits")

    def generate_full_world(
        self,
        island_mode: bool = False,
        num_rivers: int = 15
    ) -> List[List[Tile]]:
        """
        Genera un món complet amb tots els sistemes

        Args:
            island_mode: Si genera un mapa tipus illa
            num_rivers: Nombre de rius a generar

        Returns:
            Grid de tiles generat
        """
        print(f"Generant món {self.width}x{self.height} (seed={self.seed})...")

        # Genera mapes base
        self.generate_altitude(island_mode=island_mode)
        self.generate_humidity()
        self.generate_temperature()

        # Crea tiles
        self.create_tiles()

        # Genera rius
        self.generate_rivers(num_rivers=num_rivers)

        # Assigna biomes
        self.assign_biomes()

        # Genera recursos
        self.generate_resources()

        print("Món generat correctament!")
        print(f"  Estadístiques globals:")

        # Calcula estadístiques
        water_tiles = sum(1 for row in self.tiles for t in row if t.is_water)
        river_tiles = sum(1 for row in self.tiles for t in row if t.is_river)
        high_fertility = sum(1 for row in self.tiles for t in row if t.fertility_index > 7)

        water_pct = (water_tiles / (self.width * self.height)) * 100
        print(f"    Aigua: {water_tiles} tiles ({water_pct:.1f}%)")
        print(f"    Rius: {river_tiles} tiles")
        print(f"    Terra fèrtil (>7): {high_fertility} tiles")

        return self.tiles
