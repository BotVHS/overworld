"""
Event System - Sistema avançat d'esdeveniments

Gestiona esdeveniments emergents, decisions de líders i història dinàmica
"""
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import random


class EventType(Enum):
    """Tipus d'esdeveniments"""
    # Naturals
    NATURAL_DISASTER = "desastre_natural"
    GOOD_HARVEST = "bona_collita"
    FAMINE = "fam"
    PLAGUE = "pesta"
    DISCOVERY = "descobriment"

    # Polítics
    LEADER_BORN = "naixement_líder"
    LEADER_DIED = "mort_líder"
    REVOLUTION = "revolució"
    REFORM = "reforma"
    COUP = "cop_d_estat"

    # Diplomàtics
    FIRST_CONTACT = "primer_contacte"
    ALLIANCE_FORMED = "aliança_formada"
    WAR_DECLARED = "guerra_declarada"
    PEACE_TREATY = "tractat_pau"
    TRADE_AGREEMENT = "acord_comercial"

    # Socials
    POPULATION_BOOM = "boom_poblacional"
    MIGRATION = "migració"
    CULTURAL_RENAISSANCE = "renaixement_cultural"
    RELIGIOUS_SCHISM = "cisma_religiós"
    ECONOMIC_CRISIS = "crisi_econòmica"

    # Tecnològics
    TECH_BREAKTHROUGH = "avenç_tecnològic"
    WONDER_COMPLETED = "meravella_completada"

    # Militars
    BATTLE = "batalla"
    SIEGE = "setge"
    CONQUEST = "conquesta"
    REBELLION = "rebel·lió"


class EventPriority(Enum):
    """Prioritat d'un esdeveniment"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class GameEvent:
    """
    Un esdeveniment que ocorre durant la simulació
    """
    event_type: EventType
    year: int
    day: int
    title: str
    description: str
    affected_civilizations: List[str] = field(default_factory=list)
    priority: EventPriority = EventPriority.MEDIUM
    consequences: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)

    def __str__(self) -> str:
        return f"[Any {self.year}, Dia {self.day}] {self.title}: {self.description}"

    def to_dict(self) -> Dict:
        """Serialitza l'esdeveniment"""
        return {
            'event_type': self.event_type.value,
            'year': self.year,
            'day': self.day,
            'title': self.title,
            'description': self.description,
            'affected_civilizations': self.affected_civilizations,
            'priority': self.priority.value,
            'consequences': self.consequences,
            'metadata': self.metadata
        }


@dataclass
class EventGenerator:
    """
    Configuració per generar esdeveniments aleatoris
    """
    event_type: EventType
    probability_per_year: float  # 0.0-1.0, probabilitat que passi cada any
    condition: Optional[Callable] = None  # Funció que retorna bool per condició
    generator: Optional[Callable] = None  # Funció que genera l'esdeveniment


