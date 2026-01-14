"""
Plate Tectonics - Sistema de tectònica de plaques

Simula moviment de plaques, formació de muntanyes, volcans i terratrèmols
"""
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import random
import math


class PlateType(Enum):
    """Tipus de placa tectònica"""
    OCEANIC = "oceanic"      # Placa oceànica (densa)
    CONTINENTAL = "continental"  # Placa continental (lleugera)


class BoundaryType(Enum):
    """Tipus de límit entre plaques"""
    DIVERGENT = "divergent"      # Plaques s'allunyen (rift, dorsal oceànica)
    CONVERGENT = "convergent"    # Plaques xoquen (subducció, muntanyes)
    TRANSFORM = "transform"      # Plaques es llisquen lateralment


@dataclass
class TectonicPlate:
    """
    Una placa tectònica
    """
    plate_id: int
    plate_type: PlateType
    tiles: Set[Tuple[int, int]] = field(default_factory=set)  # (x, y) tiles
    velocity_x: float = 0.0  # Velocitat en X (cm/any)
    velocity_y: float = 0.0  # Velocitat en Y (cm/any)
    age: int = 0  # Edat en milions d'anys

    def get_speed(self) -> float:
        """Obté velocitat total"""
        return math.sqrt(self.velocity_x**2 + self.velocity_y**2)

    def get_direction(self) -> float:
        """Obté direcció en radians"""
        return math.atan2(self.velocity_y, self.velocity_x)


@dataclass
class PlateBoundary:
    """
    Límit entre dues plaques
    """
    plate1_id: int
    plate2_id: int
    boundary_type: BoundaryType
    tiles: List[Tuple[int, int]] = field(default_factory=list)  # Tiles del límit
    activity_level: float = 0.5  # 0.0-1.0, activitat sísmica/volcànica


@dataclass
class GeologicalEvent:
    """
    Esdeveniment geològic (terratrèmol, volcà, etc.)
    """
    event_type: str  # earthquake, volcano, mountain_building
    x: int
    y: int
    year: int
    magnitude: float  # Magnitud (escala Richter per terratrèmols)
    description: str = ""


