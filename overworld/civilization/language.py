"""
Language System - Sistema de llengües procedurals

Genera llengües úniques amb fonologia, vocabulari i famílies lingüístiques
"""
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
import random


@dataclass
class PhonemeInventory:
    """
    Inventari de fonemes d'una llengua
    """
    consonants: List[str] = field(default_factory=list)
    vowels: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Genera inventari per defecte si està buit"""
        if not self.consonants:
            self.consonants = ['p', 't', 'k', 'b', 'd', 'g', 'm', 'n', 'l', 'r', 's']
        if not self.vowels:
            self.vowels = ['a', 'e', 'i', 'o', 'u']


@dataclass
class PhonologyRules:
    """
    Regles fonològiques d'una llengua
    """
    syllable_structures: List[str] = field(default_factory=lambda: ['CV', 'CVC', 'V'])
    allow_consonant_clusters: bool = False
    max_syllables_per_word: int = 3
    stress_pattern: str = "initial"  # initial, final, penultimate


@dataclass
class Language:
    """
    Una llengua única generada proceduralment
    """
    name: str
    family: Optional[str] = None
    phoneme_inventory: PhonemeInventory = field(default_factory=PhonemeInventory)
    phonology_rules: PhonologyRules = field(default_factory=PhonologyRules)
    vocabulary: Dict[str, str] = field(default_factory=dict)
    speakers: int = 0

    def to_dict(self) -> Dict:
        """Serialitza la llengua"""
        return {
            'name': self.name,
            'family': self.family,
            'consonants': self.phoneme_inventory.consonants,
            'vowels': self.phoneme_inventory.vowels,
            'syllable_structures': self.phonology_rules.syllable_structures,
            'vocabulary_size': len(self.vocabulary),
            'speakers': self.speakers
        }


class LanguageGenerator:
    """
    Generador procedural de llengües úniques
    """

    # Pools de fonemes possibles
    CONSONANTS_POOL = {
        'stops': ['p', 'b', 't', 'd', 'k', 'g', 'q'],
        'fricatives': ['f', 'v', 's', 'z', 'sh', 'zh', 'h', 'th'],
        'nasals': ['m', 'n', 'ng'],
        'liquids': ['l', 'r'],
        'approximants': ['w', 'y']
    }

    VOWELS_POOL = {
        'basic': ['a', 'e', 'i', 'o', 'u'],
        'front': ['i', 'e', 'æ'],
        'back': ['u', 'o', 'ɔ'],
        'central': ['ə', 'ʌ']
    }

    # Vocabulari bàsic per generar
    BASIC_CONCEPTS = [
        'water', 'fire', 'earth', 'air', 'sun', 'moon', 'star',
        'mountain', 'river', 'sea', 'tree', 'stone',
        'man', 'woman', 'child', 'people',
        'one', 'two', 'three', 'four', 'five',
        'big', 'small', 'good', 'bad', 'strong', 'weak',
        'king', 'god', 'war', 'peace', 'trade', 'city',
        'north', 'south', 'east', 'west'
    ]

    def __init__(self, seed: Optional[int] = None):
        """
        Args:
            seed: Seed per reproducibilitat
        """
        if seed:
            random.seed(seed)

    def generate_language(
        self,
        civilization_name: str,
        culture_traits: Dict,
        environment_type: str,
        family: Optional[str] = None
    ) -> Language:
        """
        Genera una llengua única

        Args:
            civilization_name: Nom de la civilització
            culture_traits: Trets culturals
            environment_type: Tipus d'entorn
            family: Família lingüística (opcional)

        Returns:
            Language generada
        """
        # Genera nom de la llengua
        language_name = self._generate_language_name(civilization_name)

        # Genera inventari fonètic
        phoneme_inventory = self._generate_phoneme_inventory(culture_traits, environment_type)

        # Genera regles fonològiques
        phonology_rules = self._generate_phonology_rules(culture_traits)

        # Crea llengua
        language = Language(
            name=language_name,
            family=family or self._generate_family_name(),
            phoneme_inventory=phoneme_inventory,
            phonology_rules=phonology_rules
        )

        # Genera vocabulari bàsic
        self._generate_vocabulary(language)

        return language

    def _generate_language_name(self, civilization_name: str) -> str:
        """Genera nom de la llengua"""
        suffixes = ['ic', 'ese', 'ian', 'ish', 'i', 'an']
        return f"{civilization_name}{random.choice(suffixes)}"

    def _generate_family_name(self) -> str:
        """Genera nom de família lingüística"""
        prefixes = ['Proto', 'Ancient', 'Old', 'Classical']
        roots = ['Altaic', 'Dravid', 'Ural', 'Semit', 'Indo', 'Sino', 'Niger']
        suffixes = ['ic', 'ian', 'ese']

        if random.random() < 0.3:
            return f"{random.choice(prefixes)}-{random.choice(roots)}{random.choice(suffixes)}"
        else:
            return f"{random.choice(roots)}{random.choice(suffixes)}"

    def _generate_phoneme_inventory(
        self,
        culture_traits: Dict,
        environment_type: str
    ) -> PhonemeInventory:
        """Genera inventari de fonemes"""

        # Consonants: 10-25 fonemes
        num_consonants = random.randint(10, 25)

        consonants = []

        # Sempre inclou stops bàsics
        consonants.extend(random.sample(self.CONSONANTS_POOL['stops'], min(4, len(self.CONSONANTS_POOL['stops']))))

        # Afegeix fricatives
        num_fricatives = random.randint(2, 5)
        consonants.extend(random.sample(self.CONSONANTS_POOL['fricatives'], min(num_fricatives, len(self.CONSONANTS_POOL['fricatives']))))

        # Afegeix nasals
        consonants.extend(random.sample(self.CONSONANTS_POOL['nasals'], random.randint(1, 3)))

        # Afegeix líquids
        consonants.extend(random.sample(self.CONSONANTS_POOL['liquids'], random.randint(1, 2)))

        # Afegeix aproximants si hi ha espai
        while len(consonants) < num_consonants and self.CONSONANTS_POOL['approximants']:
            consonants.append(random.choice(self.CONSONANTS_POOL['approximants']))

        # Vocals: 3-12 fonemes
        num_vowels = random.randint(3, 12)

        vowels = list(self.VOWELS_POOL['basic'])  # Sempre inclou les 5 bàsiques

        # Afegeix vocals addicionals
        extra_pools = ['front', 'back', 'central']
        while len(vowels) < num_vowels:
            pool = random.choice(extra_pools)
            candidates = [v for v in self.VOWELS_POOL[pool] if v not in vowels]
            if candidates:
                vowels.append(random.choice(candidates))
            else:
                break

        return PhonemeInventory(
            consonants=consonants[:num_consonants],
            vowels=vowels[:num_vowels]
        )

    def _generate_phonology_rules(self, culture_traits: Dict) -> PhonologyRules:
        """Genera regles fonològiques"""

        # Estructura sil·làbica
        structures = ['V', 'CV']  # Sempre permès

        # Cultures complexes → estructures més complexes
        if culture_traits.get('science', 50) > 60 or culture_traits.get('craftsmanship', 50) > 60:
            structures.extend(['CVC', 'CCV', 'VCC'])
        else:
            structures.append('CVC')

        # Clusters consonàntics
        allow_clusters = random.random() < 0.5

        # Longitud de paraules
        max_syllables = random.randint(2, 4)

        # Patró d'accent
        stress_patterns = ['initial', 'final', 'penultimate']
        stress = random.choice(stress_patterns)

        return PhonologyRules(
            syllable_structures=structures,
            allow_consonant_clusters=allow_clusters,
            max_syllables_per_word=max_syllables,
            stress_pattern=stress
        )

    def _generate_vocabulary(self, language: Language):
        """Genera vocabulari bàsic"""
        for concept in self.BASIC_CONCEPTS:
            word = self._generate_word(language)
            language.vocabulary[concept] = word

    def _generate_word(self, language: Language) -> str:
        """Genera una paraula seguint les regles fonològiques"""

        num_syllables = random.randint(1, language.phonology_rules.max_syllables_per_word)
        syllables = []

        for _ in range(num_syllables):
            structure = random.choice(language.phonology_rules.syllable_structures)
            syllable = self._generate_syllable(structure, language.phoneme_inventory)
            syllables.append(syllable)

        return ''.join(syllables)

    def _generate_syllable(self, structure: str, inventory: PhonemeInventory) -> str:
        """Genera una síl·laba segons l'estructura"""
        result = ""

        for char in structure:
            if char == 'C':
                result += random.choice(inventory.consonants)
            elif char == 'V':
                result += random.choice(inventory.vowels)

        return result


