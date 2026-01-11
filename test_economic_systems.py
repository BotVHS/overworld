#!/usr/bin/env python3
"""
Test del sistema econòmic emergent

Genera sistemes econòmics únics per a civilitzacions amb diferents contextos
"""
import sys
from overworld.world.world import World
from overworld.civilization.civilization import create_civilizations
from overworld.emergent_systems.economic_systems import EconomicSystemGenerator


def main():
    """Test del sistema econòmic"""
    print("=" * 80)
    print("  TEST DEL SISTEMA ECONÒMIC EMERGENT")
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

    # Crea generador de sistemes econòmics
    print("=" * 80)
    print("GENERANT SISTEMES ECONÒMICS ÚNICS")
    print("=" * 80)
    print()

    generator = EconomicSystemGenerator(use_ollama=True)

    if generator.ollama and generator.ollama.available:
        print("✓ Ollama disponible - generant economies amb IA")
    else:
        print("⚠ Ollama no disponible - usant generació procedural")
    print()

    # Genera sistema econòmic per cada civilització
    for i, civ in enumerate(civ_manager.civilizations, 1):
        print(f"\n{'=' * 80}")
        print(f"CIVILITZACIÓ {i}: {civ.name}")
        print(f"{'=' * 80}")

        # Context de la civilització
        capital_tile = world.get_tile(civ.capital.x, civ.capital.y)

        from overworld.world.biome import BIOME_DEFINITIONS
        environment_type = BIOME_DEFINITIONS[capital_tile.biome].name if capital_tile.biome else "Desconegut"

        # Comprova si és costaner
        is_coastal = False
        neighbors = world.get_neighbors(civ.capital.x, civ.capital.y, radius=1)
        for neighbor in neighbors:
            if neighbor.is_water:
                is_coastal = True
                break

        # Obté recursos disponibles (filtra recursos amb valor > 0)
        available_resources = []
        if capital_tile.resources:
            available_resources = [
                resource_name.capitalize()
                for resource_name, amount in capital_tile.resources.items()
                if amount > 10.0 and resource_name not in ['minerals', 'water', 'fertility']
            ]

        print(f"Població: {civ.total_population:,} habitants")
        print(f"Entorn: {environment_type} ({'Costaner' if is_coastal else 'Interior'})")
        print(f"Recursos: {', '.join(available_resources) if available_resources else 'Cap'}")
        print(f"Nivell Tecnològic: {civ.tech_level}/8")
        print(f"Cultura: {civ.get_cultural_description()}")
        print(f"  Comerç: {civ.culture.commerce:.0f}/100")
        print(f"  Navegació: {civ.culture.navigation:.0f}/100")
        print(f"  Mineria: {civ.culture.mining:.0f}/100")
        print(f"  Agricultura: {civ.culture.agriculture:.0f}/100")
        print()

        # Genera sistema econòmic
        print("Generant sistema econòmic...")
        print()

        economic_system = generator.generate_system(
            civilization_name=civ.name,
            population=civ.total_population,
            environment_type=environment_type,
            is_coastal=is_coastal,
            available_resources=available_resources,
            culture_traits=civ.culture.to_dict(),
            tech_level=civ.tech_level,
            recent_history=civ.historical_events,
            neighbors_count=len(civ_manager.civilizations) - 1
        )

        # Mostra el sistema econòmic generat
        print(f"💰 SISTEMA ECONÒMIC: {economic_system.name}")
        print(f"{'─' * 80}")
        print(f"\nModel Econòmic:")
        print(f"  {economic_system.economic_model}")
        print(f"\nRecursos Primaris:")
        for resource in economic_system.primary_resources:
            print(f"  📦 {resource}")
        print(f"\nFocus Comercial: {economic_system.trade_focus}")
        print(f"Tipus de Moneda: {economic_system.currency_type}")
        print(f"\nDistribució de la Riquesa:")
        print(f"  {economic_system.wealth_distribution}")
        print(f"\nSistema d'Impostos:")
        print(f"  {economic_system.taxation_system}")
        print(f"\nEstructura de Gremis:")
        print(f"  {economic_system.guild_structure}")
        print(f"\nRegulació del Mercat:")
        print(f"  {economic_system.market_regulation}")
        print(f"\nOrigen Històric:")
        print(f"  {economic_system.historical_origin}")
        print(f"\nAvantatges:")
        for adv in economic_system.advantages:
            print(f"  ✓ {adv}")
        print(f"\nDesavantatges:")
        for dis in economic_system.disadvantages:
            print(f"  ✗ {dis}")
        print(f"\nÍndex de Prosperitat: {economic_system.prosperity_index}/10")
        print(f"Índex de Desigualtat: {economic_system.inequality_index}/10")

    print()
    print("=" * 80)
    print("Test completat!")
    print()
    print("Observacions:")
    print("  - Economies adaptades a recursos i geografia disponibles")
    print("  - Cultures comercials desenvolupen mercats més lliures")
    print("  - Cultures autoritàries tendeixen a planificació centralitzada")
    print("  - Civilitzacions costaneres desenvolupen talassocràcies")
    print()
    print("Pròxims passos:")
    print("  - Afegir sistemes econòmics a la classe Civilization")
    print("  - Implementar comerç entre civilitzacions")
    print("  - Simulació econòmica temporal (creixement, crisi, etc.)")
    print("  - Integració amb Ollama per decisions de líders")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
