"""
Cultural Movements - Moviments culturals i art amb IA

Genera moviments artístics, obres mestres i evolució cultural amb Ollama
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import random
from ..ai.civilization_ai_models import CivilizationAISystem


class ArtForm(Enum):
    """Formes d'art"""
    ARCHITECTURE = "arquitectura"
    SCULPTURE = "escultura"
    PAINTING = "pintura"
    MUSIC = "música"
    LITERATURE = "literatura"
    THEATER = "teatre"
    DANCE = "dansa"
    POETRY = "poesia"


@dataclass
class ArtisticWork:
    """
    Una obra d'art o cultural
    """
    title: str
    art_form: ArtForm
    creator: str  # Nom de l'artista
    year_created: int
    civilization: str
    description: str
    cultural_impact: int  # 1-10
    themes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Serialitza l'obra"""
        return {
            'title': self.title,
            'art_form': self.art_form.value,
            'creator': self.creator,
            'year_created': self.year_created,
            'civilization': self.civilization,
            'description': self.description,
            'cultural_impact': self.cultural_impact,
            'themes': self.themes
        }


@dataclass
class CulturalMovement:
    """
    Un moviment cultural o artístic
    """
    name: str
    civilization: str
    year_started: int
    art_forms: List[ArtForm]
    philosophy: str
    key_characteristics: List[str]
    major_works: List[ArtisticWork] = field(default_factory=list)
    influence_score: int = 0  # 0-100

    def to_dict(self) -> Dict:
        """Serialitza el moviment"""
        return {
            'name': self.name,
            'civilization': self.civilization,
            'year_started': self.year_started,
            'art_forms': [af.value for af in self.art_forms],
            'philosophy': self.philosophy,
            'key_characteristics': self.key_characteristics,
            'major_works_count': len(self.major_works),
            'influence_score': self.influence_score
        }


