#!/usr/bin/env python3
"""
Test del sistema de civilitzacions

Genera un món i crea civilitzacions intel·ligents
"""
import sys
from overworld.world.world import World
from overworld.civilization.civilization import create_civilizations


def main():
    """Test de civilitzacions"""
    print("=" * 80)
    print("  TEST DE CIVILITZACIONS INTEL·LIGENTS")
    print("=" * 80)
    print()

    # Genera món
    print("Generant món 150x150...")
    world = World(width=150, height=150, seed=123)
    world.generate(island_mode=False, num_rivers=10)
    print()

    # Crea civilitzacions
    print("Creant civilitzacions adaptades a l'entorn...")
    print()
    civ_manager = create_civilizations(world, count=8)
    print()

    # Mostra estadístiques
    print("=" * 80)
    print("ESTADÍSTIQUES DE LES CIVILITZACIONS")
    print("=" * 80)

    stats = civ_manager.get_statistics()

    print(f"Total civilitzacions: {stats['total_civilizations']}")
    print(f"Població total: {stats['total_population']:,}")
    print(f"Ciutats totals: {stats['total_cities']}")
    print()

    print("DISTRIBUCIÓ D'ARQUETIPS CULTURALS:")
    print("-" * 80)
    for archetype, count in stats['archetypes'].items():
        percentage = (count / stats['total_civilizations']) * 100
        print(f"  {archetype:15}: {count} ({percentage:.1f}%)")
    print()

    print("DETALL DE CIVILITZACIONS:")
    print("=" * 80)

    for i, civ in enumerate(civ_manager.civilizations, 1):
        print(f"\n{i}. {civ.name}")
        print(f"   {'=' * 70}")

        # Informació bàsica
        capital = civ.capital
        if capital:
            tile = world.get_tile(capital.x, capital.y)
            from overworld.world.biome import BIOME_DEFINITIONS
            biome_name = BIOME_DEFINITIONS[tile.biome].name if tile.biome else "?"

            print(f"   📍 Capital: {capital.name} ({capital.x}, {capital.y})")
            print(f"   🌍 Bioma: {biome_name}")
            print(f"   🌡️  Clima: Temp={tile.temperature:.2f}, Humitat={tile.humidity:.2f}")
            print(f"   🌾 Fertilitat: {tile.fertility_index:.1f}/10")
            print(f"   ⚔️  Hostilitat: {tile.hostility:.1f}/10")
            print()

        # Cultura
        archetype = civ.get_cultural_archetype()
        print(f"   📜 Arquetip cultural: {archetype.value.upper()}")
        print(f"   📖 Descripció: {civ.get_cultural_description()}")
        print()

        print(f"   💭 Valors fonamentals:")
        for value in civ.culture.core_values:
            print(f"      • {value.capitalize()}")
        print()

        print(f"   📊 Trets culturals (principals):")
        print(f"      • Militarisme: {civ.culture.militarism:.0f}/100")
        print(f"      • Comerç: {civ.culture.commerce:.0f}/100")
        print(f"      • Ciència: {civ.culture.science:.0f}/100")
        print(f"      • Religió: {civ.culture.religion:.0f}/100")
        print(f"      • Art: {civ.culture.art:.0f}/100")
        print(f"      • Agricultura: {civ.culture.agriculture:.0f}/100")
        print()

        print(f"   🏛️  Trets socials:")
        print(f"      • Autoritarisme: {civ.culture.authoritarianism:.0f}/100")
        print(f"      • Col·lectivisme: {civ.culture.collectivism:.0f}/100")
        print(f"      • Expansionisme: {civ.culture.expansionism:.0f}/100")
        print(f"      • Aïllacionisme: {civ.culture.isolationism:.0f}/100")
        print()

        # Especialitzacions
        specializations = []
        if civ.culture.navigation > 70:
            specializations.append("⛵ Navegació")
        if civ.culture.mining > 70:
            specializations.append("⛏️ Mineria")
        if civ.culture.craftsmanship > 70:
            specializations.append("🔨 Artesania")

        if specializations:
            print(f"   ⭐ Especialitzacions:")
            for spec in specializations:
                print(f"      • {spec}")
            print()

        # Població i ciutats
        print(f"   👥 Població: {civ.total_population:,}")
        print(f"   🏙️  Ciutats: {len(civ.cities)}")
        print(f"   🔬 Nivell tecnològic: {civ.tech_level} (Edat de pedra)")
        print(f"   📅 Fundada: Any {civ.founded_year}")

    print()
    print("=" * 80)
    print("Test completat!")
    print()
    print("Observacions:")
    print("  - Cultures evolucionen segons l'entorn (hostil → guerrera, fèrtil → pacífica)")
    print("  - Civilitzacions costaners tenen alta navegació")
    print("  - Civilitzacions de muntanya tenen alta mineria")
    print("  - Valors culturals reflecteixen l'adaptació a l'entorn")
    print()
    print("Pròxims passos:")
    print("  - Integració amb Ollama per decisions de líders")
    print("  - Diplomàcia entre civilitzacions")
    print("  - Expansió territorial")
    print("  - Progressió tecnològica")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
