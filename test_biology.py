#!/usr/bin/env python3
"""
Test del sistema biològic

Genera un món i pobla'l amb espècies
"""
import sys
from overworld.world.world import World
from overworld.biology.ecosystem import create_default_ecosystem


def main():
    """Test del sistema biològic"""
    print("=" * 80)
    print("  TEST DEL SISTEMA BIOLÒGIC")
    print("=" * 80)
    print()

    # Genera un món petit
    print("Generant món 150x150...")
    world = World(width=150, height=150, seed=42)
    world.generate(island_mode=False, num_rivers=10)
    print()

    # Crea ecosistema
    print("Creant ecosistema amb espècies predefinides...")
    print()
    ecosystem = create_default_ecosystem(world)
    print()

    # Mostra estadístiques
    print("=" * 80)
    print("ESTADÍSTIQUES DE L'ECOSISTEMA")
    print("=" * 80)

    stats = ecosystem.get_statistics()

    print(f"Total d'espècies: {stats['total_species']}")
    print(f"  - Animals: {stats['animal_species']}")
    print(f"  - Plantes: {stats['plant_species']}")
    print()
    print(f"Poblacions totals: {stats['total_populations']}")
    print(f"Individus totals: {stats['total_individuals']:,}")
    print(f"Biomassa total: {stats['total_biomass']:,.0f} kg")
    print()

    print("DETALL PER ESPÈCIE:")
    print("-" * 80)
    for species_stat in stats['species_details']:
        name = species_stat['name']
        stype = species_stat['type']
        count = species_stat['count']
        biomass = species_stat['biomass']

        icon = "🌿" if stype == "plant" else "🦌"
        print(f"{icon} {name:15} ({stype:15}): {count:7,} individus | {biomass:12,.0f} kg")

    print()

    # Mostra exemples de tiles amb vida
    print("=" * 80)
    print("EXEMPLES DE TILES AMB VIDA")
    print("=" * 80)

    tiles_with_life = [
        (coords, pops) for coords, pops in ecosystem.populations.items()
        if len(pops) >= 2  # Tiles amb almenys 2 espècies
    ]

    # Ordena per biodiversitat
    tiles_with_life.sort(key=lambda x: len(x[1]), reverse=True)

    for i, (coords, pops) in enumerate(tiles_with_life[:5]):
        x, y = coords
        tile = world.get_tile(x, y)

        from overworld.world.biome import BIOME_DEFINITIONS
        biome_name = BIOME_DEFINITIONS[tile.biome].name if tile.biome else "?"

        print(f"\n📍 Tile ({x}, {y}) - {biome_name}")
        print(f"   Temperatura: {tile.temperature:.2f} | Humitat: {tile.humidity:.2f}")
        print(f"   Espècies presents: {len(pops)}")

        for pop in pops:
            icon = "🌿" if pop.species.species_type.value == "plant" else "🦌"
            print(f"     {icon} {pop.species.name}: {pop.count} individus ({pop.biomass:.0f} kg)")

    print()
    print("=" * 80)
    print("Test completat!")
    print()
    print("Pròxims passos:")
    print("  - Implementar simulació temporal (naixement, mort, migració)")
    print("  - Cadenes tròfiques (depredadors cacen preses)")
    print("  - Evolució (mutacions, selecció natural)")
    print("  - Competència per recursos")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
