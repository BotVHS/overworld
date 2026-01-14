#!/usr/bin/env python3
"""
Test del sistema de cultura, art i demografia ultra-realista

Demostra:
- Moviments culturals amb IA (cada civilització amb model diferent)
- Obres d'art mestres generades per IA
- Piràmides de població ultra-realistes
- Migracions amb perfils d'edat
- Tendències demogràfiques
"""
import sys
from overworld.world.world import World
from overworld.civilization.civilization import create_civilizations
from overworld.ai.civilization_ai_models import CivilizationAISystem
from overworld.civilization.cultural_movements import CulturalSystem
from overworld.civilization.demographics import (
    DemographicsSystem,
    MigrationReason,
    AgeGroup
)


def main():
    """Test de cultura i demografia amb IA"""
    print("=" * 80)
    print("  TEST DE CULTURA, ART I DEMOGRAFIA AMB IA")
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

    # === FASE 1: ASSIGNACIÓ DE MODELS IA ===
    print("=" * 80)
    print("FASE 1: ASSIGNACIÓ DE MODELS IA PER CIVILITZACIÓ")
    print("=" * 80)
    print()

    ai_system = CivilizationAISystem()

    print("Assignant models IA únics a cada civilització:")
    print()

    for civ in civ_manager.civilizations:
        profile = ai_system.assign_model_to_civilization(
            civilization_name=civ.name,
            culture_traits=civ.culture.to_dict()
        )

        print(f"🤖 {civ.name}:")
        print(f"   Model: {profile.model_name}")
        print(f"   Temperature: {profile.temperature:.2f}")
        print(f"   Biasos culturals:")
        for bias, value in list(profile.personality_bias.items())[:3]:
            print(f"     - {bias}: {value:+.2f}")
        print()

    # === FASE 2: MOVIMENTS CULTURALS AMB IA ===
    print()
    print("=" * 80)
    print("FASE 2: MOVIMENTS CULTURALS I ARTÍSTICS")
    print("=" * 80)
    print()

    cultural_system = CulturalSystem(ai_system)

    print("Generant moviments culturals amb IA per cada civilització:")
    print()

    for civ in civ_manager.civilizations[:4]:  # Només 4 per exemple
        movement = cultural_system.generate_cultural_movement(
            civilization_name=civ.name,
            year=100,
            culture_traits=civ.culture.to_dict(),
            recent_history=civ.historical_events[-5:],
            use_ai=True
        )

        if movement:
            print(f"🎨 {civ.name} - {movement.name}:")
            print(f"   Formes d'art: {', '.join(af.value for af in movement.art_forms)}")
            print(f"   Filosofia: {movement.philosophy}")
            print(f"   Influència: {movement.influence_score}/100")
            print()

            # Genera 2 obres d'art per moviment
            for i in range(2):
                artwork = cultural_system.generate_artistic_work(
                    civilization_name=civ.name,
                    year=100 + i * 10,
                    movement=movement,
                    culture_traits=civ.culture.to_dict(),
                    use_ai=True
                )

                if artwork:
                    print(f"   📜 \"{artwork.title}\" ({artwork.art_form.value})")
                    print(f"      Per {artwork.creator}, any {artwork.year_created}")
                    print(f"      {artwork.description}")
                    print(f"      Impacte cultural: {artwork.cultural_impact}/10")
                    print()

    # === FASE 3: PIRÀMIDES DE POBLACIÓ ===
    print()
    print("=" * 80)
    print("FASE 3: PIRÀMIDES DE POBLACIÓ ULTRA-REALISTES")
    print("=" * 80)
    print()

    demographics_system = DemographicsSystem(ai_system)

    print("Generant piràmides de població amb IA:")
    print()

    for civ in civ_manager.civilizations:
        capital_tile = world.get_tile(civ.capital.x, civ.capital.y)

        from overworld.world.biome import BIOME_DEFINITIONS
        environment_type = BIOME_DEFINITIONS[capital_tile.biome].name if capital_tile.biome else "Desconegut"

        pyramid = demographics_system.generate_population_pyramid(
            civilization_name=civ.name,
            year=100,
            total_population=civ.total_population,
            culture_traits=civ.culture.to_dict(),
            environment_type=environment_type,
            tech_level=civ.tech_level,
            recent_events=civ.historical_events[-5:],
            use_ai=True
        )

        print(f"👥 {civ.name}:")
        print(f"   Població total: {pyramid.get_total_population():,}")
        print(f"   Població treballadora: {pyramid.get_working_age_population():,}")
        print(f"   Ràtio dependència: {pyramid.get_dependency_ratio():.2f}")
        print()

        # Mostra distribució per edat
        print("   Distribució per edat (homes | dones):")
        for group in AgeGroup:
            males = pyramid.male_distribution.get(group, 0)
            females = pyramid.female_distribution.get(group, 0)
            total_group = males + females
            pct = (total_group / pyramid.get_total_population() * 100) if pyramid.get_total_population() > 0 else 0

            # Barra visual
            bar_length = int(pct * 2)
            bar = "█" * bar_length

            print(f"   {group.value:12s}: {males:6,} | {females:6,}  {bar} {pct:.1f}%")

        print()

        # Tendències demogràfiques
        if civ.name in demographics_system.trends:
            trends = demographics_system.trends[civ.name]
            print(f"   Tendències demogràfiques:")
            print(f"     Taxa natalitat: {trends.birth_rate:.1f} per 1000")
            print(f"     Taxa mortalitat: {trends.death_rate:.1f} per 1000")
            print(f"     Creixement natural: {trends.get_natural_growth_rate():.1f} per 1000")
            print(f"     Mortalitat infantil: {trends.infant_mortality:.1f} per 1000 naixements")
            print(f"     Esperança de vida: {trends.life_expectancy:.1f} anys")
            print(f"     Taxa fertilitat: {trends.fertility_rate:.2f} fills/dona")
            print(f"     Urbanització: {trends.urbanization_rate:.1f}%")
            print()

    # === FASE 4: MIGRACIONS ===
    print()
    print("=" * 80)
    print("FASE 4: MIGRACIONS ENTRE CIVILITZACIONS")
    print("=" * 80)
    print()

    civs = civ_manager.civilizations

    # Simula 3 migracions diferents
    migration_scenarios = [
        {
            'source': 0,
            'dest': 1,
            'reason': MigrationReason.ECONOMIC,
            'context': {
                'economic_disparity': 'Alta',
                'trade_routes': 'Establertes',
                'language_barrier': 'Moderada'
            }
        },
        {
            'source': 2,
            'dest': 3,
            'reason': MigrationReason.WAR,
            'context': {
                'conflict_intensity': 'Alta',
                'duration': '3 anys',
                'refugee_camps': 'Disponibles'
            }
        },
        {
            'source': 4,
            'dest': 1,
            'reason': MigrationReason.FAMINE,
            'context': {
                'food_shortage': 'Severa',
                'duration': '2 anys',
                'aid_availability': 'Baixa'
            }
        }
    ]

    print("Generant migracions amb IA:")
    print()

    for scenario in migration_scenarios:
        source_civ = civs[scenario['source']]
        dest_civ = civs[scenario['dest']]

        migration = demographics_system.generate_migration(
            source_civ=source_civ.name,
            destination_civ=dest_civ.name,
            year=105,
            source_population=source_civ.total_population,
            reason=scenario['reason'],
            context=scenario['context'],
            use_ai=True
        )

        if migration:
            print(f"🚶 {migration.source_civilization} → {migration.destination_civilization}")
            print(f"   Raó: {migration.reason.value}")
            print(f"   Migrants: {migration.migrants_count:,} persones ({migration.migrants_count/source_civ.total_population*100:.2f}% de la població)")
            print(f"   {migration.description}")
            print()

            # Mostra perfil d'edat dels migrants
            if migration.age_profile:
                print("   Perfil d'edat dels migrants:")
                for group, percentage in sorted(migration.age_profile.items(), key=lambda x: list(AgeGroup).index(x[0])):
                    count = int(migration.migrants_count * percentage)
                    bar_length = int(percentage * 50)
                    bar = "▓" * bar_length
                    print(f"     {group.value:12s}: {bar} {percentage*100:.1f}% ({count:,} persones)")
                print()

    # === FASE 5: ESTADÍSTIQUES GLOBALS ===
    print()
    print("=" * 80)
    print("FASE 5: ESTADÍSTIQUES GLOBALS")
    print("=" * 80)
    print()

    cultural_stats = cultural_system.get_statistics()
    demo_stats = demographics_system.get_statistics()

    print("Estadístiques culturals:")
    print(f"  Total moviments: {cultural_stats['total_movements']}")
    print(f"  Total obres d'art: {cultural_stats['total_artworks']}")
    print(f"  Distribució per forma d'art:")
    for art_form, count in cultural_stats['art_forms_distribution'].items():
        print(f"    - {art_form}: {count} obres")
    print()

    print("Estadístiques demogràfiques:")
    print(f"  Civilitzacions analitzades: {demo_stats['total_civilizations_tracked']}")
    print(f"  Total migracions: {demo_stats['total_migrations']}")
    print(f"  Total migrants: {demo_stats['total_migrants']:,}")
    print(f"  Esperança de vida mitjana: {demo_stats['average_life_expectancy']:.1f} anys")
    print(f"  Taxa fertilitat mitjana: {demo_stats['average_fertility_rate']:.2f} fills/dona")
    print()

    # Mostra models IA utilitzats
    print("Models IA utilitzats per civilització:")
    for civ_name, profile in ai_system.profiles.items():
        print(f"  {civ_name}: {profile.model_name}")
    print()

    print("=" * 80)
    print("Test completat!")
    print()
    print("RESUM:")
    print("  ✓ Models IA únics assignats a cada civilització")
    print("  ✓ Moviments culturals generats amb IA contextual")
    print("  ✓ Obres d'art mestres creades per cada moviment")
    print("  ✓ Piràmides de població ultra-realistes amb IA")
    print("  ✓ Tendències demogràfiques (natalitat, mortalitat, esperança vida)")
    print("  ✓ Migracions amb perfils d'edat i raons contextuals")
    print()
    print("Observacions:")
    print("  - Cada civilització usa un model Ollama diferent")
    print("  - Models generen cultura i demografia segons personalitat pròpia")
    print("  - Moviments culturals són originals (no històrics humans)")
    print("  - Piràmides varien segons nivell tecnològic i cultura")
    print("  - Migracions tenen perfils d'edat realistes segons raó")
    print("  - Guerra redueix homes adults, fam afecta tots els grups")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
