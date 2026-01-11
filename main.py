#!/usr/bin/env python3
"""
Overworld - Simulació procedural completa d'un món

Punt d'entrada principal del programa
"""
import sys
from overworld.core.config import GameConfig, DEFAULT_CONFIG
from overworld.core.time_manager import TimeManager
from overworld.core.event_system import EventSystem, Event, EventType


def print_banner():
    """Mostra el banner del joc"""
    print("=" * 60)
    print("  OVERWORLD - Simulació Procedural de Món")
    print("  Versió 0.1.0 - En desenvolupament")
    print("=" * 60)
    print()


def test_core_systems():
    """Prova els sistemes bàsics"""
    print("Provant sistemes bàsics...")
    print()

    # Configuració
    config = DEFAULT_CONFIG
    print(f"✓ Configuració carregada")
    print(f"  - Mapa: {config.world.width}x{config.world.height}")
    print(f"  - Plaques tectòniques: {config.world.num_plates}")
    print(f"  - Model Ollama: {config.ollama.model}")
    print()

    # Gestor de temps
    time_manager = TimeManager(days_per_year=config.world.days_per_year)
    print(f"✓ Gestor de temps inicialitzat")
    print(f"  - {time_manager}")

    # Simula alguns dies
    time_manager.set_speed(10)
    ticks = time_manager.update(1.0)
    print(f"  - Després de 1s a 10x: {time_manager}")
    print()

    # Sistema d'esdeveniments
    event_system = EventSystem()
    print(f"✓ Sistema d'esdeveniments inicialitzat")

    # Subscriu un listener
    def on_city_founded(event: Event):
        print(f"  📢 {event}")

    event_system.subscribe(EventType.CITY_FOUNDED, on_city_founded)

    # Emet un esdeveniment de prova
    test_event = Event(
        event_type=EventType.CITY_FOUNDED,
        day=time_manager.time.day,
        year=time_manager.time.year,
        description="La ciutat de Provalàndia ha estat fundada!",
        data={"population": 100, "location": (250, 250)}
    )
    event_system.emit(test_event)
    print()

    print("=" * 60)
    print("Sistemes bàsics funcionant correctament!")
    print()
    print("Pròxims passos:")
    print("  1. Generació del món amb noise")
    print("  2. Renderitzat bàsic amb pygame")
    print("  3. Sistema climàtic")
    print("  4. Biologia i genètica")
    print("  5. Civilitzacions amb IA")
    print("=" * 60)


def main():
    """Funció principal"""
    print_banner()

    # De moment, només provem els sistemes bàsics
    test_core_systems()

    return 0


if __name__ == "__main__":
    sys.exit(main())