class PlateTectonicsSystem:
    """
    Sistema de tectònica de plaques
    """

    def __init__(self, world_width: int, world_height: int):
        """
        Args:
            world_width: Amplada del món
            world_height: Alçada del món
        """
        self.world_width = world_width
        self.world_height = world_height
        self.plates: Dict[int, TectonicPlate] = {}
        self.boundaries: List[PlateBoundary] = []
        self.geological_events: List[GeologicalEvent] = []
        self.plate_map: Dict[Tuple[int, int], int] = {}  # (x,y) -> plate_id

    def generate_plates(self, num_plates: int = 8) -> None:
        """
        Genera plaques tectòniques aleatòries

        Args:
            num_plates: Nombre de plaques a generar
        """
        print(f"Generant {num_plates} plaques tectòniques...")

        # Genera punts d'origen per cada placa (seeds)
        seeds = []
        for i in range(num_plates):
            x = random.randint(0, self.world_width - 1)
            y = random.randint(0, self.world_height - 1)
            seeds.append((x, y, i))

        # Creixement de plaques per Voronoi
        for x in range(self.world_width):
            for y in range(self.world_height):
                # Troba placa més propera
                min_dist = float('inf')
                closest_plate = 0

                for sx, sy, plate_id in seeds:
                    # Distància amb wrap-around
                    dx = min(abs(x - sx), self.world_width - abs(x - sx))
                    dy = min(abs(y - sy), self.world_height - abs(y - sy))
                    dist = math.sqrt(dx**2 + dy**2)

                    if dist < min_dist:
                        min_dist = dist
                        closest_plate = plate_id

                self.plate_map[(x, y)] = closest_plate

        # Crea objectes TectonicPlate
        for i in range(num_plates):
            # Tipus de placa (70% oceànica, 30% continental)
            plate_type = PlateType.OCEANIC if random.random() < 0.7 else PlateType.CONTINENTAL

            # Velocitat aleatòria (2-10 cm/any, típic de plaques reals)
            speed = random.uniform(2.0, 10.0)
            direction = random.uniform(0, 2 * math.pi)

            plate = TectonicPlate(
                plate_id=i,
                plate_type=plate_type,
                velocity_x=speed * math.cos(direction),
                velocity_y=speed * math.sin(direction),
                age=random.randint(50, 200)  # 50-200 milions d'anys
            )

            # Afegeix tiles a la placa
            for (x, y), pid in self.plate_map.items():
                if pid == i:
                    plate.tiles.add((x, y))

            self.plates[i] = plate

        print(f"  ✓ {len(self.plates)} plaques creades")
        for pid, plate in self.plates.items():
            print(f"    Placa {pid}: {plate.plate_type.value}, {len(plate.tiles)} tiles, "
                  f"{plate.get_speed():.1f} cm/any")

    def detect_boundaries(self) -> None:
        """Detecta límits entre plaques"""
        print("Detectant límits de plaques...")

        boundary_tiles: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}  # (plate1, plate2) -> tiles

        for x in range(self.world_width):
            for y in range(self.world_height):
                plate_id = self.plate_map.get((x, y), -1)
                if plate_id == -1:
                    continue

                # Comprova veïns
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx = (x + dx) % self.world_width
                    ny = (y + dy) % self.world_height

                    neighbor_plate = self.plate_map.get((nx, ny), -1)

                    if neighbor_plate != -1 and neighbor_plate != plate_id:
                        # Límit entre plaques
                        key = tuple(sorted([plate_id, neighbor_plate]))
                        if key not in boundary_tiles:
                            boundary_tiles[key] = []
                        boundary_tiles[key].append((x, y))

        # Crea objectes PlateBoundary
        self.boundaries = []
        for (p1, p2), tiles in boundary_tiles.items():
            plate1 = self.plates[p1]
            plate2 = self.plates[p2]

            # Determina tipus de límit segons velocitats
            boundary_type = self._determine_boundary_type(plate1, plate2)

            # Activitat segons tipus i velocitats
            activity = self._calculate_boundary_activity(plate1, plate2, boundary_type)

            boundary = PlateBoundary(
                plate1_id=p1,
                plate2_id=p2,
                boundary_type=boundary_type,
                tiles=list(set(tiles)),  # Elimina duplicats
                activity_level=activity
            )

            self.boundaries.append(boundary)

        print(f"  ✓ {len(self.boundaries)} límits detectats")
        boundary_counts = {}
        for b in self.boundaries:
            boundary_counts[b.boundary_type.value] = boundary_counts.get(b.boundary_type.value, 0) + 1

        for btype, count in boundary_counts.items():
            print(f"    {btype}: {count} límits")

    def _determine_boundary_type(self, plate1: TectonicPlate, plate2: TectonicPlate) -> BoundaryType:
        """Determina tipus de límit segons velocitats relatives"""
        # Velocitat relativa
        rel_vx = plate1.velocity_x - plate2.velocity_x
        rel_vy = plate1.velocity_y - plate2.velocity_y
        rel_speed = math.sqrt(rel_vx**2 + rel_vy**2)

        # Direcció relativa
        angle_diff = abs(plate1.get_direction() - plate2.get_direction())

        if angle_diff < math.pi / 6 or angle_diff > 5 * math.pi / 6:
            # Plaques van en direccions similars/oposades
            if rel_speed < 3.0:
                return BoundaryType.TRANSFORM
            else:
                return BoundaryType.DIVERGENT if angle_diff < math.pi / 2 else BoundaryType.CONVERGENT
        else:
            # Direccions perpendiculars
            return BoundaryType.TRANSFORM

    def _calculate_boundary_activity(
        self,
        plate1: TectonicPlate,
        plate2: TectonicPlate,
        boundary_type: BoundaryType
    ) -> float:
        """Calcula nivell d'activitat del límit"""
        # Velocitat relativa
        rel_vx = plate1.velocity_x - plate2.velocity_x
        rel_vy = plate1.velocity_y - plate2.velocity_y
        rel_speed = math.sqrt(rel_vx**2 + rel_vy**2)

        # Activitat base segons tipus
        if boundary_type == BoundaryType.CONVERGENT:
            base_activity = 0.8  # Alta activitat
        elif boundary_type == BoundaryType.DIVERGENT:
            base_activity = 0.6  # Activitat moderada
        else:  # TRANSFORM
            base_activity = 0.7  # Activitat moderada-alta

        # Ajusta segons velocitat (més ràpid = més activitat)
        activity = base_activity * (rel_speed / 10.0)
        return min(1.0, activity)

    def simulate_geological_events(
        self,
        year: int,
        world_tiles: Dict[Tuple[int, int], any]
    ) -> List[GeologicalEvent]:
        """
        Simula esdeveniments geològics (terratrèmols, volcans)

        Args:
            year: Any actual
            world_tiles: Tiles del món per modificar altitud

        Returns:
            Llista d'esdeveniments generats
        """
        events = []

        for boundary in self.boundaries:
            # Probabilitat d'esdeveniment segons activitat
            if random.random() > boundary.activity_level:
                continue

            # Selecciona tile aleatori del límit
            if not boundary.tiles:
                continue

            x, y = random.choice(boundary.tiles)

            if boundary.boundary_type == BoundaryType.CONVERGENT:
                # Zona de subducció o col·lisió continental
                plate1 = self.plates[boundary.plate1_id]
                plate2 = self.plates[boundary.plate2_id]

                if plate1.plate_type == PlateType.OCEANIC and plate2.plate_type == PlateType.OCEANIC:
                    # Subducció oceànica → Fossa i volcans
                    event_type = "volcano" if random.random() < 0.3 else "earthquake"
                    magnitude = random.uniform(5.0, 8.5)

                    if event_type == "volcano":
                        description = "Erupció volcànica submarina"
                        # Incrementa altitud (volcà)
                        if (x, y) in world_tiles:
                            world_tiles[(x, y)].altitude = min(1.0, world_tiles[(x, y)].altitude + 0.15)
                    else:
                        description = f"Terratrèmol de magnitud {magnitude:.1f}"

                elif plate1.plate_type == PlateType.CONTINENTAL and plate2.plate_type == PlateType.CONTINENTAL:
                    # Col·lisió continental → Muntanyes
                    event_type = "mountain_building"
                    magnitude = random.uniform(4.0, 7.0)
                    description = "Formació de muntanyes per col·lisió"

                    # Incrementa altitud (muntanya)
                    if (x, y) in world_tiles:
                        world_tiles[(x, y)].altitude = min(1.0, world_tiles[(x, y)].altitude + 0.10)

                else:
                    # Subducció oceànica-continental → Volcans i terratrèmols
                    event_type = "volcano" if random.random() < 0.4 else "earthquake"
                    magnitude = random.uniform(6.0, 9.0)

                    if event_type == "volcano":
                        description = "Erupció volcànica en zona de subducció"
                        if (x, y) in world_tiles:
                            world_tiles[(x, y)].altitude = min(1.0, world_tiles[(x, y)].altitude + 0.12)
                    else:
                        description = f"Terratrèmol de subducció, magnitud {magnitude:.1f}"

            elif boundary.boundary_type == BoundaryType.DIVERGENT:
                # Rift o dorsal oceànica
                event_type = "earthquake" if random.random() < 0.7 else "volcano"
                magnitude = random.uniform(4.0, 6.5)

                if event_type == "volcano":
                    description = "Activitat volcànica en dorsal oceànica"
                    if (x, y) in world_tiles:
                        world_tiles[(x, y)].altitude = min(1.0, world_tiles[(x, y)].altitude + 0.08)
                else:
                    description = f"Terratrèmol de rift, magnitud {magnitude:.1f}"

            else:  # TRANSFORM
                # Falla transformant
                event_type = "earthquake"
                magnitude = random.uniform(5.0, 8.0)
                description = f"Terratrèmol de falla transformant, magnitud {magnitude:.1f}"

            event = GeologicalEvent(
                event_type=event_type,
                x=x,
                y=y,
                year=year,
                magnitude=magnitude,
                description=description
            )

            events.append(event)
            self.geological_events.append(event)

        return events

    def get_plate_at(self, x: int, y: int) -> Optional[TectonicPlate]:
        """Obté placa en una posició"""
        plate_id = self.plate_map.get((x, y))
        return self.plates.get(plate_id) if plate_id is not None else None

    def get_statistics(self) -> Dict:
        """Obté estadístiques del sistema"""
        plate_types = {}
        for plate in self.plates.values():
            ptype = plate.plate_type.value
            plate_types[ptype] = plate_types.get(ptype, 0) + 1

        event_types = {}
        for event in self.geological_events:
            etype = event.event_type
            event_types[etype] = event_types.get(etype, 0) + 1

        avg_speed = sum(p.get_speed() for p in self.plates.values()) / len(self.plates) if self.plates else 0

        return {
            'total_plates': len(self.plates),
            'plate_types': plate_types,
            'total_boundaries': len(self.boundaries),
            'boundary_types': {
                'divergent': sum(1 for b in self.boundaries if b.boundary_type == BoundaryType.DIVERGENT),
                'convergent': sum(1 for b in self.boundaries if b.boundary_type == BoundaryType.CONVERGENT),
                'transform': sum(1 for b in self.boundaries if b.boundary_type == BoundaryType.TRANSFORM)
            },
            'total_geological_events': len(self.geological_events),
            'event_types': event_types,
            'average_plate_speed': avg_speed
        }
