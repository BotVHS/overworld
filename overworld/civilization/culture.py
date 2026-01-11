"""
Culture - Sistema de cultura i trets culturals

Defineix trets culturals que evolucionen segons l'entorn
"""
from typing import Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
import random


class CulturalArchetype(Enum):
    """Arquetips culturals base segons entorn"""
    WARRIOR = "warrior"           # Entorns hostils
    PEACEFUL = "peaceful"         # Entorns fèrtils i tranquils
    MARITIME = "maritime"         # Entorns costaners/illes
    JUNGLE = "jungle"             # Jungles
    MOUNTAIN = "mountain"         # Muntanyes
    DESERT = "desert"             # Deserts
    NOMADIC = "nomadic"           # Estepes, savanes
    BALANCED = "balanced"         # Equilibrat


@dataclass
class CulturalTraits:
    """
    Trets culturals d'una civilització

    Cada tret és un valor entre 0-100 que indica la intensitat
    """
    # Trets principals
    militarism: float = 50.0      # Militarisme (0=pacifista, 100=guerrer)
    commerce: float = 50.0        # Comerç
    science: float = 50.0         # Ciència i coneixement
    religion: float = 50.0        # Religiositat
    art: float = 50.0            # Art i cultura
    agriculture: float = 50.0     # Agricultura

    # Trets socials
    authoritarianism: float = 50.0  # Autoritarisme (0=democràcia, 100=dictadura)
    collectivism: float = 50.0      # Col·lectivisme (0=individualisme, 100=col·lectivisme)
    expansionism: float = 50.0      # Expansionisme territorial
    isolationism: float = 50.0      # Aïllacionisme

    # Trets especials
    navigation: float = 50.0        # Navegació
    mining: float = 50.0           # Mineria
    craftsmanship: float = 50.0    # Artesania

    # Valors (no quantificables, són strings)
    core_values: list = field(default_factory=list)  # ["honor", "prosperitat", etc.]

    def to_dict(self) -> Dict:
        """Serialitza els trets culturals"""
        return {
            'militarism': self.militarism,
            'commerce': self.commerce,
            'science': self.science,
            'religion': self.religion,
            'art': self.art,
            'agriculture': self.agriculture,
            'authoritarianism': self.authoritarianism,
            'collectivism': self.collectivism,
            'expansionism': self.expansionism,
            'isolationism': self.isolationism,
            'navigation': self.navigation,
            'mining': self.mining,
            'craftsmanship': self.craftsmanship,
            'core_values': self.core_values
        }

    @staticmethod
    def from_dict(data: Dict) -> 'CulturalTraits':
        """Deserialitza els trets culturals"""
        return CulturalTraits(
            militarism=data.get('militarism', 50.0),
            commerce=data.get('commerce', 50.0),
            science=data.get('science', 50.0),
            religion=data.get('religion', 50.0),
            art=data.get('art', 50.0),
            agriculture=data.get('agriculture', 50.0),
            authoritarianism=data.get('authoritarianism', 50.0),
            collectivism=data.get('collectivism', 50.0),
            expansionism=data.get('expansionism', 50.0),
            isolationism=data.get('isolationism', 50.0),
            navigation=data.get('navigation', 50.0),
            mining=data.get('mining', 50.0),
            craftsmanship=data.get('craftsmanship', 50.0),
            core_values=data.get('core_values', [])
        )

    def get_archetype(self) -> CulturalArchetype:
        """Determina l'arquetip cultural dominant"""
        if self.militarism > 70:
            return CulturalArchetype.WARRIOR
        elif self.navigation > 70:
            return CulturalArchetype.MARITIME
        elif self.commerce > 70:
            return CulturalArchetype.PEACEFUL
        elif self.mining > 70:
            return CulturalArchetype.MOUNTAIN
        else:
            return CulturalArchetype.BALANCED


