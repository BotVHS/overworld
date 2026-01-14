#!/usr/bin/env python3
"""
Main UI - Script principal amb interfície gràfica avançada

Inicialitza el món complet amb totes les funcionalitats:
- Món procedural
- Tectònica de plaques
- Sistema climàtic
- Civilitzacions amb IA
- Interfície gràfica completa
"""
import sys
from overworld.world.world import World
from overworld.world.plate_tectonics import PlateTectonicsSystem
from overworld.world.climate_system import ClimateSystem
from overworld.civilization.civilization import create_civilizations
from overworld.ai.civilization_ai_models import CivilizationAISystem
from overworld.civilization.cultural_movements import CulturalSystem
from overworld.civilization.demographics import DemographicsSystem
from overworld.civilization.diplomacy import DiplomacySystem
from overworld.civilization.warfare import WarfareSystem
from overworld.ui.advanced_ui import AdvancedUI, ViewMode


def main():
    """Inicialitza el món i llança la UI"""
    print("=" * 80)
    print("  OVERWORLD - ADVANCED SIMULATION")
    print("=" * 80)
    print()

    # === FASE 1: GENERACIÓ DEL MÓN ===
    print("=" * 80)
    print("FASE 1: GENERACIÓ DEL MÓN")
    print("=" * 80)
    print()

    world_size = 300  # Món de 300x300
    print(f"Generant món {world_size}x{world_size}...")
    world = World(width=world_size, height=world_size, seed=42)
    world.generate(island_mode=False, num_rivers=20)
    print()

    # === FASE 2: TECTÒNICA DE PLAQUES ===
    print("=" * 80)
    print("FASE 2: TECTÒNICA DE PLAQUES")
    print("=" * 80)
    print()

    tectonics = PlateTectonicsSystem(world.width, world.height)
    tectonics.generate_plates(num_plates=12)
    print()

    tectonics.detect_boundaries()
    print()

    # Simula esdeveniments geològics inicials
    print("Simulant esdeveniments geològics inicials...")
    world_tiles_dict = {}
    for x in range(world.width):
        for y in range(world.height):
            tile = world.get_tile(x, y)
            if tile:
                world_tiles_dict[(x, y)] = tile

    initial_events = tectonics.simulate_geological_events(year=0, world_tiles=world_tiles_dict)
    print(f"  ✓ {len(initial_events)} esdeveniments geològics")
    print()

    # === FASE 3: SISTEMA CLIMÀTIC ===
    print("=" * 80)
    print("FASE 3: SISTEMA CLIMÀTIC")
    print("=" * 80)
    print()

    climate = ClimateSystem(world.width, world.height)
    print("Calculant patrons meteorològics inicials...")
    climate.calculate_weather_patterns(world_tiles_dict)
    print("Simulant cicle de l'aigua...")
    climate.simulate_water_cycle(world_tiles_dict)

    stats = climate.get_statistics()
    print(f"  ✓ Temperatura mitjana: {stats['average_temperature']:.1f}°C")
    print(f"  ✓ {len(stats['climate_distribution'])} zones climàtiques diferents")
    print()

    # === FASE 4: CIVILITZACIONS ===
    print("=" * 80)
    print("FASE 4: CIVILITZACIONS AMB IA")
    print("=" * 80)
    print()

    print("Creant civilitzacions...")
    civ_manager = create_civilizations(world, count=8)
    print()

    # Sistema IA per civilitzacions
    ai_system = CivilizationAISystem()

    # Assigna models IA
    print("Assignant models IA únics per civilització:")
    for civ in civ_manager.civilizations:
        profile = ai_system.assign_model_to_civilization(
            civilization_name=civ.name,
            culture_traits=civ.culture.to_dict()
        )
        print(f"  {civ.name}: {profile.model_name} (temp: {profile.temperature:.2f})")
    print()

    # === FASE 5: SISTEMES SOCIALS ===
    print("=" * 80)
    print("FASE 5: SISTEMES SOCIALS")
    print("=" * 80)
    print()

    # Cultura
    print("Inicialitzant sistema cultural...")
    cultural_system = CulturalSystem(ai_system)

    # Genera alguns moviments culturals
    for civ in civ_manager.civilizations[:3]:
        movement = cultural_system.generate_cultural_movement(
            civilization_name=civ.name,
            year=0,
            culture_traits=civ.culture.to_dict(),
            recent_history=civ.historical_events,
            use_ai=False  # Procedural per velocitat
        )
        if movement:
            print(f"  {civ.name}: {movement.name}")
    print()

    # Demografia
    print("Inicialitzant sistema demogràfic...")
    demographics_system = DemographicsSystem(ai_system)

    # Genera piràmides de població
    for civ in civ_manager.civilizations[:3]:
        capital_tile = world.get_tile(civ.capital.x, civ.capital.y)
        from overworld.world.biome import BIOME_DEFINITIONS
        environment_type = BIOME_DEFINITIONS[capital_tile.biome].name if capital_tile.biome else "Desconegut"

        pyramid = demographics_system.generate_population_pyramid(
            civilization_name=civ.name,
            year=0,
            total_population=civ.total_population,
            culture_traits=civ.culture.to_dict(),
            environment_type=environment_type,
            tech_level=civ.tech_level,
            recent_events=civ.historical_events,
            use_ai=False
        )
        print(f"  {civ.name}: {pyramid.get_total_population():,} habitants")
    print()

    # Diplomàcia i guerra
    print("Inicialitzant diplomàcia i guerra...")
    diplomacy = DiplomacySystem()
    warfare = WarfareSystem(diplomacy)

    # Estableix relacions inicials
    for i, civ1 in enumerate(civ_manager.civilizations):
        for civ2 in civ_manager.civilizations[i+1:]:
            # Relacions neutrals per defecte
            from overworld.civilization.diplomacy import RelationshipType
            diplomacy.set_relationship(civ1.name, civ2.name, RelationshipType.NEUTRAL, 0)

        # Registra força militar
        warfare.register_military_force(
            civilization_name=civ1.name,
            soldiers=500 + int(civ1.culture.militarism * 5),
            tech_level=civ1.tech_level,
            morale=50 + int(civ1.culture.militarism / 4),
            experience=0
        )

    print(f"  ✓ {len(diplomacy.relationships)} relacions diplomàtiques")
    print(f"  ✓ {len(warfare.military_forces)} forces militars")
    print()

    # === FASE 6: ESTADÍSTIQUES INICIALS ===
    print("=" * 80)
    print("FASE 6: ESTADÍSTIQUES INICIALS")
    print("=" * 80)
    print()

    tec_stats = tectonics.get_statistics()
    print("Tectònica:")
    print(f"  Plaques: {tec_stats['total_plates']} ({tec_stats['plate_types'].get('oceanic', 0)} oceàniques, "
          f"{tec_stats['plate_types'].get('continental', 0)} continentals)")
    print(f"  Límits: {tec_stats['total_boundaries']}")
    print(f"  Esdeveniments: {tec_stats['total_geological_events']}")
    print()

    clim_stats = climate.get_statistics()
    print("Clima:")
    print(f"  Temperatura mitjana: {clim_stats['average_temperature']:.1f}°C")
    print(f"  Precipitació mitjana: {clim_stats['average_precipitation']:.1f} mm/mes")
    print(f"  Zones climàtiques: {len(clim_stats['climate_distribution'])}")
    print()

    print("Civilitzacions:")
    print(f"  Total: {len(civ_manager.civilizations)}")
    print(f"  Població total: {sum(c.total_population for c in civ_manager.civilizations):,}")
    print(f"  Ciutats totals: {sum(len(c.cities) for c in civ_manager.civilizations)}")
    print()

    # === FASE 7: LLANÇAR UI ===
    print("=" * 80)
    print("FASE 7: LLANÇAMENT DE LA INTERFÍCIE GRÀFICA")
    print("=" * 80)
    print()

    print("Inicialitzant interfície gràfica avançada...")
    ui = AdvancedUI(screen_width=1600, screen_height=900)

    # Carrega dades del món
    ui.load_world(
        world=world,
        civilizations=civ_manager,
        tectonics=tectonics,
        climate=climate
    )

    # Actualitza estadístiques
    ui.stats_panel.lines = [
        f"Any: 0",
        "",
        f"Món: {world.width}x{world.height}",
        f"Tiles: {world.width * world.height:,}",
        "",
        f"Civilitzacions: {len(civ_manager.civilizations)}",
        f"Població: {sum(c.total_population for c in civ_manager.civilizations):,}",
        "",
        f"Plaques: {tec_stats['total_plates']}",
        f"Temp mitjana: {clim_stats['average_temperature']:.1f}°C",
    ]

    print()
    print("=" * 80)
    print("🖥️  INTERFÍCIE GRÀFICA INICIADA")
    print("=" * 80)
    print()
    print("CONTROLS:")
    print("  🖱️  Click         - Selecciona tile i mostra informació detallada")
    print("  ⌨️  WASD/Fletxes  - Mou la càmera pel món")
    print("  ⌨️  Espai         - Play/Pause simulació temporal")
    print("  ⌨️  +/-           - Avança/retrocedeix 10 anys")
    print("  ⌨️  1-5           - Canvia mode de visualització:")
    print("     1: Terreny (altitud)")
    print("     2: Biomes")
    print("     3: Civilitzacions")
    print("     4: Tectònica de plaques")
    print("     5: Clima (Köppen)")
    print("  ⌨️  ESC           - Tanca aplicació")
    print()
    print("MODES DE VISUALITZACIÓ:")
    print("  🗺️  Terreny      - Mapa d'altitud amb colors")
    print("  🌳 Biomes       - Distribució de biomes i ecosistemes")
    print("  🏛️  Civs         - Territoris i ciutats de civilitzacions")
    print("  ⚖️  Política     - Sistemes polítics i govern")
    print("  🕊️  Religió      - Sistemes religiosos i creences")
    print("  💰 Economia     - Sistemes econòmics i recursos")
    print("  👥 Demografia   - Densitat de població i piràmides")
    print("  🎨 Cultura      - Moviments culturals i art")
    print("  🤝 Diplomàcia   - Relacions, aliances i guerres")
    print("  🌋 Plaques      - Plaques tectòniques i límits")
    print("  🌡️  Clima        - Classificació climàtica Köppen")
    print("  🗣️  Llengües     - Famílies lingüístiques")
    print()
    print("PANELLS:")
    print("  📋 Panell esquerre - Informació detallada del tile seleccionat")
    print("  📊 Panell dret     - Estadístiques globals")
    print("  🗺️  Mini-mapa       - Vista general del món")
    print("  ⏱️  Timeline        - Control temporal i any actual")
    print()
    print("=" * 80)
    print()

    # Llança UI
    try:
        ui.run(max_fps=60)
    except KeyboardInterrupt:
        print("\n⚠️  Interromput per l'usuari")

    print()
    print("=" * 80)
    print("Simulació finalitzada!")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
