"""
Language Evolution - Evolució lingüística amb IA

Sistema avançat d'evolució de llengües amb:
- Generació contextual amb Ollama
- Préstecs lingüístics entre civilitzacions
- Globalització i llengües franca
- Criollització i pidginització
"""
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
import random
from .language import Language, LanguageGenerator, PhonemeInventory
from ..ai.ollama_client import get_ollama_client


@dataclass
class LinguisticContact:
    """
    Contacte lingüístic entre dues civilitzacions
    """
    civ1_name: str
    civ2_name: str
    intensity: float  # 0.0-1.0, intensitat del contacte
    duration_years: int  # Duració del contacte
    contact_type: str  # trade, war, cultural_exchange, conquest


@dataclass
class Loanword:
    """
    Paraula prestada d'una altra llengua
    """
    concept: str
    word: str
    source_language: str
    year_borrowed: int


class AdvancedLanguageGenerator:
    """
    Generador avançat de llengües amb IA
    """

    def __init__(self, use_ollama: bool = True):
        """
        Args:
            use_ollama: Si usar Ollama per generació contextual
        """
        self.use_ollama = use_ollama
        self.ollama = get_ollama_client() if use_ollama else None
        self.basic_generator = LanguageGenerator()

    def generate_contextual_language(
        self,
        civilization_name: str,
        culture_traits: Dict,
        environment_type: str,
        political_system: Optional[Dict] = None,
        religious_system: Optional[Dict] = None,
        economic_system: Optional[Dict] = None,
        history: Optional[List[str]] = None
    ) -> Language:
        """
        Genera una llengua amb context complet

        Args:
            civilization_name: Nom de la civilització
            culture_traits: Trets culturals
            environment_type: Tipus d'entorn
            political_system: Sistema polític
            religious_system: Sistema religiós
            economic_system: Sistema econòmic
            history: Història recent

        Returns:
            Language generada
        """
        # Genera llengua base
        language = self.basic_generator.generate_language(
            civilization_name=civilization_name,
            culture_traits=culture_traits,
            environment_type=environment_type
        )

        # Amplia vocabulari amb context si Ollama disponible
        if self.use_ollama and self.ollama and self.ollama.available:
            self._expand_vocabulary_with_ai(
                language,
                civilization_name,
                culture_traits,
                environment_type,
                political_system,
                religious_system,
                economic_system,
                history
            )

        return language

    def _expand_vocabulary_with_ai(
        self,
        language: Language,
        civilization_name: str,
        culture_traits: Dict,
        environment_type: str,
        political_system: Optional[Dict],
        religious_system: Optional[Dict],
        economic_system: Optional[Dict],
        history: Optional[List[str]]
    ):
        """Amplia vocabulari amb conceptes contextuals generats per IA"""

        # Construeix prompt contextual
        prompt = f"""Genera 10 conceptes únics importants per la civilització {civilization_name}.

CONTEXT:
Entorn: {environment_type}
Sistema polític: {political_system.get('name') if political_system else 'Desconegut'}
Sistema religiós: {religious_system.get('name') if religious_system else 'Desconegut'}
Sistema econòmic: {economic_system.get('name') if economic_system else 'Desconegut'}

Valors culturals: {', '.join(culture_traits.get('core_values', ['equilibri']))}
Militarisme: {culture_traits.get('militarism', 50):.0f}/100
Religiositat: {culture_traits.get('religion', 50):.0f}/100
Comerç: {culture_traits.get('commerce', 50):.0f}/100

Història recent:
{chr(10).join(f"- {event}" for event in (history or [])[:5]) if history else "- Cap història"}

INSTRUCCIONS:
Basant-te en aquest context, genera 10 conceptes únics que serien importants per aquesta civilització.
Per exemple, una cultura comercial marina pot tenir conceptes com "port segur", "vent favorable", "ruta comercial".
Una cultura religiosa de muntanya pot tenir "cim sagrat", "ermità", "pelegrinatge".

Respon NOMÉS en format JSON (sense markdown):
{{
"conceptes": ["concepte1", "concepte2", ..., "concepte10"]
}}"""

        result = self.ollama.generate_json(prompt, temperature=0.8)

        if result and 'conceptes' in result:
            # Genera paraules per aquests conceptes
            for concept in result['conceptes'][:10]:
                if concept not in language.vocabulary:
                    word = self.basic_generator._generate_word(language)
                    language.vocabulary[concept] = word