class CultureFactory:
    """
    Fàbrica per generar cultures segons l'entorn

    Implementa la lògica d'evolució cultural segons README
    """

    @staticmethod
    def create_from_environment(
        hostility: float,
        fertility: float,
        is_coastal: bool,
        is_mountain: bool,
        is_desert: bool,
        is_jungle: bool,
        temperature: float,
        humidity: float
    ) -> CulturalTraits:
        """
        Crea trets culturals adaptats a l'entorn

        Args:
            hostility: Índex d'hostilitat (0-10)
            fertility: Índex de fertilitat (0-10)
            is_coastal: Si és zona costanera
            is_mountain: Si és muntanya
            is_desert: Si és desert
            is_jungle: Si és jungla
            temperature: Temperatura (0-1)
            humidity: Humitat (0-1)

        Returns:
            Trets culturals generats
        """
        culture = CulturalTraits()

        # === ENTORNS HOSTILS (deserts, tundra, muntanyes altes, zones amb depredadors) ===
        if hostility > 7:
            culture.militarism = 70 + random.uniform(0, 20)      # Cultura guerrera
            culture.authoritarianism = 60 + random.uniform(0, 30) # Governs autoritaris
            culture.collectivism = 65 + random.uniform(0, 25)     # Col·lectivisme fort
            culture.science = 40 + random.uniform(0, 20)          # Menys ciència
            culture.art = 35 + random.uniform(0, 20)              # Menys art
            culture.expansionism = 60 + random.uniform(0, 30)     # Expansionisme agressiu
            culture.isolationism = 20 + random.uniform(0, 20)     # Poc aïllacionista
            culture.core_values = ["honor", "força", "supervivència", "disciplina", "sacrifici"]

        # === ENTORNS FÈRTILS I TRANQUILS (valls fluvials, planes temperades) ===
        elif fertility > 7 and hostility < 4:
            culture.militarism = 20 + random.uniform(0, 20)       # Pacifista
            culture.commerce = 70 + random.uniform(0, 20)         # Alt comerç
            culture.science = 60 + random.uniform(0, 30)          # Alta ciència
            culture.art = 65 + random.uniform(0, 25)              # Alt art
            culture.authoritarianism = 25 + random.uniform(0, 25) # Més democràtic
            culture.agriculture = 75 + random.uniform(0, 20)      # Alta agricultura
            culture.expansionism = 30 + random.uniform(0, 20)     # Poc expansionista
            culture.core_values = ["prosperitat", "coneixement", "art", "comerç", "llibertat"]

        # === ENTORNS MARÍTIMS (illes, costes) ===
        elif is_coastal:
            culture.navigation = 75 + random.uniform(0, 20)       # Alta navegació
            culture.commerce = 65 + random.uniform(0, 25)         # Alt comerç marítim
            culture.militarism = 45 + random.uniform(0, 30)       # Variable
            culture.expansionism = 55 + random.uniform(0, 25)     # Expansió marítima
            culture.isolationism = 25 + random.uniform(0, 20)     # Poc aïllacionista
            culture.authoritarianism = 40 + random.uniform(0, 30) # Variable
            culture.core_values = ["exploració", "aventura", "llibertat", "comerç"]

        # === ENTORNS DE JUNGLA ===
        elif is_jungle:
            culture.militarism = 55 + random.uniform(0, 20)       # Guerrilla
            culture.isolationism = 60 + random.uniform(0, 30)     # Aïllacionista
            culture.religion = 70 + random.uniform(0, 20)         # Molt religiós/xamànic
            culture.science = 35 + random.uniform(0, 20)          # Menys ciència formal
            culture.authoritarianism = 45 + random.uniform(0, 30) # Variable
            culture.core_values = ["harmonia", "tradició", "espiritualitat", "natura"]

        # === ENTORNS DE MUNTANYA ===
        elif is_mountain:
            culture.mining = 75 + random.uniform(0, 20)           # Alta mineria
            culture.militarism = 60 + random.uniform(0, 25)       # Defensius
            culture.craftsmanship = 70 + random.uniform(0, 20)    # Alta artesania
            culture.isolationism = 50 + random.uniform(0, 30)     # Moderadament aïllats
            culture.authoritarianism = 45 + random.uniform(0, 25) # Clans
            culture.core_values = ["resistència", "artesania", "tradició", "clans"]

        # === ENTORNS DE DESERT ===
        elif is_desert:
            culture.militarism = 55 + random.uniform(0, 25)       # Guerrers del desert
            culture.commerce = 60 + random.uniform(0, 25)         # Rutes comercials
            culture.religion = 65 + random.uniform(0, 25)         # Religiosos
            culture.authoritarianism = 55 + random.uniform(0, 30) # Tendència autoritària
            culture.navigation = 35 + random.uniform(0, 20)       # Navegació limitada
            culture.core_values = ["supervivència", "fe", "tradició", "comunitat"]

        # === BALANCED (per defecte) ===
        else:
            # Valors moderats amb variació
            culture.militarism = 40 + random.uniform(0, 30)
            culture.commerce = 45 + random.uniform(0, 30)
            culture.science = 45 + random.uniform(0, 30)
            culture.religion = 45 + random.uniform(0, 30)
            culture.art = 45 + random.uniform(0, 30)
            culture.agriculture = 50 + random.uniform(0, 30)
            culture.core_values = ["equilibri", "pragmatisme", "adaptació"]

        # Normalitza tots els valors a 0-100
        culture.militarism = max(0, min(100, culture.militarism))
        culture.commerce = max(0, min(100, culture.commerce))
        culture.science = max(0, min(100, culture.science))
        culture.religion = max(0, min(100, culture.religion))
        culture.art = max(0, min(100, culture.art))
        culture.agriculture = max(0, min(100, culture.agriculture))
        culture.authoritarianism = max(0, min(100, culture.authoritarianism))
        culture.collectivism = max(0, min(100, culture.collectivism))
        culture.expansionism = max(0, min(100, culture.expansionism))
        culture.isolationism = max(0, min(100, culture.isolationism))
        culture.navigation = max(0, min(100, culture.navigation))
        culture.mining = max(0, min(100, culture.mining))
        culture.craftsmanship = max(0, min(100, culture.craftsmanship))

        return culture

    @staticmethod
    def evolve_culture(
        current: CulturalTraits,
        years_passed: int,
        environmental_change: float = 0.0,
        major_events: list = None
    ) -> CulturalTraits:
        """
        Evoluciona una cultura al llarg del temps

        Args:
            current: Cultura actual
            years_passed: Anys transcorreguts
            environmental_change: Canvi ambiental (-1 a 1, 0=cap canvi)
            major_events: Esdeveniments majors que afecten la cultura

        Returns:
            Nova cultura evolucionada
        """
        # Copia la cultura actual
        new_culture = CulturalTraits(
            militarism=current.militarism,
            commerce=current.commerce,
            science=current.science,
            religion=current.religion,
            art=current.art,
            agriculture=current.agriculture,
            authoritarianism=current.authoritarianism,
            collectivism=current.collectivism,
            expansionism=current.expansionism,
            isolationism=current.isolationism,
            navigation=current.navigation,
            mining=current.mining,
            craftsmanship=current.craftsmanship,
            core_values=current.core_values.copy()
        )

        # Canvis gradualsper anys (deriva cultural natural)
        drift_rate = years_passed / 100.0  # Més anys = més deriva

        new_culture.militarism += random.gauss(0, drift_rate)
        new_culture.commerce += random.gauss(0, drift_rate)
        new_culture.science += random.gauss(0, drift_rate)
        new_culture.religion += random.gauss(0, drift_rate)
        new_culture.art += random.gauss(0, drift_rate)

        # Normalitza
        new_culture.militarism = max(0, min(100, new_culture.militarism))
        new_culture.commerce = max(0, min(100, new_culture.commerce))
        new_culture.science = max(0, min(100, new_culture.science))
        new_culture.religion = max(0, min(100, new_culture.religion))
        new_culture.art = max(0, min(100, new_culture.art))

        return new_culture
