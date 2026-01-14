#!/usr/bin/env python3
"""
Test del sistema d'evolució lingüística avançat

Demostra:
- Generació contextual amb Ollama
- Préstecs lingüístics entre civilitzacions
- Evolució temporal
- Creació de llengües franca
- Globalització lingüística
"""
import sys
from overworld.world.world import World
from overworld.civilization.civilization import create_civilizations
from overworld.emergent_systems.political_systems import PoliticalSystemGenerator
from overworld.emergent_systems.religious_systems import ReligiousSystemGenerator
from overworld.emergent_systems.economic_systems import EconomicSystemGenerator
from overworld.civilization.language_evolution import (
    AdvancedLanguageGenerator,
    LanguageEvolutionSystem
)


def main():
    """Test d'evolució lingüística avançada"""
    print("=" * 80)
    print("  TEST D'EVOLUCIÓ LINGÜÍSTICA AVANÇADA AMB IA")
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

    # Generadors
    print("Inicialitzant generadors...")
    lang_generator = AdvancedLanguageGenerator(use_ollama=True)
    evolution_system = LanguageEvolutionSystem(use_ollama=True)
    political_gen = PoliticalSystemGenerator(use_ollama=True)
    religious_gen = ReligiousSystemGenerator(use_ollama=True)
    economic_gen = EconomicSystemGenerator(use_ollama=True)

    if lang_generator.ollama and lang_generator.ollama.available:
        print("✓ Ollama disponible - generació contextual amb IA")
    else:
        print("⚠ Ollama no disponible - generació procedural")
    print()

    # === FASE 1: GENERACIÓ CONTEXTUAL ===
    print("=" * 80)
    print("FASE 1: GENERACIÓ DE LLENGÜES AMB CONTEXT COMPLET")
    print("=" * 80)
    print()

    civilizations_data = []

    for i, civ in enumerate(civ_manager.civilizations, 1):
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
            recent_history=civ.historical_events
        )

        # Comprova si és costaner
        is_coastal = False
        neighbors = world.get_neighbors(civ.capital.x, civ.capital.y, radius=1)
        for neighbor in neighbors:
            if neighbor.is_water:
                is_coastal = True
                break

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

        # Genera llengua contextual
        print(f"🗣️  {civ.name} ({environment_type}):")

        language = lang_generator.generate_contextual_language(
            civilization_name=civ.name,
            culture_traits=civ.culture.to_dict(),
            environment_type=environment_type,
            political_system=political_system.to_dict(),
            religious_system=religious_system.to_dict(),
            economic_system=economic_system.to_dict(),
            history=civ.historical_events
        )

        language.speakers = civ.total_population

        print(f"   Llengua: {language.name}")
        print(f"   Família: {language.family}")
        print(f"   Fonemes: {len(language.phoneme_inventory.consonants)}C + {len(language.phoneme_inventory.vowels)}V")
        print(f"   Vocabulari: {len(language.vocabulary)} paraules")
        print(f"   Exemples: water={language.vocabulary.get('water', '?')}, king={language.vocabulary.get('king', '?')}")
        print()

        civilizations_data.append({
            'civilization': civ,
            'language': language,
            'capital_pos': (civ.capital.x, civ.capital.y)
        })

    # === FASE 2: PRÉSTECS LINGÜÍSTICS ===
    print()
    print("=" * 80)
    print("FASE 2: PRÉSTECS LINGÜÍSTICS ENTRE CIVILITZACIONS PROPERES")
    print("=" * 80)
    print()

    # Troba parelles de civilitzacions properes
    for i, data1 in enumerate(civilizations_data):
        for data2 in civilizations_data[i+1:]:
            # Calcula distància
            x1, y1 = data1['capital_pos']
            x2, y2 = data2['capital_pos']
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

            # Si són properes (<50 tiles), préstecs lingüístics
            if distance < 50:
                civ1_name = data1['civilization'].name
                civ2_name = data2['civilization'].name
                lang1 = data1['language']
                lang2 = data2['language']

                # Intensitat segons distància
                intensity = max(0.1, 1.0 - (distance / 50.0))

                print(f"📍 {civ1_name} ↔ {civ2_name} (distància: {distance:.0f} tiles)")
                print(f"   Intensitat de contacte: {intensity:.2f}")

                # Registra contacte
                evolution_system.register_contact(
                    civ1_name=civ1_name,
                    civ2_name=civ2_name,
                    intensity=intensity,
                    duration_years=50,
                    contact_type="trade"
                )

                # Aplica préstecs bidireccionals
                loans1to2 = evolution_system.apply_linguistic_borrowing(
                    language1=lang2,
                    language2=lang1,
                    civ1_name=civ2_name,
                    civ2_name=civ1_name,
                    year=100,
                    intensity=intensity
                )

                loans2to1 = evolution_system.apply_linguistic_borrowing(
                    language1=lang1,
                    language2=lang2,
                    civ1_name=civ1_name,
                    civ2_name=civ2_name,
                    year=100,
                    intensity=intensity
                )

                print(f"   {civ1_name} → {civ2_name}: {loans1to2} paraules prestades")
                print(f"   {civ2_name} → {civ1_name}: {loans2to1} paraules prestades")

                # Mostra exemples de préstecs
                if lang1.name in evolution_system.loanwords:
                    loans = evolution_system.loanwords[lang1.name][:3]
                    if loans:
                        print(f"   Exemples de préstecs a {lang1.name}:")
                        for loan in loans:
                            print(f"     - {loan.concept}='{loan.word}' (de {loan.source_language})")
                print()

    # === FASE 3: EVOLUCIÓ TEMPORAL ===
    print()
    print("=" * 80)
    print("FASE 3: EVOLUCIÓ TEMPORAL (200 ANYS)")
    print("=" * 80)
    print()

    print("Simulant 200 anys d'evolució lingüística...")
    print()

    for data in civilizations_data[:3]:  # Només 3 primeres per exemple
        civ = data['civilization']
        lang = data['language']

        print(f"🕐 {civ.name} ({lang.name}):")

        # Guarda paraules originals
        original_water = lang.vocabulary.get('water', '')
        original_fire = lang.vocabulary.get('fire', '')
        original_king = lang.vocabulary.get('king', '')

        # Evoluciona
        evolution_system.evolve_language_over_time(
            language=lang,
            years_passed=200,
            events=None
        )

        # Mostra canvis
        new_water = lang.vocabulary.get('water', '')
        new_fire = lang.vocabulary.get('fire', '')
        new_king = lang.vocabulary.get('king', '')

        print(f"   water: '{original_water}' → '{new_water}'")
        print(f"   fire:  '{original_fire}' → '{new_fire}'")
        print(f"   king:  '{original_king}' → '{new_king}'")
        print()

    # === FASE 4: LLENGUA FRANCA ===
    print()
    print("=" * 80)
    print("FASE 4: CREACIÓ DE LLENGUA FRANCA (GLOBALITZACIÓ)")
    print("=" * 80)
    print()

    print("Creant llengua franca comercial entre totes les civilitzacions...")
    print()

    all_languages = [data['language'] for data in civilizations_data]
    all_civ_names = [data['civilization'].name for data in civilizations_data]

    lingua_franca = evolution_system.create_lingua_franca(
        languages=all_languages,
        civilization_names=all_civ_names,
        year=200,
        context="trade"
    )

    print(f"🌍 {lingua_franca.name}")
    print(f"   Família: {lingua_franca.family}")
    print(f"   Fonemes: {len(lingua_franca.phoneme_inventory.consonants)}C + {len(lingua_franca.phoneme_inventory.vowels)}V")
    print(f"   (Simplificació dels fonemes més comuns de totes les llengües)")
    print()
    print(f"   Vocabulari mixt:")
    for concept in ['water', 'fire', 'king', 'trade', 'peace']:
        if concept in lingua_franca.vocabulary:
            word = lingua_franca.vocabulary[concept]
            print(f"     {concept:10s} = {word}")
    print()

    # === FASE 5: DIVERSITAT LINGÜÍSTICA ===
    print()
    print("=" * 80)
    print("FASE 5: MESURA DE DIVERSITAT LINGÜÍSTICA")
    print("=" * 80)
    print()

    diversity_initial = evolution_system.get_linguistic_diversity(all_languages)
    print(f"Diversitat lingüística inicial: {diversity_initial:.2%}")
    print(f"  (0% = llengües idèntiques, 100% = llengües completament diferents)")
    print()

    # Compara similituds entre parelles
    print("Similituds entre llengües:")
    for i, data1 in enumerate(civilizations_data[:3]):
        for data2 in civilizations_data[i+1:4]:
            lang1 = data1['language']
            lang2 = data2['language']
            similarity = evolution_system._calculate_similarity(lang1, lang2)
            print(f"  {lang1.name} ↔ {lang2.name}: {similarity:.2%} similar")
    print()

    # Estadístiques globals
    stats = evolution_system.get_statistics()
    print("Estadístiques d'evolució lingüística:")
    print(f"  Total contactes registrats: {stats['total_contacts']}")
    print(f"  Total paraules prestades: {stats['total_loanwords']}")
    print(f"  Llengües amb préstecs: {stats['languages_with_loans']}")
    print(f"  Mitjana préstecs per llengua: {stats['average_loans_per_language']:.1f}")

    print()
    print("=" * 80)
    print("Test completat!")
    print()
    print("RESUM:")
    print("  ✓ Llengües generades amb context complet (IA + cultura + entorn)")
    print("  ✓ Préstecs lingüístics entre civilitzacions properes")
    print("  ✓ Evolució temporal (canvis fonètics al llarg de 200 anys)")
    print("  ✓ Llengua franca creada per globalització comercial")
    print("  ✓ Diversitat lingüística mesurada")
    print()
    print("Observacions:")
    print("  - Llengües evolucionen segons proximitat geogràfica")
    print("  - Préstecs més intensos en civilitzacions properes (<50 tiles)")
    print("  - Evolució temporal causa canvis fonètics graduales")
    print("  - Llengua franca simplifica fonemes i mixa vocabulari")
    print("  - Diversitat lingüística reflexa història i contactes")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
