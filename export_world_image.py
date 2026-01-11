#!/usr/bin/env python3
"""
Exportador d'imatges del món

Genera un món i exporta imatges de les diferents capes.
"""
import sys
from PIL import Image
from overworld.world.world import World
from overworld.world.biome import BIOME_DEFINITIONS


def export_layer(world: World, layer: str, output_path: str):
    """
    Exporta una capa del món com a imatge PNG

    Args:
        world: Món a exportar
        layer: Capa a exportar (biomes, altitude, temperature, etc.)
        output_path: Camí del fitxer de sortida
    """
    # Crea imatge
    img = Image.new('RGB', (world.width, world.height))
    pixels = img.load()

    # Genera píxels
    for y in range(world.height):
        for x in range(world.width):
            tile = world.get_tile(x, y)

            if layer == "biomes":
                if tile.biome:
                    color = BIOME_DEFINITIONS[tile.biome].color
                else:
                    color = (100, 100, 100)

            elif layer == "altitude":
                value = tile.altitude
                if tile.is_water:
                    intensity = int(value * 255)
                    color = (0, intensity // 2, 100 + intensity // 2)
                else:
                    if value < 0.6:
                        intensity = int((value - 0.35) / 0.25 * 255)
                        color = (intensity // 2, 100 + intensity // 2, intensity // 4)
                    elif value < 0.8:
                        intensity = int((value - 0.6) / 0.2 * 255)
                        color = (100 + intensity // 2, 80 + intensity // 3, 60)
                    else:
                        intensity = int((value - 0.8) / 0.2 * 255)
                        color = (200 + intensity // 4, 200 + intensity // 4, 200 + intensity // 4)

            elif layer == "temperature":
                value = tile.temperature
                if value < 0.5:
                    blue = int((0.5 - value) * 2 * 255)
                    red = int(value * 2 * 100)
                    color = (red, 50, blue)
                else:
                    red = int((value - 0.5) * 2 * 255)
                    green = int((1.0 - value) * 2 * 100)
                    color = (100 + red, green, 0)

            elif layer == "humidity":
                value = tile.humidity
                if value < 0.5:
                    brown = int((0.5 - value) * 2 * 200)
                    blue = int(value * 2 * 100)
                    color = (100 + brown, 80 + brown // 2, blue)
                else:
                    green = int((value - 0.5) * 2 * 150)
                    blue = int(value * 255)
                    color = (0, green, blue)

            elif layer == "fertility":
                value = tile.fertility_index / 10.0
                if value < 0.5:
                    red = int((0.5 - value) * 2 * 255)
                    green = int(value * 2 * 150)
                    color = (red, green, 0)
                else:
                    green = int(150 + (value - 0.5) * 2 * 105)
                    color = (0, green, 0)

            else:
                color = (100, 100, 100)

            pixels[x, y] = color

    # Guarda imatge
    img.save(output_path)
    print(f"✓ Exportat: {output_path}")


def main():
    """Genera un món i exporta imatges"""
    print("=" * 80)
    print("  OVERWORLD - EXPORTADOR D'IMATGES")
    print("=" * 80)
    print()

    # Genera món
    print("Generant món 300x300...")
    world = World(width=300, height=300, seed=12345)
    world.generate(island_mode=False, num_rivers=20)

    print()
    print("✓ Món generat!")
    print()

    # Exporta capes
    print("Exportant capes com a imatges PNG...")
    print()

    layers = [
        ("biomes", "world_biomes.png"),
        ("altitude", "world_altitude.png"),
        ("temperature", "world_temperature.png"),
        ("humidity", "world_humidity.png"),
        ("fertility", "world_fertility.png"),
    ]

    for layer_name, filename in layers:
        export_layer(world, layer_name, filename)

    print()
    print("=" * 80)
    print("✓ Exportació completada!")
    print()
    print("Fitxers generats:")
    for _, filename in layers:
        print(f"  - {filename}")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
