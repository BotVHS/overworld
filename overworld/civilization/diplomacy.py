"""
Diplomacy System - Sistema de diplomàcia i relacions internacionals

Gestiona relacions entre civilitzacions, tractats, aliances i conflictes
"""
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import random


class RelationshipType(Enum):
    """Tipus de relació entre civilitzacions"""
    ALLY = "ally"                    # Aliats (defensiu o ofensiu)
    FRIENDLY = "friendly"            # Amistós
    NEUTRAL = "neutral"              # Neutral
    UNFRIENDLY = "unfriendly"       # Poc amistós
    HOSTILE = "hostile"              # Hostil
    AT_WAR = "at_war"               # En guerra


class TreatyType(Enum):
    """Tipus de tractats"""
    PEACE_TREATY = "peace_treaty"
    TRADE_AGREEMENT = "trade_agreement"
    DEFENSIVE_PACT = "defensive_pact"
    MILITARY_ALLIANCE = "military_alliance"
    NON_AGGRESSION = "non_aggression"
    VASSALAGE = "vassalage"
    CULTURAL_EXCHANGE = "cultural_exchange"


class DiplomaticAction(Enum):
    """Accions diplomàtiques possibles"""
    DECLARE_WAR = "declare_war"
    PROPOSE_PEACE = "propose_peace"
    FORM_ALLIANCE = "form_alliance"
    BREAK_ALLIANCE = "break_alliance"
    SEND_GIFT = "send_gift"
    DEMAND_TRIBUTE = "demand_tribute"
    DENOUNCE = "denounce"
    PRAISE = "praise"
    REQUEST_MILITARY_AID = "request_military_aid"
    PROPOSE_TRADE = "propose_trade"


@dataclass
class Treaty:
    """
    Un tractat entre dues o més civilitzacions
    """
    treaty_type: TreatyType
    participants: List[str]  # Noms de civilitzacions
    year_signed: int
    duration_years: int  # -1 = permanent
    terms: Dict = field(default_factory=dict)
    broken: bool = False

    def is_active(self, current_year: int) -> bool:
        """Comprova si el tractat està actiu"""
        if self.broken:
            return False
        if self.duration_years == -1:
            return True
        return (current_year - self.year_signed) < self.duration_years

    def involves(self, civ_name: str) -> bool:
        """Comprova si una civilització participa en el tractat"""
        return civ_name in self.participants


@dataclass
class DiplomaticRelationship:
    """
    Relació diplomàtica entre dues civilitzacions
    """
    civ1_name: str
    civ2_name: str
    relationship_type: RelationshipType = RelationshipType.NEUTRAL
    opinion_score: int = 0  # -100 a +100
    treaties: List[Treaty] = field(default_factory=list)
    history: List[str] = field(default_factory=list)  # Històric d'interaccions

    def add_history_event(self, year: int, event: str):
        """Afegeix esdeveniment a l'històric"""
        self.history.append(f"Any {year}: {event}")

    def modify_opinion(self, delta: int):
        """Modifica l'opinió entre civilitzacions"""
        self.opinion_score = max(-100, min(100, self.opinion_score + delta))

        # Actualitza tipus de relació segons opinió
        if self.opinion_score >= 60:
            self.relationship_type = RelationshipType.FRIENDLY
        elif self.opinion_score >= 30:
            self.relationship_type = RelationshipType.NEUTRAL
        elif self.opinion_score >= -30:
            self.relationship_type = RelationshipType.UNFRIENDLY
        else:
            self.relationship_type = RelationshipType.HOSTILE

    def has_active_treaty(self, treaty_type: TreatyType, current_year: int) -> bool:
        """Comprova si té un tractat actiu d'un tipus"""
        return any(
            t.treaty_type == treaty_type and t.is_active(current_year)
            for t in self.treaties
        )

    def get_relationship_description(self) -> str:
        """Obté descripció de la relació"""
        descriptions = {
            RelationshipType.ALLY: "Aliats",
            RelationshipType.FRIENDLY: "Amistós",
            RelationshipType.NEUTRAL: "Neutral",
            RelationshipType.UNFRIENDLY: "Tens",
            RelationshipType.HOSTILE: "Hostil",
            RelationshipType.AT_WAR: "En guerra"
        }
        return descriptions.get(self.relationship_type, "Desconegut")


