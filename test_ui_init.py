#!/usr/bin/env python3
"""
Test d'inicialització de la UI

Verifica que la UI es pot inicialitzar correctament sense executar el bucle principal
"""
import sys
import os

# Desactiva display per test
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from overworld.world.world import World
from overworld.world.plate_tectonics import PlateTectonicsSystem
from overworld.world.climate_system import ClimateSystem
from overworld.civilization.civilization import create_civilizations
from overworld.ui.advanced_ui import AdvancedUI, ViewMode


def main():
    """Test d'inicialització de la UI"""
    print("=" * 80)
    print("  TEST D'INICIALITZACIÓ DE LA UI")
    print("=" * 80)
    print()

    # Genera món petit per test
    print("Generant món de test 100x100...")
    world = World(width=100, height=100, seed=42)
    world.generate(island_mode=False, num_rivers=5)
    print(f"  ✓ Món generat: {world.width}x{world.height}")
    print()

    # Tectònica
    print("Generant plaques tectòniques...")
    tectonics = PlateTectonicsSystem(world.width, world.height)
    tectonics.generate_plates(num_plates=6)
    tectonics.detect_boundaries()
    print(f"  ✓ {len(tectonics.plates)} plaques")
    print()

    # Clima
    print("Inicialitzant sistema climàtic...")
    climate = ClimateSystem(world.width, world.height)
    world_tiles_dict = {}
    for x in range(world.width):
        for y in range(world.height):
            tile = world.get_tile(x, y)
            if tile:
                world_tiles_dict[(x, y)] = tile
    climate.calculate_weather_patterns(world_tiles_dict)
    print(f"  ✓ Patrons meteorològics calculats")
    print()

    # Civilitzacions
    print("Creant civilitzacions...")
    civ_manager = create_civilizations(world, count=4)
    print(f"  ✓ {len(civ_manager.civilizations)} civilitzacions")
    print()

    # === TEST DE LA UI ===
    print("=" * 80)
    print("TEST: INICIALITZACIÓ DE LA UI")
    print("=" * 80)
    print()

    print("Creant interfície gràfica...")
    ui = AdvancedUI(screen_width=1200, screen_height=800)
    print("  ✓ UI creada")
    print()

    # Test de components
    print("Verificant components de la UI:")
    print(f"  Botons: {len(ui.buttons)}")
    print(f"  Mode actual: {ui.current_view.value}")
    print(f"  Panell d'informació: {ui.info_panel.title}")
    print(f"  Panell d'estadístiques: {ui.stats_panel.title}")
    print()

    # Carrega món
    print("Carregant dades del món a la UI...")
    ui.load_world(
        world=world,
        civilizations=civ_manager,
        tectonics=tectonics,
        climate=climate
    )
    print("  ✓ Món carregat")
    print()

    # Test de canvi de modes
    print("Testant canvi de modes de visualització:")
    test_modes = [
        ViewMode.TERRAIN,
        ViewMode.BIOMES,
        ViewMode.CIVILIZATIONS,
        ViewMode.TECTONICS,
        ViewMode.CLIMATE,
        ViewMode.TEMPERATURE
    ]

    for mode in test_modes:
        ui.set_view_mode(mode)
        ui._generate_map_surface()
        print(f"  ✓ Mode {mode.value}: Mapa generat ({ui.map_surface.get_width()}x{ui.map_surface.get_height()} px)")

    print()

    # Test d'informació de tile
    print("Testant panell d'informació:")
    test_tiles = [(20, 20), (50, 50), (80, 80)]

    for x, y in test_tiles:
        ui.update_info_panel(x, y)
        print(f"  ✓ Tile ({x}, {y}): {len(ui.info_panel.lines)} línies d'informació")

    print()

    # Test de botons
    print("Testant callbacks de botons:")
    ui.reset_time()
    print(f"  ✓ Reset time: Any = {ui.current_year}")

    ui.advance_years(50)
    print(f"  ✓ Avança 50 anys: Any = {ui.current_year}")

    ui.toggle_play()
    print(f"  ✓ Toggle play: is_playing = {ui.is_playing}")

    print()

    # Estadístiques finals
    print("=" * 80)
    print("TEST COMPLETAT AMB ÈXIT!")
    print("=" * 80)
    print()

    print("Components verificats:")
    print(f"  ✓ Món: {world.width}x{world.height} tiles")
    print(f"  ✓ Plaques tectòniques: {len(tectonics.plates)}")
    print(f"  ✓ Sistema climàtic: {len(climate.weather_patterns)} patrons")
    print(f"  ✓ Civilitzacions: {len(civ_manager.civilizations)}")
    print(f"  ✓ UI botons: {len(ui.buttons)}")
    print(f"  ✓ Modes de visualització: {len(test_modes)} testats")
    print()

    print("La UI està llesta per usar!")
    print("Executa 'python3 main_ui.py' per llançar la interfície completa.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
