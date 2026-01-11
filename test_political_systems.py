#!/usr/bin/env python3
"""
Test del sistema polític emergent

Genera sistemes polítics únics per a civilitzacions amb diferents contextos
"""
import sys
from overworld.world.world import World
from overworld.civilization.civilization import create_civilizations
from overworld.emergent_systems.political_systems import PoliticalSystemGenerator


def main():
    """Test del sistema polític"""
    print("=" * 80)
    print("  TEST DEL SISTEMA POLÍTIC EMERGENT")
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

    # Crea generador de sistemes polítics
    print("=" * 80)
    print("GENERANT SISTEMES POLÍTICS ÚNICS")
    print("=" * 80)
    print()

    generator = PoliticalSystemGenerator(use_ollama=True)

    if generator.ollama and generator.ollama.available:
        print("✓ Ollama disponible - generant sistemes amb IA")
    else:
        print("⚠ Ollama no disponible - usant generació procedural")
    print()

    # Genera sistema polític per cada civilització
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
        print(f"  Militarisme: {civ.culture.militarism:.0f}/100")
        print(f"  Comerç: {civ.culture.commerce:.0f}/100")
        print(f"  Autoritarisme: {civ.culture.authoritarianism:.0f}/100")
        print()

        # Genera sistema polític
        print("Generant sistema polític...")
        print()

        political_system = generator.generate_system(
            civilization_name=civ.name,
            population=civ.total_population,
            environment_type=environment_type,
            hostility=capital_tile.hostility,
            fertility=capital_tile.fertility_index,
            culture_traits=civ.culture.to_dict(),
            recent_history=civ.historical_events,
            traumas=None,  # Podríem afegir traumes si tinguéssim simulació històrica
            glories=None   # Podríem afegir glòries si tinguéssim simulació històrica
        )

        # Mostra el sistema polític generat
        print(f"🏛️  SISTEMA POLÍTIC: {political_system.name}")
        print(f"{'─' * 80}")
        print(f"\nDescripció:")
        print(f"  {political_system.description}")
        print(f"\nFuncionament:")
        print(f"  {political_system.how_it_works}")
        print(f"\nOrigen Històric:")
        print(f"  {political_system.historical_origin}")
        print(f"\nAvantatges:")
        for adv in political_system.advantages:
            print(f"  ✓ {adv}")
        print(f"\nDesavantatges:")
        for dis in political_system.disadvantages:
            print(f"  ✗ {dis}")
        print(f"\nEstabilitat: {political_system.stability}/10")
        print(f"Satisfacció Popular: {political_system.popular_satisfaction}/10")

    print()
    print("=" * 80)
    print("Test completat!")
    print()
    print("Pròxims passos:")
    print("  - Afegir sistemes polítics a la classe Civilization")
    print("  - Implementar evolució dels sistemes polítics al llarg del temps")
    print("  - Generar esdeveniments polítics (revolucions, reformes, cops d'estat)")
    print("  - Sistemes religiosos emergents")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