class AdvancedEventSystem:
    """
    Sistema avançat d'esdeveniments

    Gestiona:
    - Esdeveniments emergents aleatoris
    - Història dinàmica de les civilitzacions
    - Trigger de decisions de líders
    - Conseqüències d'esdeveniments
    """

    def __init__(self):
        self.events: List[GameEvent] = []
        self.event_generators: List[EventGenerator] = []
        self.listeners: Dict[EventType, List[Callable]] = {}

        # Registra generadors per defecte
        self._register_default_generators()

    def _register_default_generators(self):
        """Registra generadors d'esdeveniments per defecte"""

        # Desastres naturals (5% per any)
        self.register_generator(
            EventGenerator(
                event_type=EventType.NATURAL_DISASTER,
                probability_per_year=0.05,
                generator=self._generate_natural_disaster
            )
        )

        # Bones collites (15% per any)
        self.register_generator(
            EventGenerator(
                event_type=EventType.GOOD_HARVEST,
                probability_per_year=0.15,
                generator=self._generate_good_harvest
            )
        )

        # Fam (3% per any)
        self.register_generator(
            EventGenerator(
                event_type=EventType.FAMINE,
                probability_per_year=0.03,
                generator=self._generate_famine
            )
        )

        # Descobriments (10% per any)
        self.register_generator(
            EventGenerator(
                event_type=EventType.DISCOVERY,
                probability_per_year=0.10,
                generator=self._generate_discovery
            )
        )

        # Boom poblacional (8% per any)
        self.register_generator(
            EventGenerator(
                event_type=EventType.POPULATION_BOOM,
                probability_per_year=0.08,
                generator=self._generate_population_boom
            )
        )

        # Crisis econòmica (5% per any)
        self.register_generator(
            EventGenerator(
                event_type=EventType.ECONOMIC_CRISIS,
                probability_per_year=0.05,
                generator=self._generate_economic_crisis
            )
        )

    def register_generator(self, generator: EventGenerator):
        """Registra un generador d'esdeveniments"""
        self.event_generators.append(generator)

    def subscribe(self, event_type: EventType, callback: Callable):
        """Subscriu un callback a un tipus d'esdeveniment"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def emit_event(self, event: GameEvent):
        """Emet un esdeveniment i notifica els listeners"""
        self.events.append(event)

        # Notifica listeners
        if event.event_type in self.listeners:
            for callback in self.listeners[event.event_type]:
                callback(event)

    def simulate_year(
        self,
        year: int,
        civilizations: List,
        context: Dict = None
    ) -> List[GameEvent]:
        """
        Simula un any complet i genera esdeveniments

        Args:
            year: Any actual
            civilizations: Llista de civilitzacions
            context: Context addicional (món, ecosistema, etc.)

        Returns:
            Llista d'esdeveniments generats aquest any
        """
        year_events = []

        for generator in self.event_generators:
            # Comprova condició si existeix
            if generator.condition and not generator.condition(civilizations, context):
                continue

            # Comprova probabilitat
            if random.random() < generator.probability_per_year:
                # Genera esdeveniment
                if generator.generator:
                    event = generator.generator(year, civilizations, context)
                    if event:
                        self.emit_event(event)
                        year_events.append(event)

        return year_events

    # === GENERADORS D'ESDEVENIMENTS ===

    def _generate_natural_disaster(
        self,
        year: int,
        civilizations: List,
        context: Dict
    ) -> Optional[GameEvent]:
        """Genera un desastre natural"""
        if not civilizations:
            return None

        civ = random.choice(civilizations)
        disaster_types = [
            ("terratrèmol", "Un fort terratrèmol ha sacsejat"),
            ("inundació", "Rius desbordats han inundat"),
            ("erupció volcànica", "Un volcà ha entrat en erupció a prop de"),
            ("huracà", "Un huracà devastador ha colpejat"),
            ("sequera", "Una sequera severa ha assecat")
        ]

        disaster_type, description = random.choice(disaster_types)

        return GameEvent(
            event_type=EventType.NATURAL_DISASTER,
            year=year,
            day=random.randint(1, 365),
            title=f"{disaster_type.capitalize()} a {civ.name}",
            description=f"{description} {civ.name}",
            affected_civilizations=[civ.name],
            priority=EventPriority.HIGH,
            consequences={
                'population_loss': random.randint(5, 20),  # % de població
                'infrastructure_damage': random.randint(10, 40)
            },
            metadata={'disaster_type': disaster_type}
        )

    def _generate_good_harvest(
        self,
        year: int,
        civilizations: List,
        context: Dict
    ) -> Optional[GameEvent]:
        """Genera una bona collita"""
        if not civilizations:
            return None

        civ = random.choice(civilizations)

        return GameEvent(
            event_type=EventType.GOOD_HARVEST,
            year=year,
            day=random.randint(200, 300),  # Tardor
            title=f"Collita excepcional a {civ.name}",
            description=f"Els camps de {civ.name} han donat una collita abundant",
            affected_civilizations=[civ.name],
            priority=EventPriority.LOW,
            consequences={
                'food_surplus': random.randint(20, 50),
                'population_growth': random.randint(1, 5)
            }
        )

    def _generate_famine(
        self,
        year: int,
        civilizations: List,
        context: Dict
    ) -> Optional[GameEvent]:
        """Genera una fam"""
        if not civilizations:
            return None

        civ = random.choice(civilizations)

        causes = [
            "La mala collita",
            "La sequera",
            "Les plagues d'insectes",
            "La guerra"
        ]

        cause = random.choice(causes)

        return GameEvent(
            event_type=EventType.FAMINE,
            year=year,
            day=random.randint(1, 365),
            title=f"Fam a {civ.name}",
            description=f"{cause} ha causat fam a {civ.name}",
            affected_civilizations=[civ.name],
            priority=EventPriority.CRITICAL,
            consequences={
                'population_loss': random.randint(10, 30),
                'unrest': random.randint(20, 50)
            },
            metadata={'cause': cause}
        )

    def _generate_discovery(
        self,
        year: int,
        civilizations: List,
        context: Dict
    ) -> Optional[GameEvent]:
        """Genera un descobriment"""
        if not civilizations:
            return None

        civ = random.choice(civilizations)

        discoveries = [
            ("nous jaciments d'or", "recursos"),
            ("una terra fèrtil inexplorada", "territori"),
            ("una ruta comercial lucrativa", "comerç"),
            ("ruïnes antigues amb coneixements perduts", "coneixement"),
            ("una nova tècnica agrícola", "agricultura")
        ]

        discovery, category = random.choice(discoveries)

        return GameEvent(
            event_type=EventType.DISCOVERY,
            year=year,
            day=random.randint(1, 365),
            title=f"Descobriment a {civ.name}",
            description=f"{civ.name} ha descobert {discovery}",
            affected_civilizations=[civ.name],
            priority=EventPriority.MEDIUM,
            consequences={
                'prosperity_bonus': random.randint(5, 20)
            },
            metadata={'discovery_category': category}
        )

    def _generate_population_boom(
        self,
        year: int,
        civilizations: List,
        context: Dict
    ) -> Optional[GameEvent]:
        """Genera un boom poblacional"""
        if not civilizations:
            return None

        civ = random.choice(civilizations)

        return GameEvent(
            event_type=EventType.POPULATION_BOOM,
            year=year,
            day=random.randint(1, 365),
            title=f"Creixement poblacional a {civ.name}",
            description=f"La població de {civ.name} ha crescut significativament",
            affected_civilizations=[civ.name],
            priority=EventPriority.LOW,
            consequences={
                'population_growth': random.randint(10, 25)
            }
        )

    def _generate_economic_crisis(
        self,
        year: int,
        civilizations: List,
        context: Dict
    ) -> Optional[GameEvent]:
        """Genera una crisi econòmica"""
        if not civilizations:
            return None

        civ = random.choice(civilizations)

        causes = [
            "Col·lapse del comerç",
            "Inflació descontrolada",
            "Deutes excessius",
            "Corrupció generalitzada"
        ]

        cause = random.choice(causes)

        return GameEvent(
            event_type=EventType.ECONOMIC_CRISIS,
            year=year,
            day=random.randint(1, 365),
            title=f"Crisi econòmica a {civ.name}",
            description=f"{cause} ha causat una crisi econòmica a {civ.name}",
            affected_civilizations=[civ.name],
            priority=EventPriority.HIGH,
            consequences={
                'economic_penalty': random.randint(15, 40),
                'unrest': random.randint(10, 30)
            },
            metadata={'cause': cause}
        )

    def get_history(
        self,
        civilization_name: Optional[str] = None,
        event_type: Optional[EventType] = None,
        limit: int = 50
    ) -> List[GameEvent]:
        """
        Obté l'històric d'esdeveniments

        Args:
            civilization_name: Filtra per civilització (None = tots)
            event_type: Filtra per tipus d'esdeveniment (None = tots)
            limit: Nombre màxim d'esdeveniments a retornar

        Returns:
            Llista d'esdeveniments
        """
        filtered = self.events

        if civilization_name:
            filtered = [
                e for e in filtered
                if civilization_name in e.affected_civilizations
            ]

        if event_type:
            filtered = [
                e for e in filtered
                if e.event_type == event_type
            ]

        # Ordena per any descendent
        filtered.sort(key=lambda e: (e.year, e.day), reverse=True)

        return filtered[:limit]

    def get_statistics(self) -> Dict:
        """Obté estadístiques dels esdeveniments"""
        stats = {
            'total_events': len(self.events),
            'by_type': {},
            'by_priority': {},
            'events_per_year': {}
        }

        for event in self.events:
            # Per tipus
            event_type_name = event.event_type.value
            stats['by_type'][event_type_name] = stats['by_type'].get(event_type_name, 0) + 1

            # Per prioritat
            priority_name = event.priority.name
            stats['by_priority'][priority_name] = stats['by_priority'].get(priority_name, 0) + 1

            # Per any
            stats['events_per_year'][event.year] = stats['events_per_year'].get(event.year, 0) + 1

        return stats
