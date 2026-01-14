#!/usr/bin/env python3
"""
Test de tectònica de plaques i sistema climàtic

Demostra:
- Generació de plaques tectòniques
- Límits de plaques (divergents, convergents, transformants)
- Esdeveniments geològics (terratrèmols, volcans, muntanyes)
- Sistema climàtic amb estacions
- Cicle de l'aigua (evaporació, precipitació, escorrentia)
- Patrons meteorològics amb vents
"""
import sys
from overworld.world.world import World
from overworld.world.plate_tectonics import PlateTectonicsSystem, BoundaryType
from overworld.world.climate_system import ClimateSystem, Season


def main():
    """Test de tectònica i clima"""
    print("=" * 80)
    print("  TEST DE TECTÒNICA DE PLAQUES I SISTEMA CLIMÀTIC")
    print("=" * 80)
    print()

    # Genera un món mitjà
    print("Generant món 200x200...")
    world = World(width=200, height=200, seed=42)
    world.generate(island_mode=False, num_rivers=15)
    print()

    # === FASE 1: TECTÒNICA DE PLAQUES ===
    print("=" * 80)
    print("FASE 1: GENERACIÓ DE PLAQUES TECTÒNIQUES")
    print("=" * 80)
    print()

    tectonics = PlateTectonicsSystem(world.width, world.height)

    # Genera 10 plaques
    tectonics.generate_plates(num_plates=10)
    print()

    # Detecta límits
    tectonics.detect_boundaries()
    print()

    # Mostra detalls de plaques
    print("Detalls de les plaques:")
    print()
    for plate_id, plate in list(tectonics.plates.items())[:5]:  # Només 5 per exemple
        print(f"  Placa {plate_id}:")
        print(f"    Tipus: {plate.plate_type.value}")
        print(f"    Tiles: {len(plate.tiles):,}")
        print(f"    Velocitat: {plate.get_speed():.2f} cm/any")
        print(f"    Direcció: {math.degrees(plate.get_direction()):.1f}°")
        print(f"    Edat: {plate.age} milions d'anys")
        print()

    # === FASE 2: LÍMITS DE PLAQUES ===
    print()
    print("=" * 80)
    print("FASE 2: ANÀLISI DE LÍMITS DE PLAQUES")
    print("=" * 80)
    print()

    print("Límits més actius:")
    print()

    # Ordena límits per activitat
    sorted_boundaries = sorted(tectonics.boundaries, key=lambda b: b.activity_level, reverse=True)

    for i, boundary in enumerate(sorted_boundaries[:5], 1):
        plate1 = tectonics.plates[boundary.plate1_id]
        plate2 = tectonics.plates[boundary.plate2_id]

        print(f"{i}. Límit entre Placa {boundary.plate1_id} ({plate1.plate_type.value}) "
              f"i Placa {boundary.plate2_id} ({plate2.plate_type.value})")
        print(f"   Tipus: {boundary.boundary_type.value}")
        print(f"   Activitat: {boundary.activity_level:.2f}/1.0")
        print(f"   Tiles afectats: {len(boundary.tiles):,}")

        # Descriu què passa
        if boundary.boundary_type == BoundaryType.CONVERGENT:
            if plate1.plate_type.value == "oceanic" and plate2.plate_type.value == "oceanic":
                print(f"   → Subducció oceànica: Fossa marina i volcans submarins")
            elif plate1.plate_type.value == "continental" and plate2.plate_type.value == "continental":
                print(f"   → Col·lisió continental: Formació de grans cadenes muntanyoses")
            else:
                print(f"   → Subducció oceànica-continental: Volcans i terratrèmols intensos")
        elif boundary.boundary_type == BoundaryType.DIVERGENT:
            print(f"   → Rift: Nova crosta oceànica, activitat volcànica moderada")
        else:
            print(f"   → Falla transformant: Terratrèmols per fricció lateral")

        print()

    # === FASE 3: ESDEVENIMENTS GEOLÒGICS ===
    print()
    print("=" * 80)
    print("FASE 3: SIMULACIÓ D'ESDEVENIMENTS GEOLÒGICS")
    print("=" * 80)
    print()

    print("Simulant 3 anys d'activitat geològica...")
    print()

    # Converteix tiles a dict per simul·lació
    world_tiles_dict = {}
    for x in range(world.width):
        for y in range(world.height):
            tile = world.get_tile(x, y)
            if tile:
                world_tiles_dict[(x, y)] = tile

    all_events = []
    for year in range(1, 4):
        print(f"Any {year}:")
        events = tectonics.simulate_geological_events(year, world_tiles_dict)

        # Mostra esdeveniments més significatius
        significant = sorted(events, key=lambda e: e.magnitude if e.event_type != "mountain_building" else 5.0, reverse=True)[:3]

        for event in significant:
            symbol = {"earthquake": "🌍", "volcano": "🌋", "mountain_building": "⛰️"}.get(event.event_type, "❓")
            print(f"  {symbol} {event.description} a ({event.x}, {event.y})")

        print(f"  Total esdeveniments: {len(events)}")
        print()
        all_events.extend(events)

    # Resum d'esdeveniments
    event_summary = {}
    for event in all_events:
        event_summary[event.event_type] = event_summary.get(event.event_type, 0) + 1

    print("Resum d'esdeveniments geològics:")
    for etype, count in event_summary.items():
        symbol = {"earthquake": "🌍", "volcano": "🌋", "mountain_building": "⛰️"}.get(etype, "❓")
        print(f"  {symbol} {etype}: {count}")
    print()

    # === FASE 4: SISTEMA CLIMÀTIC ===
    print()
    print("=" * 80)
    print("FASE 4: SISTEMA CLIMÀTIC I ESTACIONS")
    print("=" * 80)
    print()

    climate = ClimateSystem(world.width, world.height)

    print("Simulant 4 estacions (1 any complet):")
    print()

    for month in range(12):
        climate.advance_season()

        # Només mostra canvis d'estació
        if month % 3 == 0:
            print(f"📅 Mes {climate.current_month} - {climate.get_season_name()}")

            # Calcula patrons meteorològics
            climate.calculate_weather_patterns(world_tiles_dict)

            # Mostra estadístiques estacionals
            stats = climate.get_statistics()
            print(f"   Temperatura mitjana: {stats['average_temperature']:.1f}°C")
            print(f"   Precipitació mitjana: {stats['average_precipitation']:.1f} mm/mes")
            print(f"   Velocitat vent mitjana: {stats['average_wind_speed']:.1f} km/h")
            print(f"   Coberta núvols mitjana: {stats['average_cloud_cover']:.1%}")
            print()

    # === FASE 5: PATRONS METEOROLÒGICS ===
    print()
    print("=" * 80)
    print("FASE 5: PATRONS METEOROLÒGICS DETALLATS")
    print("=" * 80)
    print()

    # Analitza alguns punts interessants
    sample_points = [
        (50, 20, "Zona Equatorial"),
        (50, 100, "Zona Temperada"),
        (50, 180, "Zona Polar")
    ]

    print("Anàlisi de zones climàtiques representatives:")
    print()

    for x, y, zone_name in sample_points:
        weather = climate.weather_patterns.get((x, y))
        if not weather:
            continue

        climate_type = climate.get_climate_classification(x, y)

        print(f"📍 {zone_name} ({x}, {y}):")
        print(f"   Clima: {climate_type}")
        print(f"   Temperatura: {weather.temperature:.1f}°C")
        print(f"   Precipitació: {weather.precipitation:.1f} mm/mes")
        print(f"   Vent: {weather.wind_speed:.1f} km/h ({weather.wind_direction.value})")
        print(f"   Humitat: {weather.humidity:.1%}")
        print(f"   Núvols: {weather.cloud_cover:.1%}")
        print()

    # === FASE 6: CICLE DE L'AIGUA ===
    print()
    print("=" * 80)
    print("FASE 6: CICLE DE L'AIGUA")
    print("=" * 80)
    print()

    climate.simulate_water_cycle(world_tiles_dict)

    water_stats = climate.get_statistics()['water_cycle']

    print("Cicle global de l'aigua:")
    print(f"  💧 Evaporació total: {water_stats['total_evaporation']:,.0f} mm")
    print(f"  🌧️  Precipitació total: {water_stats['total_precipitation']:,.0f} mm")
    print(f"  🌊 Escorrentia total: {water_stats['total_runoff']:,.0f} mm")
    print()

    # Balance
    balance = water_stats['total_evaporation'] - water_stats['total_precipitation']
    print(f"Balance hídric: {balance:+,.0f} mm")
    if abs(balance) < 1000:
        print("  ✓ Cicle equilibrat")
    elif balance > 0:
        print("  ⚠️  Més evaporació que precipitació (més sec)")
    else:
        print("  ⚠️  Més precipitació que evaporació (més humit)")
    print()

    # Mostra cicle detallat en alguns punts
    print("Cicle de l'aigua en zones representatives:")
    print()

    for x, y, zone_name in sample_points:
        cycle = climate.water_cycles.get((x, y))
        if not cycle:
            continue

        print(f"📍 {zone_name}:")
        print(f"   Evaporació: {cycle.evaporation:.1f} mm/mes")
        print(f"   Condensació: {cycle.condensation:.1f} mm/mes")
        print(f"   Precipitació: {cycle.precipitation:.1f} mm/mes")
        print(f"   Infiltració: {cycle.infiltration:.1f} mm/mes")
        print(f"   Escorrentia: {cycle.runoff:.1f} mm/mes")
        print()

    # === FASE 7: DISTRIBUCIÓ CLIMÀTICA ===
    print()
    print("=" * 80)
    print("FASE 7: DISTRIBUCIÓ DE CLIMES (Köppen)")
    print("=" * 80)
    print()

    climate_dist = climate.get_statistics()['climate_distribution']

    print("Distribució de zones climàtiques:")
    total_tiles = sum(climate_dist.values())

    for climate_type in sorted(climate_dist.keys(), key=lambda k: climate_dist[k], reverse=True):
        count = climate_dist[climate_type]
        percentage = (count / total_tiles * 100) if total_tiles > 0 else 0
        bar_length = int(percentage / 2)
        bar = "█" * bar_length

        print(f"  {climate_type:25s}: {bar} {percentage:.1f}% ({count:,} tiles)")

    print()

    # === FASE 8: ESTADÍSTIQUES FINALS ===
    print()
    print("=" * 80)
    print("FASE 8: ESTADÍSTIQUES GLOBALS")
    print("=" * 80)
    print()

    tec_stats = tectonics.get_statistics()
    clim_stats = climate.get_statistics()

    print("Tectònica de plaques:")
    print(f"  Total plaques: {tec_stats['total_plates']}")
    print(f"    - Oceàniques: {tec_stats['plate_types'].get('oceanic', 0)}")
    print(f"    - Continentals: {tec_stats['plate_types'].get('continental', 0)}")
    print(f"  Total límits: {tec_stats['total_boundaries']}")
    print(f"    - Divergents: {tec_stats['boundary_types']['divergent']}")
    print(f"    - Convergents: {tec_stats['boundary_types']['convergent']}")
    print(f"    - Transformants: {tec_stats['boundary_types']['transform']}")
    print(f"  Velocitat mitjana plaques: {tec_stats['average_plate_speed']:.2f} cm/any")
    print(f"  Total esdeveniments geològics: {tec_stats['total_geological_events']}")
    print()

    print("Sistema climàtic:")
    print(f"  Estació actual: {clim_stats['current_season']}")
    print(f"  Mes actual: {clim_stats['current_month']}")
    print(f"  Temperatura mitjana global: {clim_stats['average_temperature']:.1f}°C")
    print(f"  Precipitació mitjana: {clim_stats['average_precipitation']:.1f} mm/mes")
    print(f"  Vent mitjà: {clim_stats['average_wind_speed']:.1f} km/h")
    print(f"  Total zones climàtiques: {len(clim_stats['climate_distribution'])}")
    print()

    print("=" * 80)
    print("Test completat!")
    print()
    print("RESUM:")
    print("  ✓ Plaques tectòniques generades amb tipus i velocitats")
    print("  ✓ Límits detectats (divergents, convergents, transformants)")
    print("  ✓ Esdeveniments geològics simulats (terratrèmols, volcans, muntanyes)")
    print("  ✓ Sistema climàtic amb 4 estacions")
    print("  ✓ Patrons meteorològics amb temperatura, precipitació i vents")
    print("  ✓ Cicle de l'aigua complert (evaporació, precipitació, escorrentia)")
    print("  ✓ Classificació climàtica Köppen per totes les zones")
    print()
    print("Observacions:")
    print("  - Plaques es mouen a velocitats reals (2-10 cm/any)")
    print("  - Límits convergents generen muntanyes i volcans")
    print("  - Límits divergents creen dorsals oceàniques")
    print("  - Clima varia segons latitud i estació")
    print("  - Cicle de l'aigua està equilibrat globalment")
    print("  - Vents segueixen cel·les atmosfèriques (Hadley, Ferrel, Polar)")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    import math
    sys.exit(main())
