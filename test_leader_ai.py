#!/usr/bin/env python3
"""
Test del sistema d'IA de líders

Demostra com els líders prenen decisions basades en personalitat, cultura i context
"""
import sys
from overworld.world.world import World
from overworld.civilization.civilization import create_civilizations
from overworld.emergent_systems.political_systems import PoliticalSystemGenerator
from overworld.emergent_systems.religious_systems import ReligiousSystemGenerator
from overworld.emergent_systems.economic_systems import EconomicSystemGenerator
from overworld.ai.leader_ai import (
    LeaderAI, DecisionContext, DecisionType,
    generate_leader_personality
)


def main():
    """Test de l'IA de líders"""
    print("=" * 80)
    print("  TEST DE L'IA DE LÍDERS")
    print("=" * 80)
    print()

    # Genera un món petit
    print("Generant món 150x150...")
    world = World(width=150, height=150, seed=42)
    world.generate(island_mode=False, num_rivers=10)
    print()

    # Crea civilitzacions
    print("Creant civilitzacions...")
    civ_manager = create_civilizations(world, count=3)
    print()

    # Generadors de sistemes emergents
    print("Generant sistemes emergents...")
    political_gen = PoliticalSystemGenerator(use_ollama=True)
    religious_gen = ReligiousSystemGenerator(use_ollama=True)
    economic_gen = EconomicSystemGenerator(use_ollama=True)
    leader_ai = LeaderAI(use_ollama=True)

    if leader_ai.ollama and leader_ai.ollama.available:
        print("✓ Ollama disponible - decisions amb IA")
    else:
        print("⚠ Ollama no disponible - decisions procedurals")
    print()

    # Per cada civilització, genera sistemes i líder
    civilizations_data = []

    for civ in civ_manager.civilizations:
        capital_tile = world.get_tile(civ.capital.x, civ.capital.y)

        from overworld.world.biome import BIOME_DEFINITIONS
        environment_type = BIOME_DEFINITIONS[capital_tile.biome].name if capital_tile.biome else "Desconegut"

        # Genera sistemes emergents
        political_system = political_gen.generate_system(
            civilization_name=civ.name,
            population=civ.total_population,
            environment_type=environment_type,
            hostility=capital_tile.hostility,
            fertility=capital_tile.fertility_index,
            culture_traits=civ.culture.to_dict(),
            recent_history=civ.historical_events,
            traumas=None,
            glories=None
        )

        religious_system = religious_gen.generate_system(
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

        # Comprova si és costaner
        is_coastal = False
        neighbors = world.get_neighbors(civ.capital.x, civ.capital.y, radius=1)
        for neighbor in neighbors:
            if neighbor.is_water:
                is_coastal = True
                break

        # Recursos
        available_resources = [
            resource_name.capitalize()
            for resource_name, amount in capital_tile.resources.items()
            if amount > 10.0 and resource_name not in ['minerals', 'water', 'fertility']
        ]

        economic_system = economic_gen.generate_system(
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

        # Genera líder amb personalitat
        leader = generate_leader_personality(civ.name, civ.culture.to_dict())

        civilizations_data.append({
            'civilization': civ,
            'political_system': political_system,
            'religious_system': religious_system,
            'economic_system': economic_system,
            'leader': leader,
            'resources': available_resources
        })

    print("=" * 80)
    print("DECISIONS DELS LÍDERS")
    print("=" * 80)
    print()

    # Escenaris de decisió
    scenarios = [
        {
            'type': DecisionType.WAR_DECLARATION,
            'prompt': f"Un veí ha atacat una de les teves ciutats frontereres. Què fas?"
        },
        {
            'type': DecisionType.TRADE_AGREEMENT,
            'prompt': f"Un veí ofereix un tractat comercial favorable. Acceptes?"
        },
        {
            'type': DecisionType.POLITICAL_REFORM,
            'prompt': f"Hi ha descontentament popular amb el sistema polític actual. Què fas?"
        },
        {
            'type': DecisionType.EXPANSION,
            'prompt': f"Has descobert terres fèrtils deshabitades al nord. Què fas?"
        }
    ]

    for i, civ_data in enumerate(civilizations_data, 1):
        civ = civ_data['civilization']
        leader = civ_data['leader']

        print(f"\n{'=' * 80}")
        print(f"CIVILITZACIÓ {i}: {civ.name}")
        print(f"{'=' * 80}")

        print(f"\n👑 LÍDER: {leader.name}")
        print(f"{'─' * 80}")
        print(f"  Agressivitat: {leader.aggressiveness}/10")
        print(f"  Pragmatisme: {leader.pragmatism}/10")
        print(f"  Religiositat: {leader.religiosity}/10")
        print(f"  Expansionisme: {leader.expansionism}/10")
        print(f"  Tolerància al Risc: {leader.risk_tolerance}/10")
        print(f"  Habilitat Diplomàtica: {leader.diplomacy_skill}/10")

        print(f"\n🏛️  Sistemes:")
        print(f"  Polític: {civ_data['political_system'].name}")
        print(f"  Religiós: {civ_data['religious_system'].name}")
        print(f"  Econòmic: {civ_data['economic_system'].name}")

        print(f"\nCultura: {civ.get_cultural_description()}")
        print(f"  Militarisme: {civ.culture.militarism:.0f}/100")
        print(f"  Comerç: {civ.culture.commerce:.0f}/100")

        # Prova cada escenari
        for scenario in scenarios[:2]:  # Només 2 escenaris per civilització per no allargar-ho
            print(f"\n{'─' * 80}")
            print(f"📋 ESCENARI: {scenario['type'].value.upper()}")
            print(f"{'─' * 80}")
            print(f"Situació: {scenario['prompt']}")
            print()

            # Crea context de decisió
            context = DecisionContext(
                civilization_name=civ.name,
                leader_personality=leader,
                population=civ.total_population,
                tech_level=civ.tech_level,
                political_system=civ_data['political_system'].to_dict(),
                religious_system=civ_data['religious_system'].to_dict(),
                economic_system=civ_data['economic_system'].to_dict(),
                culture_traits=civ.culture.to_dict(),
                current_resources=civ_data['resources'],
                neighbors=[other['civilization'].name for other in civilizations_data if other['civilization'].id != civ.id],
                recent_events=civ.historical_events,
                military_strength=5 + int(civ.culture.militarism / 20),  # 5-10
                economic_strength=5 + int(civ_data['economic_system'].prosperity_index / 2),  # 5-10
                decision_type=scenario['type'],
                decision_prompt=scenario['prompt']
            )

            # Líder pren decisió
            decision = leader_ai.make_decision(context)

            print(f"💭 Decisió de {leader.name}:")
            print(f"   Acció: {decision.action}")
            print(f"   Raonament: {decision.reasoning}")
            print(f"   Resultat Esperat: {decision.expected_outcome}")
            print(f"   Nivell de Risc: {decision.risk_level}/10")
            print(f"   Confiança: {decision.confidence}/10")

    print()
    print("=" * 80)
    print("Test completat!")
    print()
    print("Observacions:")
    print("  - Líders amb alta agressivitat tendeixen a decisions militars")
    print("  - Líders pragmàtics prenen decisions racionals i calculades")
    print("  - Líders religiosos basen decisions en la fe i doctrina")
    print("  - Personalitat + cultura + sistemes emergents = decisions úniques")
    print()
    print("Pròxims passos:")
    print("  - Afegir líders a la classe Civilization")
    print("  - Implementar simulació temporal amb decisions periòdiques")
    print("  - Històric de decisions i conseqüències")
    print("  - Sistema de guerra i conflictes basats en decisions de líders")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
