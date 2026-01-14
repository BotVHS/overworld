#!/usr/bin/env python3
"""
Test del sistema de llengües

Genera llengües úniques amb fonologia procedural i famílies lingüístiques
"""
import sys
from overworld.world.world import World
from overworld.civilization.civilization import create_civilizations
from overworld.civilization.language import LanguageGenerator, LanguageFamily


def main():
    """Test del sistema de llengües"""
    print("=" * 80)
    print("  TEST DEL SISTEMA DE LLENGÜES PROCEDURALS")
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

    # Crea generador de llengües
    print("=" * 80)
    print("GENERANT LLENGÜES ÚNIQUES")
    print("=" * 80)
    print()

    generator = LanguageGenerator(seed=42)

    # Genera llengua per cada civilització
    languages = []

    for i, civ in enumerate(civ_manager.civilizations, 1):
        capital_tile = world.get_tile(civ.capital.x, civ.capital.y)

        from overworld.world.biome import BIOME_DEFINITIONS
        environment_type = BIOME_DEFINITIONS[capital_tile.biome].name if capital_tile.biome else "Desconegut"

        print(f"\n{'=' * 80}")
        print(f"CIVILITZACIÓ {i}: {civ.name}")
        print(f"{'=' * 80}")

        # Genera llengua
        language = generator.generate_language(
            civilization_name=civ.name,
            culture_traits=civ.culture.to_dict(),
            environment_type=environment_type
        )

        language.speakers = civ.total_population
        languages.append(language)

        # Mostra informació de la llengua
        print(f"\n🗣️  LLENGUA: {language.name}")
        print(f"{'─' * 80}")
        print(f"  Família: {language.family}")
        print(f"  Parlants: {language.speakers:,}")
        print()
        print(f"  Fonologia:")
        print(f"    Consonants ({len(language.phoneme_inventory.consonants)}): {', '.join(language.phoneme_inventory.consonants)}")
        print(f"    Vocals ({len(language.phoneme_inventory.vowels)}): {', '.join(language.phoneme_inventory.vowels)}")
        print()
        print(f"  Regles:")
        print(f"    Estructures sil·làbiques: {', '.join(language.phonology_rules.syllable_structures)}")
        print(f"    Clusters consonàntics: {'Sí' if language.phonology_rules.allow_consonant_clusters else 'No'}")
        print(f"    Màx síl·labes per paraula: {language.phonology_rules.max_syllables_per_word}")
        print(f"    Patró d'accent: {language.phonology_rules.stress_pattern}")
        print()
        print(f"  Vocabulari Bàsic (exemples):")

        # Mostra exemples de vocabulari
        example_concepts = ['water', 'fire', 'sun', 'moon', 'mountain', 'king', 'god', 'one', 'two', 'three']
        for concept in example_concepts:
            if concept in language.vocabulary:
                print(f"    {concept:12s} = {language.vocabulary[concept]}")

    # Demostra famílies lingüístiques
    print()
    print("=" * 80)
    print("FAMÍLIES LINGÜÍSTIQUES I EVOLUCIÓ")
    print("=" * 80)
    print()

    # Crea una família lingüística
    family = LanguageFamily(name="Proto-Altaic", proto_language=languages[0])
    print(f"📚 Família: {family.name}")
    print(f"   Llengua proto: {languages[0].name}")
    print()

    # Genera 3 llengües filles amb diferents graus de divergència
    print("Generant llengües filles amb evolució fonètica:")
    print()

    divergences = [0.2, 0.4, 0.6]
    daughter_civs = ["Nordia", "Sudia", "Estia"]

    for i, (div, civ_name) in enumerate(zip(divergences, daughter_civs), 1):
        daughter_lang = family.generate_daughter_language(
            civilization_name=civ_name,
            base_language=languages[0],
            divergence=div
        )

        print(f"  {i}. {daughter_lang.name} (divergència {div*100:.0f}%)")
        print(f"     Consonants: {', '.join(daughter_lang.phoneme_inventory.consonants[:10])}...")
        print(f"     Exemples:")

        # Compara paraules
        for concept in ['water', 'fire', 'king']:
            proto_word = languages[0].vocabulary.get(concept, '?')
            daughter_word = daughter_lang.vocabulary.get(concept, '?')
            print(f"       {concept:12s}: {proto_word:10s} → {daughter_word}")
        print()

    # Estadístiques de la família
    stats = family.get_statistics()
    print(f"Estadístiques de {stats['family_name']}:")
    print(f"  Llengües: {stats['num_languages']}")
    print(f"  Llengües dins la família: {', '.join(stats['languages'])}")

    print()
    print("=" * 80)
    print("Test completat!")
    print()
    print("Observacions:")
    print("  - Cada civilització té una llengua única")
    print("  - Inventaris fonètics diferents (10-25 consonants, 3-12 vocals)")
    print("  - Regles fonològiques variades (estructures sil·làbiques, clusters)")
    print("  - Vocabulari generat proceduralment")
    print("  - Famílies lingüístiques amb evolució fonètica")
    print("  - Divergència lingüística simulada")
    print()
    print("Pròxims passos:")
    print("  - Afegir llengües a la classe Civilization")
    print("  - Evolució lingüística al llarg del temps")
    print("  - Dialectes regionals")
    print("  - Préstecs lingüístics entre civilitzacions")
    print("  - Demografia amb distribució de parlants")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