class LanguageEvolutionSystem:
    """
    Sistema d'evolució lingüística temporal
    """

    def __init__(self, use_ollama: bool = True):
        """
        Args:
            use_ollama: Si usar Ollama per evolució contextual
        """
        self.use_ollama = use_ollama
        self.ollama = get_ollama_client() if use_ollama else None
        self.contacts: List[LinguisticContact] = []
        self.loanwords: Dict[str, List[Loanword]] = {}  # language_name -> loanwords

    def register_contact(
        self,
        civ1_name: str,
        civ2_name: str,
        intensity: float,
        duration_years: int,
        contact_type: str
    ):
        """Registra un contacte lingüístic entre civilitzacions"""
        contact = LinguisticContact(
            civ1_name=civ1_name,
            civ2_name=civ2_name,
            intensity=intensity,
            duration_years=duration_years,
            contact_type=contact_type
        )
        self.contacts.append(contact)

    def apply_linguistic_borrowing(
        self,
        language1: Language,
        language2: Language,
        civ1_name: str,
        civ2_name: str,
        year: int,
        intensity: float = 0.3
    ) -> int:
        """
        Aplica préstecs lingüístics entre dues llengües

        Args:
            language1: Llengua receptora
            language2: Llengua donant
            civ1_name: Nom civilització 1
            civ2_name: Nom civilització 2
            year: Any actual
            intensity: Intensitat del contacte (0.0-1.0)

        Returns:
            Nombre de paraules prestades
        """
        # Determina quantes paraules es presten
        num_loans = int(len(language2.vocabulary) * intensity * 0.1)  # Fins a 10%
        num_loans = max(1, min(num_loans, 10))  # Entre 1 i 10

        borrowed = 0

        # Selecciona paraules aleatòries de language2
        concepts = list(language2.vocabulary.keys())
        random.shuffle(concepts)

        for concept in concepts[:num_loans]:
            # Adapta la paraula a la fonologia de language1
            source_word = language2.vocabulary[concept]
            adapted_word = self._phonological_adaptation(source_word, language1)

            # Afegeix a vocabulari
            language1.vocabulary[concept] = adapted_word

            # Registra préstec
            if language1.name not in self.loanwords:
                self.loanwords[language1.name] = []

            self.loanwords[language1.name].append(
                Loanword(
                    concept=concept,
                    word=adapted_word,
                    source_language=language2.name,
                    year_borrowed=year
                )
            )

            borrowed += 1

        return borrowed

    def _phonological_adaptation(self, word: str, target_language: Language) -> str:
        """
        Adapta una paraula a la fonologia d'una llengua

        Args:
            word: Paraula original
            target_language: Llengua objectiu

        Returns:
            Paraula adaptada
        """
        # Adaptació simple: substitueix fonemes no existents
        adapted = ""

        for char in word:
            if char in target_language.phoneme_inventory.consonants:
                adapted += char
            elif char in target_language.phoneme_inventory.vowels:
                adapted += char
            else:
                # Substitueix per fonema similar
                if char in ['p', 'b', 't', 'd', 'k', 'g']:
                    # Stops: escull un stop disponible
                    available_stops = [c for c in target_language.phoneme_inventory.consonants
                                     if c in ['p', 'b', 't', 'd', 'k', 'g']]
                    if available_stops:
                        adapted += random.choice(available_stops)
                    else:
                        adapted += random.choice(target_language.phoneme_inventory.consonants)
                else:
                    # Altres: escull consonant/vocal aleatòria
                    if random.random() < 0.7:
                        adapted += random.choice(target_language.phoneme_inventory.consonants)
                    else:
                        adapted += random.choice(target_language.phoneme_inventory.vowels)

        return adapted if adapted else self.basic_generator._generate_word(target_language)

    def evolve_language_over_time(
        self,
        language: Language,
        years_passed: int,
        events: Optional[List] = None
    ):
        """
        Evoluciona una llengua al llarg del temps

        Args:
            language: Llengua a evolucionar
            years_passed: Anys transcorreguts
            events: Esdeveniments que afecten la llengua
        """
        # Taxa d'evolució: ~1-3% de vocabulari canvia cada 100 anys
        evolution_rate = (years_passed / 100.0) * 0.02

        # Evolució natural
        words_to_change = int(len(language.vocabulary) * evolution_rate)

        concepts = list(language.vocabulary.keys())
        random.shuffle(concepts)

        for concept in concepts[:words_to_change]:
            # Canvi fonètic menor
            old_word = language.vocabulary[concept]
            new_word = self._apply_sound_change(old_word, intensity=0.3)
            language.vocabulary[concept] = new_word

    def _apply_sound_change(self, word: str, intensity: float) -> str:
        """Aplica canvis fonètics a una paraula"""
        if random.random() > intensity or len(word) <= 1:
            return word

        changes = [
            lambda w: w[1:] if len(w) > 2 else w,  # Perd primera lletra
            lambda w: w[:-1] if len(w) > 2 else w,  # Perd última lletra
            lambda w: w + random.choice(['a', 'i', 'u', 'e', 'o']),  # Afegeix vocal
            lambda w: w[0] + w[2:] if len(w) > 2 else w,  # Perd segona lletra
        ]

        change = random.choice(changes)
        return change(word)

    def create_lingua_franca(
        self,
        languages: List[Language],
        civilization_names: List[str],
        year: int,
        context: str = "trade"
    ) -> Language:
        """
        Crea una llengua franca basada en múltiples llengües

        Args:
            languages: Llengües contribuents
            civilization_names: Noms de les civilitzacions
            year: Any de creació
            context: Context (trade, diplomatic, religious)

        Returns:
            Nova llengua franca
        """
        # Nom de la llengua franca
        if context == "trade":
            franca_name = "Mercantile Common"
        elif context == "diplomatic":
            franca_name = "Diplomatic Tongue"
        elif context == "religious":
            franca_name = "Sacred Language"
        else:
            franca_name = "Common Speech"

        # Inventari fonètic: unió simplificada
        all_consonants = []
        all_vowels = []

        for lang in languages:
            all_consonants.extend(lang.phoneme_inventory.consonants)
            all_vowels.extend(lang.phoneme_inventory.vowels)

        # Simplifica: escull els més comuns
        consonant_counts = {}
        for c in all_consonants:
            consonant_counts[c] = consonant_counts.get(c, 0) + 1

        vowel_counts = {}
        for v in all_vowels:
            vowel_counts[v] = vowel_counts.get(v, 0) + 1

        # Escull top 12 consonants, top 6 vocals
        common_consonants = sorted(consonant_counts.keys(), key=lambda x: consonant_counts[x], reverse=True)[:12]
        common_vowels = sorted(vowel_counts.keys(), key=lambda x: vowel_counts[x], reverse=True)[:6]

        # Crea llengua franca
        franca = Language(
            name=franca_name,
            family="Lingua Franca",
            phoneme_inventory=PhonemeInventory(
                consonants=common_consonants,
                vowels=common_vowels
            ),
            phonology_rules=languages[0].phonology_rules  # Hereta regles de la primera
        )

        # Vocabulari: mixt de totes les llengües
        for concept in LanguageGenerator.BASIC_CONCEPTS:
            # Escull paraula d'una llengua aleatòria
            source_lang = random.choice(languages)
            if concept in source_lang.vocabulary:
                word = source_lang.vocabulary[concept]
                # Adapta a fonologia de la franca
                adapted = self._phonological_adaptation(word, franca)
                franca.vocabulary[concept] = adapted

        return franca

    def get_linguistic_diversity(self, languages: List[Language]) -> float:
        """
        Calcula diversitat lingüística (0.0-1.0)

        0.0 = Totes les llengües idèntiques
        1.0 = Llengües completament diferents

        Args:
            languages: Llista de llengües

        Returns:
            Índex de diversitat
        """
        if len(languages) < 2:
            return 0.0

        total_similarity = 0.0
        comparisons = 0

        for i, lang1 in enumerate(languages):
            for lang2 in languages[i+1:]:
                similarity = self._calculate_similarity(lang1, lang2)
                total_similarity += similarity
                comparisons += 1

        avg_similarity = total_similarity / comparisons if comparisons > 0 else 1.0
        diversity = 1.0 - avg_similarity

        return diversity

    def _calculate_similarity(self, lang1: Language, lang2: Language) -> float:
        """Calcula similitud entre dues llengües (0.0-1.0)"""

        # Similitud fonètica
        common_consonants = set(lang1.phoneme_inventory.consonants) & set(lang2.phoneme_inventory.consonants)
        common_vowels = set(lang1.phoneme_inventory.vowels) & set(lang2.phoneme_inventory.vowels)

        total_phonemes1 = len(lang1.phoneme_inventory.consonants) + len(lang1.phoneme_inventory.vowels)
        total_phonemes2 = len(lang2.phoneme_inventory.consonants) + len(lang2.phoneme_inventory.vowels)

        phonetic_similarity = (len(common_consonants) + len(common_vowels)) / ((total_phonemes1 + total_phonemes2) / 2.0)

        # Similitud de vocabulari
        common_concepts = set(lang1.vocabulary.keys()) & set(lang2.vocabulary.keys())
        shared_words = 0

        for concept in common_concepts:
            if lang1.vocabulary[concept] == lang2.vocabulary[concept]:
                shared_words += 1

        vocab_similarity = shared_words / len(common_concepts) if common_concepts else 0.0

        # Similitud de família
        family_similarity = 1.0 if lang1.family == lang2.family else 0.0

        # Mitjana ponderada
        similarity = (phonetic_similarity * 0.3 + vocab_similarity * 0.5 + family_similarity * 0.2)

        return min(1.0, similarity)

    def get_statistics(self) -> Dict:
        """Obté estadístiques d'evolució lingüística"""
        total_loanwords = sum(len(loans) for loans in self.loanwords.values())

        return {
            'total_contacts': len(self.contacts),
            'total_loanwords': total_loanwords,
            'languages_with_loans': len(self.loanwords),
            'average_loans_per_language': total_loanwords / len(self.loanwords) if self.loanwords else 0
        }