class DiplomacySystem:
    """
    Sistema de diplomàcia i relacions internacionals
    """

    def __init__(self):
        self.relationships: Dict[Tuple[str, str], DiplomaticRelationship] = {}
        self.all_treaties: List[Treaty] = []
        self.diplomatic_events: List[Dict] = []

    def _get_relationship_key(self, civ1_name: str, civ2_name: str) -> Tuple[str, str]:
        """Obté clau normalitzada per relació"""
        return tuple(sorted([civ1_name, civ2_name]))

    def get_relationship(
        self,
        civ1_name: str,
        civ2_name: str
    ) -> DiplomaticRelationship:
        """Obté relació entre dues civilitzacions"""
        key = self._get_relationship_key(civ1_name, civ2_name)

        if key not in self.relationships:
            # Crea relació nova
            self.relationships[key] = DiplomaticRelationship(
                civ1_name=civ1_name,
                civ2_name=civ2_name
            )

        return self.relationships[key]

    def set_relationship(
        self,
        civ1_name: str,
        civ2_name: str,
        relationship_type: RelationshipType,
        opinion_score: Optional[int] = None
    ):
        """Estableix relació entre civilitzacions"""
        relationship = self.get_relationship(civ1_name, civ2_name)
        relationship.relationship_type = relationship_type

        if opinion_score is not None:
            relationship.opinion_score = opinion_score

    def sign_treaty(
        self,
        treaty_type: TreatyType,
        participants: List[str],
        year: int,
        duration_years: int = -1,
        terms: Optional[Dict] = None
    ) -> Treaty:
        """
        Signa un tractat entre civilitzacions

        Args:
            treaty_type: Tipus de tractat
            participants: Civilitzacions participants
            year: Any de signatura
            duration_years: Duració (-1 = permanent)
            terms: Termes específics del tractat

        Returns:
            Treaty signat
        """
        treaty = Treaty(
            treaty_type=treaty_type,
            participants=participants,
            year_signed=year,
            duration_years=duration_years,
            terms=terms or {}
        )

        self.all_treaties.append(treaty)

        # Afegeix tractat a relacions bilaterals
        if len(participants) == 2:
            relationship = self.get_relationship(participants[0], participants[1])
            relationship.treaties.append(treaty)

            # Millora opinió
            if treaty_type in [TreatyType.PEACE_TREATY, TreatyType.TRADE_AGREEMENT]:
                relationship.modify_opinion(20)
            elif treaty_type in [TreatyType.DEFENSIVE_PACT, TreatyType.MILITARY_ALLIANCE]:
                relationship.modify_opinion(40)
                relationship.relationship_type = RelationshipType.ALLY

            # Registra esdeveniment
            relationship.add_history_event(year, f"Tractat signat: {treaty_type.value}")

        # Registra esdeveniment global
        self.diplomatic_events.append({
            'year': year,
            'type': 'treaty_signed',
            'treaty_type': treaty_type.value,
            'participants': participants
        })

        return treaty

    def break_treaty(self, treaty: Treaty, year: int, breaker: str):
        """Trenca un tractat"""
        treaty.broken = True

        # Penalitza opinió amb tots els participants
        for participant in treaty.participants:
            if participant != breaker:
                relationship = self.get_relationship(breaker, participant)
                relationship.modify_opinion(-50)
                relationship.add_history_event(year, f"{breaker} va trencar {treaty.treaty_type.value}")

        # Registra esdeveniment
        self.diplomatic_events.append({
            'year': year,
            'type': 'treaty_broken',
            'treaty_type': treaty.treaty_type.value,
            'breaker': breaker
        })

    def declare_war(
        self,
        aggressor: str,
        defender: str,
        year: int,
        casus_belli: str = "Expansió territorial"
    ):
        """Declara guerra entre civilitzacions"""
        relationship = self.get_relationship(aggressor, defender)
        relationship.relationship_type = RelationshipType.AT_WAR
        relationship.opinion_score = -100
        relationship.add_history_event(year, f"{aggressor} va declarar guerra: {casus_belli}")

        # Registra esdeveniment
        self.diplomatic_events.append({
            'year': year,
            'type': 'war_declared',
            'aggressor': aggressor,
            'defender': defender,
            'casus_belli': casus_belli
        })

    def make_peace(
        self,
        civ1_name: str,
        civ2_name: str,
        year: int,
        terms: Optional[Dict] = None
    ) -> Treaty:
        """Signa tractat de pau"""
        relationship = self.get_relationship(civ1_name, civ2_name)
        relationship.relationship_type = RelationshipType.NEUTRAL
        relationship.modify_opinion(30)
        relationship.add_history_event(year, "Tractat de pau signat")

        # Crea tractat de pau
        peace_treaty = self.sign_treaty(
            treaty_type=TreatyType.PEACE_TREATY,
            participants=[civ1_name, civ2_name],
            year=year,
            duration_years=10,  # 10 anys de pau
            terms=terms
        )

        return peace_treaty

    def get_allies(self, civ_name: str, current_year: int) -> List[str]:
        """Obté llista d'aliats d'una civilització"""
        allies = []

        for key, relationship in self.relationships.items():
            if civ_name in key:
                other_civ = key[0] if key[1] == civ_name else key[1]

                # Comprova si són aliats
                if relationship.relationship_type == RelationshipType.ALLY:
                    allies.append(other_civ)
                elif relationship.has_active_treaty(TreatyType.MILITARY_ALLIANCE, current_year):
                    allies.append(other_civ)

        return allies

    def get_enemies(self, civ_name: str) -> List[str]:
        """Obté llista d'enemics d'una civilització"""
        enemies = []

        for key, relationship in self.relationships.items():
            if civ_name in key:
                other_civ = key[0] if key[1] == civ_name else key[1]

                if relationship.relationship_type in [RelationshipType.HOSTILE, RelationshipType.AT_WAR]:
                    enemies.append(other_civ)

        return enemies

    def is_at_war(self, civ1_name: str, civ2_name: str) -> bool:
        """Comprova si dues civilitzacions estan en guerra"""
        relationship = self.get_relationship(civ1_name, civ2_name)
        return relationship.relationship_type == RelationshipType.AT_WAR

    def calculate_diplomatic_power(
        self,
        civ_name: str,
        all_civilizations: List
    ) -> float:
        """
        Calcula poder diplomàtic d'una civilització

        Args:
            civ_name: Nom de la civilització
            all_civilizations: Llista de totes les civilitzacions

        Returns:
            Score de poder diplomàtic (0.0-10.0)
        """
        score = 0.0

        # Aliances (+1 per aliança)
        allies = self.get_allies(civ_name, 2000)  # Any fictici
        score += len(allies) * 1.0

        # Relacions positives (+0.5 per relació amistosa)
        for key, relationship in self.relationships.items():
            if civ_name in key and relationship.opinion_score > 30:
                score += 0.5

        # Tractat comercials actius (+0.3)
        active_trade_treaties = sum(
            1 for treaty in self.all_treaties
            if treaty.involves(civ_name) and
            treaty.treaty_type == TreatyType.TRADE_AGREEMENT and
            treaty.is_active(2000)
        )
        score += active_trade_treaties * 0.3

        # Enemics (penalització -0.5)
        enemies = self.get_enemies(civ_name)
        score -= len(enemies) * 0.5

        return max(0.0, min(10.0, score))

    def get_relationship_matrix(self, civilization_names: List[str]) -> Dict:
        """
        Obté matriu de relacions entre totes les civilitzacions

        Returns:
            Dict amb relacions
        """
        matrix = {}

        for civ1 in civilization_names:
            matrix[civ1] = {}
            for civ2 in civilization_names:
                if civ1 == civ2:
                    matrix[civ1][civ2] = None
                else:
                    relationship = self.get_relationship(civ1, civ2)
                    matrix[civ1][civ2] = {
                        'type': relationship.relationship_type.value,
                        'opinion': relationship.opinion_score
                    }

        return matrix

    def get_statistics(self) -> Dict:
        """Obté estadístiques del sistema diplomàtic"""
        total_relationships = len(self.relationships)

        relationship_counts = {rt.value: 0 for rt in RelationshipType}
        for rel in self.relationships.values():
            relationship_counts[rel.relationship_type.value] += 1

        active_treaties = sum(1 for t in self.all_treaties if not t.broken)
        broken_treaties = sum(1 for t in self.all_treaties if t.broken)

        return {
            'total_relationships': total_relationships,
            'relationship_types': relationship_counts,
            'total_treaties': len(self.all_treaties),
            'active_treaties': active_treaties,
            'broken_treaties': broken_treaties,
            'diplomatic_events': len(self.diplomatic_events)
        }
