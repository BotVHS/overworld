#!/usr/bin/env python3
"""
Test del sistema d'esdeveniments

Simula anys amb esdeveniments emergents i història dinàmica
"""
import sys
from overworld.world.world import World
from overworld.civilization.civilization import create_civilizations
from overworld.core.event_system import AdvancedEventSystem, EventType, EventPriority


def main():
    """Test del sistema d'esdeveniments"""
    print("=" * 80)
    print("  TEST DEL SISTEMA D'ESDEVENIMENTS EMERGENTS")
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

    # Crea sistema d'esdeveniments
    print("=" * 80)
    print("SIMULANT 20 ANYS AMB ESDEVENIMENTS EMERGENTS")
    print("=" * 80)
    print()

    event_system = AdvancedEventSystem()

    # Subscriu listener per esdeveniments crítics
    def on_critical_event(event):
        print(f"⚠️  ESDEVENIMENT CRÍTIC: {event.title}")

    event_system.subscribe(EventType.FAMINE, on_critical_event)
    event_system.subscribe(EventType.NATURAL_DISASTER, on_critical_event)

    # Simula 20 anys
    for year in range(1, 21):
        print(f"\n{'─' * 80}")
        print(f"ANY {year}")
        print(f"{'─' * 80}")

        # Simula un any complet
        year_events = event_system.simulate_year(
            year=year,
            civilizations=civ_manager.civilizations,
            context={'world': world}
        )

        if year_events:
            print(f"\n🎲 {len(year_events)} esdeveniments aquest any:")
            for event in year_events:
                priority_icon = {
                    EventPriority.LOW: "ℹ️",
                    EventPriority.MEDIUM: "📌",
                    EventPriority.HIGH: "⚡",
                    EventPriority.CRITICAL: "🔴"
                }.get(event.priority, "•")

                print(f"\n  {priority_icon} {event.title}")
                print(f"      {event.description}")
                print(f"      Afecta: {', '.join(event.affected_civilizations)}")
                if event.consequences:
                    print(f"      Conseqüències: {event.consequences}")
        else:
            print("\n  Cap esdeveniment destacable aquest any")

    # Mostra estadístiques globals
    print()
    print("=" * 80)
    print("RESUM D'HISTÒRIA (20 ANYS)")
    print("=" * 80)
    print()

    stats = event_system.get_statistics()

    print(f"Total d'esdeveniments: {stats['total_events']}")
    print()

    print("Per tipus:")
    for event_type, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {event_type}: {count}")
    print()

    print("Per prioritat:")
    for priority, count in sorted(stats['by_priority'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {priority}: {count}")
    print()

    # Mostra història per civilització
    print("=" * 80)
    print("HISTÒRIA PER CIVILITZACIÓ")
    print("=" * 80)

    for civ in civ_manager.civilizations:
        print(f"\n📜 {civ.name}:")
        print(f"{'─' * 80}")

        civ_events = event_system.get_history(civilization_name=civ.name, limit=10)

        if civ_events:
            for event in civ_events:
                priority_icon = {
                    EventPriority.LOW: "ℹ️",
                    EventPriority.MEDIUM: "📌",
                    EventPriority.HIGH: "⚡",
                    EventPriority.CRITICAL: "🔴"
                }.get(event.priority, "•")

                print(f"  {priority_icon} Any {event.year}: {event.title}")
                print(f"      {event.description}")
        else:
            print("  Sense esdeveniments registrats")

    print()
    print("=" * 80)
    print("Test completat!")
    print()
    print("Observacions:")
    print("  - Esdeveniments emergents aleatoris cada any")
    print("  - Probabilitats realistes (bones collites 15%, desastres 5%, etc.)")
    print("  - Història dinàmica registrada per civilització")
    print("  - Prioritats diferenciades (LOW, MEDIUM, HIGH, CRITICAL)")
    print("  - Conseqüències quantificables per esdeveniments")
    print()
    print("Pròxims passos:")
    print("  - Aplicar conseqüències a les civilitzacions")
    print("  - Decisions de líders basades en esdeveniments")
    print("  - Esdeveniments diplomàtics (guerres, aliances)")
    print("  - Esdeveniments tecnològics i culturals")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
