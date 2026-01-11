#!/usr/bin/env python3
"""
Test de generació del món

Genera un món i mostra estadístiques i un preview ASCII
"""
import sys
import time
from overworld.world.world import World


def print_ascii_map(world: World, layer: str = "altitude", width: int = 80):
    """
    Mostra un preview ASCII del món

    Args:
        layer: "altitude", "humidity", "temperature", "fertility"
        width: Amplada del preview en caràcters
    """
    # Calcula el downsampling
    step_x = max(1, world.width // width)
    step_y = max(1, world.height // (width // 2))  # Aspecte 2:1

    print(f"\n{layer.upper()} MAP:")
    print("=" * width)

    for y in range(0, world.height, step_y):
        line = ""
        for x in range(0, world.width, step_x):
            tile = world.get_tile(x, y)

            if layer == "altitude":
                value = tile.altitude
            elif layer == "humidity":
                value = tile.humidity
            elif layer == "temperature":
                value = tile.temperature
            elif layer == "fertility":
                value = tile.fertility_index / 10
            else:
                value = 0

            # Aigua sempre en blau
            if tile.is_water and layer == "altitude":
                char = "~"
            elif tile.is_river and layer == "altitude":
                char = "≈"
            else:
                # Escala ASCII segons el valor
                chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
                idx = int(value * (len(chars) - 1))
                char = chars[idx]

            line += char
        print(line)

    print("=" * width)


def main():
    """Test de generació del món"""
    print("=" * 80)
    print("  TEST DE GENERACIÓ DEL MÓN")
    print("=" * 80)
    print()

    # Crea un món petit per al test (100x100 és ràpid)
    # Per producció usa 500x500 o més
    print("Creant món de 150x150...")
    world = World(width=150, height=150, seed=12345)

    # Genera el món
    start_time = time.time()
    world.generate(island_mode=False, num_rivers=10)
    elapsed = time.time() - start_time

    print(f"\n✓ Món generat en {elapsed:.2f} segons")
    print()

    # Mostra estadístiques
    print("ESTADÍSTIQUES DEL MÓN:")
    print("-" * 80)
    stats = world.get_statistics()

    print(f"Mida: {stats['total_tiles']} tiles ({world.width}x{world.height})")
    print(f"Aigua: {stats['water_tiles']} tiles ({stats['water_percentage']:.1f}%)")
    print(f"Terra: {stats['land_tiles']} tiles")
    print(f"Rius: {stats['river_tiles']} tiles")
    print()
    print(f"Terra fèrtil (>6): {stats['fertile_land']} tiles ({stats['fertile_percentage']:.1f}%)")
    print(f"Terra hostil (>7): {stats['hostile_land']} tiles ({stats['hostile_percentage']:.1f}%)")
    print()
    print(f"Altitud mitjana: {stats['avg_altitude']:.3f}")
    print(f"Temperatura mitjana: {stats['avg_temperature']:.3f}")
    print(f"Humitat mitjana: {stats['avg_humidity']:.3f}")
    print()

    # Mostra alguns tiles interessants
    print("TILES INTERESSANTS:")
    print("-" * 80)

    # Terra més fèrtil
    fertile_tiles = world.find_tiles_by_criteria(min_fertility=8.0, is_water=False)
    if fertile_tiles:
        tile = fertile_tiles[0]
        print(f"🌾 Terra més fèrtil: ({tile.x}, {tile.y})")
        print(f"   Fertilitat: {tile.fertility_index:.1f}/10")
        print(f"   Altitud: {tile.altitude:.2f}, Humitat: {tile.humidity:.2f}, Temp: {tile.temperature:.2f}")
        print()

    # Muntanya més alta
    mountains = world.find_tiles_by_criteria(min_altitude=0.9, is_water=False)
    if mountains:
        tile = mountains[0]
        print(f"⛰️  Muntanya més alta: ({tile.x}, {tile.y})")
        print(f"   Altitud: {tile.altitude:.2f}")
        print(f"   Hostilitat: {tile.hostility:.1f}/10")
        print()

    # Rius
    rivers = [t for row in world.tiles for t in row if t.is_river]
    if rivers:
        tile = rivers[0]
        print(f"💧 Exemple de riu: ({tile.x}, {tile.y})")
        print(f"   Aigua: {tile.resources['water']:.0f}/100")
        print()

    # Mostra mapes ASCII
    print_ascii_map(world, "altitude", width=80)
    print_ascii_map(world, "temperature", width=80)
    print_ascii_map(world, "fertility", width=80)

    print()
    print("=" * 80)
    print("Test completat!")
    print()
    print("Pròxims passos:")
    print("  - Assignar biomes segons altitud/humitat/temperatura")
    print("  - Generar recursos naturals (minerals, petroli, etc.)")
    print("  - Implementar tectònica de plaques")
    print("  - Renderitzar amb pygame en colors")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
