#!/usr/bin/env python3
"""
Visualitzador del món amb pygame

Genera un món i el mostra gràficament amb controls interactius.
"""
import sys
from overworld.world.world import World
from overworld.graphics.renderer import WorldRenderer
from overworld.core.time_manager import TimeManager


def main():
    """Genera un món i el visualitza"""
    print("=" * 80)
    print("  OVERWORLD - VISUALITZADOR")
    print("=" * 80)
    print()

    # Crea un món (ajusta la mida segons les teves necessitats)
    # Per a visualització, un món més petit és més ràpid
    print("Generant món 200x200...")
    world = World(width=200, height=200, seed=42)
    world.generate(island_mode=False, num_rivers=15)

    print()
    print("✓ Món generat correctament!")
    print()

    # Crea gestor de temps
    time_manager = TimeManager()

    # Crea renderer
    print("Iniciant visualitzador...")
    renderer = WorldRenderer(
        world=world,
        time_manager=time_manager,
        screen_width=1400,
        screen_height=900,
        tile_size=4  # Mida dels tiles (ajusta segons zoom desitjat)
    )

    print()
    print("=" * 80)
    print("CONTROLS:")
    print("-" * 80)
    print("  1-7      : Canvia entre capes (Biomes, Altitud, Temperatura, etc.)")
    print("  WASD     : Mou la càmera")
    print("  Fletxes  : Mou la càmera (alternativa)")
    print("  +/-      : Zoom in/out")
    print("  Clic     : Selecciona un tile (mostra informació)")
    print("  HOME     : Reset càmera i zoom")
    print("  ESC      : Tanca")
    print("=" * 80)
    print()
    print("Iniciant...")
    print()

    # Executa el bucle de renderització
    renderer.run(fps=60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