class CulturalSystem:
    """
    Sistema de cultura i art amb IA
    """

    def __init__(self, ai_system: CivilizationAISystem):
        """
        Args:
            ai_system: Sistema de models IA per civilització
        """
        self.ai_system = ai_system
        self.movements: List[CulturalMovement] = []
        self.artworks: List[ArtisticWork] = []

    def generate_cultural_movement(
        self,
        civilization_name: str,
        year: int,
        culture_traits: Dict,
        recent_history: List[str],
        use_ai: bool = True
    ) -> Optional[CulturalMovement]:
        """
        Genera un moviment cultural amb IA

        Args:
            civilization_name: Nom de la civilització
            year: Any de creació
            culture_traits: Trets culturals
            recent_history: Història recent
            use_ai: Si usar IA o procedural

        Returns:
            CulturalMovement generat
        """
        if use_ai:
            movement = self._generate_movement_with_ai(
                civilization_name,
                year,
                culture_traits,
                recent_history
            )

            if movement:
                self.movements.append(movement)
                return movement

        # Fallback procedural
        return self._generate_movement_procedural(
            civilization_name,
            year,
            culture_traits
        )

    def _generate_movement_with_ai(
        self,
        civilization_name: str,
        year: int,
        culture_traits: Dict,
        recent_history: List[str]
    ) -> Optional[CulturalMovement]:
        """Genera moviment cultural amb el model IA de la civilització"""

        # Construeix prompt
        prompt = f"""Genera un moviment cultural o artístic únic per la civilització {civilization_name}.

CONTEXT CULTURAL:
Any: {year}
Valors culturals dominants: {', '.join(culture_traits.get('core_values', ['equilibri']))}
Nivell artístic: {culture_traits.get('art', 50):.0f}/100
Nivell científic: {culture_traits.get('science', 50):.0f}/100
Religiositat: {culture_traits.get('religion', 50):.0f}/100

Història recent:
{chr(10).join(f"- {event}" for event in recent_history[:5]) if recent_history else "- Sense història recent"}

INSTRUCCIONS:
Crea un moviment cultural ORIGINAL i ÚNIC (no Renaixement, Barroc, etc. històrics humans).
El moviment ha de reflectir els valors i història de {civilization_name}.

Exemples de moviments originals:
- "Harmonisme Celestial" (cultura religiosa científica)
- "Moviment de les Formes Naturals" (cultura natural i artística)
- "Expressionisme de Guerra" (cultura militarista post-conflicte)

Respon NOMÉS en format JSON (sense markdown):
{{
"nom": "nom original del moviment",
"formes_art": ["arquitectura", "pintura", "música"],
"filosofia": "filosofia central del moviment (1-2 frases)",
"caracteristiques": ["característica1", "característica2", "característica3"],
"influencia": "1-100 (influència cultural del moviment)"
}}"""

        result = self.ai_system.generate_with_civ_model(
            civilization_name=civilization_name,
            prompt=prompt
        )

        if not result:
            return None

        try:
            # Parseja art forms
            art_forms = []
            art_form_map = {
                'arquitectura': ArtForm.ARCHITECTURE,
                'escultura': ArtForm.SCULPTURE,
                'pintura': ArtForm.PAINTING,
                'música': ArtForm.MUSIC,
                'música': ArtForm.MUSIC,
                'literatura': ArtForm.LITERATURE,
                'teatre': ArtForm.THEATER,
                'dansa': ArtForm.DANCE,
                'poesia': ArtForm.POETRY
            }

            for form_name in result.get('formes_art', []):
                form_name_lower = form_name.lower()
                if form_name_lower in art_form_map:
                    art_forms.append(art_form_map[form_name_lower])

            if not art_forms:
                art_forms = [ArtForm.PAINTING, ArtForm.MUSIC]

            movement = CulturalMovement(
                name=result.get('nom', f'Moviment Cultural de {civilization_name}'),
                civilization=civilization_name,
                year_started=year,
                art_forms=art_forms,
                philosophy=result.get('filosofia', ''),
                key_characteristics=result.get('caracteristiques', []),
                influence_score=int(result.get('influencia', 50))
            )

            self.movements.append(movement)
            return movement

        except Exception as e:
            print(f"⚠️  Error creant CulturalMovement: {e}")
            return None

    def _generate_movement_procedural(
        self,
        civilization_name: str,
        year: int,
        culture_traits: Dict
    ) -> CulturalMovement:
        """Genera moviment cultural proceduralment"""

        # Noms basats en cultura
        art_level = culture_traits.get('art', 50)
        religion_level = culture_traits.get('religion', 50)
        science_level = culture_traits.get('science', 50)

        if art_level > 70:
            prefixes = ["Neo", "Trans", "Ultra", "Post"]
            roots = ["Expressionisme", "Realisme", "Naturalisme", "Minimalisme"]
        elif religion_level > 70:
            prefixes = ["Sagrat", "Diví", "Celestial", "Místic"]
            roots = ["Art", "Harmonisme", "Simbolisme"]
        elif science_level > 70:
            prefixes = ["Racional", "Lògic", "Abstracte", "Geomètric"]
            roots = ["Constructivisme", "Funcionalisme"]
        else:
            prefixes = ["Nou", "Gran", "Primer"]
            roots = ["Moviment", "Corrent", "Escola"]

        name = f"{random.choice(prefixes)} {random.choice(roots)}"

        # Formes d'art
        art_forms = random.sample(list(ArtForm), random.randint(2, 4))

        # Filosofia
        if art_level > religion_level and art_level > science_level:
            philosophy = "L'art com a expressió suprema de l'esperit humà"
        elif religion_level > science_level:
            philosophy = "La bellesa com a reflex del diví"
        else:
            philosophy = "La forma segueix la funció i la raó"

        movement = CulturalMovement(
            name=name,
            civilization=civilization_name,
            year_started=year,
            art_forms=art_forms,
            philosophy=philosophy,
            key_characteristics=[
                "Innovador",
                "Distintiu",
                "Influential"
            ],
            influence_score=random.randint(30, 80)
        )

        self.movements.append(movement)
        return movement

    def generate_artistic_work(
        self,
        civilization_name: str,
        year: int,
        movement: Optional[CulturalMovement],
        culture_traits: Dict,
        use_ai: bool = True
    ) -> Optional[ArtisticWork]:
        """
        Genera una obra d'art amb IA

        Args:
            civilization_name: Civilització
            year: Any de creació
            movement: Moviment cultural (opcional)
            culture_traits: Trets culturals
            use_ai: Si usar IA

        Returns:
            ArtisticWork generada
        """
        if use_ai and movement:
            work = self._generate_work_with_ai(
                civilization_name,
                year,
                movement,
                culture_traits
            )

            if work:
                self.artworks.append(work)
                movement.major_works.append(work)
                return work

        # Fallback procedural
        return self._generate_work_procedural(
            civilization_name,
            year,
            movement
        )

    def _generate_work_with_ai(
        self,
        civilization_name: str,
        year: int,
        movement: CulturalMovement,
        culture_traits: Dict
    ) -> Optional[ArtisticWork]:
        """Genera obra d'art amb IA"""

        art_form = random.choice(movement.art_forms)

        prompt = f"""Genera una obra d'art mestre per la civilització {civilization_name}.

CONTEXT:
Moviment cultural: {movement.name}
Filosofia del moviment: {movement.philosophy}
Forma d'art: {art_form.value}
Any: {year}

INSTRUCCIONS:
Crea una obra d'art ORIGINAL i MEMORABLE dins del moviment "{movement.name}".
Títol creatiu, artista inventat, descripció evocadora.

Respon en JSON (sense markdown):
{{
"titol": "títol creatiu de l'obra",
"artista": "nom de l'artista inventor",
"descripcio": "descripció de l'obra (2-3 frases)",
"temes": ["tema1", "tema2"],
"impacte": "1-10 (impacte cultural)"
}}"""

        result = self.ai_system.generate_with_civ_model(
            civilization_name=civilization_name,
            prompt=prompt
        )

        if not result:
            return None

        try:
            work = ArtisticWork(
                title=result.get('titol', 'Obra Sense Títol'),
                art_form=art_form,
                creator=result.get('artista', 'Artista Desconegut'),
                year_created=year,
                civilization=civilization_name,
                description=result.get('descripcio', ''),
                cultural_impact=int(result.get('impacte', 5)),
                themes=result.get('temes', [])
            )

            self.artworks.append(work)
            return work

        except Exception as e:
            print(f"⚠️  Error creant ArtisticWork: {e}")
            return None

    def _generate_work_procedural(
        self,
        civilization_name: str,
        year: int,
        movement: Optional[CulturalMovement]
    ) -> ArtisticWork:
        """Genera obra proceduralment"""

        if movement:
            art_form = random.choice(movement.art_forms)
            title = f"{movement.name} Opus {random.randint(1, 100)}"
        else:
            art_form = random.choice(list(ArtForm))
            title = f"Obra de {civilization_name}"

        # Artista procedural
        prefixes = ["Gran", "Mestre", "Savi"]
        suffixes = ["or", "ix", "el", "ar", "on"]
        artist = f"{random.choice(prefixes)} {civilization_name[:4]}{random.choice(suffixes)}"

        work = ArtisticWork(
            title=title,
            art_form=art_form,
            creator=artist,
            year_created=year,
            civilization=civilization_name,
            description=f"Una obra notable del període {year}",
            cultural_impact=random.randint(3, 8),
            themes=["bellesa", "poder", "natura"]
        )

        self.artworks.append(work)
        return work

    def get_movements_by_civilization(self, civilization_name: str) -> List[CulturalMovement]:
        """Obté moviments d'una civilització"""
        return [m for m in self.movements if m.civilization == civilization_name]

    def get_statistics(self) -> Dict:
        """Obté estadístiques culturals"""
        return {
            'total_movements': len(self.movements),
            'total_artworks': len(self.artworks),
            'art_forms_distribution': self._get_art_form_distribution(),
            'top_movements': sorted(
                self.movements,
                key=lambda m: m.influence_score,
                reverse=True
            )[:5]
        }

    def _get_art_form_distribution(self) -> Dict[str, int]:
        """Distribució de formes d'art"""
        distribution = {}

        for work in self.artworks:
            form = work.art_form.value
            distribution[form] = distribution.get(form, 0) + 1

        return distribution