class LanguageFamily:
    """
    Família lingüística amb llengües emparentades
    """

    def __init__(self, name: str, proto_language: Optional[Language] = None):
        """
        Args:
            name: Nom de la família
            proto_language: Llengua proto-ancestral (opcional)
        """
        self.name = name
        self.proto_language = proto_language
        self.languages: List[Language] = []

    def add_language(self, language: Language):
        """Afegeix una llengua a la família"""
        language.family = self.name
        self.languages.append(language)

    def generate_daughter_language(
        self,
        civilization_name: str,
        base_language: Language,
        divergence: float = 0.3
    ) -> Language:
        """
        Genera una llengua filla amb evolució fonètica

        Args:
            civilization_name: Nom de la nova civilització
            base_language: Llengua base
            divergence: Grau de divergència (0.0-1.0)

        Returns:
            Nova llengua divergent
        """
        generator = LanguageGenerator()

        # Hereta fonemes però amb canvis
        new_consonants = base_language.phoneme_inventory.consonants.copy()
        new_vowels = base_language.phoneme_inventory.vowels.copy()

        # Canvis fonètics (sound changes)
        num_changes = int(len(new_consonants) * divergence)
        for _ in range(num_changes):
            if len(new_consonants) > 3 and random.random() < 0.5:
                # Perd un fonema
                new_consonants.remove(random.choice(new_consonants))
            else:
                # Guanya un fonema
                all_consonants = [c for sublist in LanguageGenerator.CONSONANTS_POOL.values() for c in sublist]
                candidates = [c for c in all_consonants if c not in new_consonants]
                if candidates:
                    new_consonants.append(random.choice(candidates))

        # Crea nova llengua
        new_language = Language(
            name=generator._generate_language_name(civilization_name),
            family=self.name,
            phoneme_inventory=PhonemeInventory(
                consonants=new_consonants,
                vowels=new_vowels
            ),
            phonology_rules=base_language.phonology_rules
        )

        # Hereta vocabulari amb canvis
        for concept, word in base_language.vocabulary.items():
            if random.random() < divergence:
                # Regenera paraula
                new_word = generator._generate_word(new_language)
            else:
                # Canvi fonètic menor
                new_word = self._apply_sound_change(word, divergence)

            new_language.vocabulary[concept] = new_word

        self.add_language(new_language)
        return new_language

    def _apply_sound_change(self, word: str, intensity: float) -> str:
        """Aplica canvis fonètics menors"""
        if random.random() > intensity:
            return word

        # Canvis possibles
        changes = [
            lambda w: w[1:] if len(w) > 1 else w,  # Perd primera lletra
            lambda w: w[:-1] if len(w) > 1 else w,  # Perd última lletra
            lambda w: w + random.choice(['a', 'i', 'u']),  # Afegeix vocal final
        ]

        change = random.choice(changes)
        return change(word)

    def get_statistics(self) -> Dict:
        """Obté estadístiques de la família"""
        return {
            'family_name': self.name,
            'num_languages': len(self.languages),
            'total_speakers': sum(lang.speakers for lang in self.languages),
            'languages': [lang.name for lang in self.languages]
        }
