#!/usr/bin/env python3
"""
Test del sistema religiós emergent

Genera religions úniques per a civilitzacions amb diferents contextos
"""
import sys
from overworld.world.world import World
from overworld.civilization.civilization import create_civilizations
from overworld.emergent_systems.religious_systems import ReligiousSystemGenerator


def main():
    """Test del sistema religiós"""
    print("=" * 80)
    print("  TEST DEL SISTEMA RELIGIÓS EMERGENT")
    print("=" * 80)
    print()

    # Genera un món petit
    print("Generant món 150x150...")
    world = World(width=150, height=150, seed=42)
    world.generate(island_mode=False, num_rivers=10)
    print()

    # Crea civilitzacions
    print("Creant civilitzacions...")
    civ_manager = create_civilizations(world, count=5)
    print()

    # Crea generador de sistemes religiosos
    print("=" * 80)
    print("GENERANT SISTEMES RELIGIOSOS ÚNICS")
    print("=" * 80)
    print()

    generator = ReligiousSystemGenerator(use_ollama=True)

    if generator.ollama and generator.ollama.available:
        print("✓ Ollama disponible - generant religions amb IA")
    else:
        print("⚠ Ollama no disponible - usant generació procedural")
    print()

    # Genera sistema religiós per cada civilització
    for i, civ in enumerate(civ_manager.civilizations, 1):
        print(f"\n{'=' * 80}")
        print(f"CIVILITZACIÓ {i}: {civ.name}")
        print(f"{'=' * 80}")

        # Context de la civilització
        capital_tile = world.get_tile(civ.capital.x, civ.capital.y)

        from overworld.world.biome import BIOME_DEFINITIONS
        environment_type = BIOME_DEFINITIONS[capital_tile.biome].name if capital_tile.biome else "Desconegut"

        print(f"Població: {civ.total_population:,} habitants")
        print(f"Entorn: {environment_type}")
        print(f"  Hostilitat: {capital_tile.hostility:.1f}/10")
        print(f"  Fertilitat: {capital_tile.fertility_index:.1f}/10")
        print(f"Cultura: {civ.get_cultural_description()}")
        print(f"  Religiositat: {civ.culture.religion:.0f}/100")
        print(f"  Ciència: {civ.culture.science:.0f}/100")
        print(f"  Militarisme: {civ.culture.militarism:.0f}/100")
        print()

        # Genera sistema religiós
        print("Generant sistema religiós...")
        print()

        religious_system = generator.generate_system(
            civilization_name=civ.name,
            population=civ.total_population,
            environment_type=environment_type,
            hostility=capital_tile.hostility,
            fertility=capital_tile.fertility_index,
            culture_traits=civ.culture.to_dict(),
            recent_history=civ.historical_events,
            traumas=None,
            glories=None,
            natural_disasters=None
        )

        # Mostra el sistema religiós generat
        print(f"🙏 RELIGIÓ: {religious_system.name}")
        print(f"{'─' * 80}")
        print(f"\nTipus de Divinitat: {religious_system.deity_type}")
        print(f"\nDoctrina Central:")
        print(f"  {religious_system.core_doctrine}")
        print(f"\nMite de Creació:")
        print(f"  {religious_system.creation_myth}")
        print(f"\nCreença en el Més Enllà:")
        print(f"  {religious_system.afterlife_belief}")
        print(f"\nPràctiques Sagrades:")
        for practice in religious_system.sacred_practices:
            print(f"  🕯️  {practice}")
        print(f"\nTabús:")
        for taboo in religious_system.taboos:
            print(f"  ⛔ {taboo}")
        print(f"\nEstructura del Clergat:")
        print(f"  {religious_system.clergy_structure}")
        print(f"\nOrigen Històric:")
        print(f"  {religious_system.historical_origin}")
        print(f"\nInfluència Social: {religious_system.influence_on_society}/10")
        print(f"Dogmatisme: {religious_system.dogmatism}/10")

    print()
    print("=" * 80)
    print("Test completat!")
    print()
    print("Observacions:")
    print("  - Religions adaptades a l'entorn (costa→déus marítims, desert→monoteisme)")
    print("  - Cultures científiques generen filosofies més racionals")
    print("  - Cultures militaristes generen cultes guerrers")
    print("  - Alta religiositat → major influència social")
    print()
    print("Pròxims passos:")
    print("  - Afegir sistemes religiosos a la classe Civilization")
    print("  - Implementar evolució religiosa (cismes, reformes, sincretisme)")
    print("  - Conflictes religiosos entre civilitzacions")
    print("  - Sistemes econòmics emergents")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
