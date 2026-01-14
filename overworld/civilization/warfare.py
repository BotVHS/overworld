"""
Warfare System - Sistema de guerra i conflictes militars

Gestiona guerres, batalles i forces militars
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random
from .diplomacy import DiplomacySystem


class WarStatus(Enum):
    """Estat d'una guerra"""
    ONGOING = "ongoing"          # En curs
    STALEMATE = "stalemate"      # Estancada
    DECISIVE = "decisive"        # Decisiva (un bàndol guanyant clarament)
    ENDED_PEACE = "ended_peace"  # Acabada amb pau
    ENDED_CONQUEST = "ended_conquest"  # Acabada amb conquesta


class BattleOutcome(Enum):
    """Resultat d'una batalla"""
    DECISIVE_VICTORY = "decisive_victory"
    VICTORY = "victory"
    PYRRHIC_VICTORY = "pyrrhic_victory"
    STALEMATE = "stalemate"
    DEFEAT = "defeat"


@dataclass
class MilitaryForce:
    """
    Força militar d'una civilització
    """
    civilization_name: str
    soldiers: int
    tech_level: int  # 0-8
    morale: int  # 0-100
    experience: int  # 0-100
    supply_level: int  # 0-100

    def get_military_strength(self) -> float:
        """
        Calcula força militar total

        Returns:
            Score de força (0.0-100.0+)
        """
        base_strength = self.soldiers * (1 + self.tech_level * 0.2)
        morale_mult = 0.5 + (self.morale / 100.0) * 0.5
        experience_mult = 0.7 + (self.experience / 100.0) * 0.3
        supply_mult = 0.5 + (self.supply_level / 100.0) * 0.5

        strength = base_strength * morale_mult * experience_mult * supply_mult

        return strength

    def apply_casualties(self, percentage: float):
        """Aplica baixes (0.0-1.0)"""
        casualties = int(self.soldiers * percentage)
        self.soldiers = max(0, self.soldiers - casualties)

        # Pèrdua de moral
        self.morale = max(0, self.morale - int(percentage * 50))

    def gain_experience(self, amount: int):
        """Guanya experiència"""
        self.experience = min(100, self.experience + amount)

    def restore_supply(self, amount: int):
        """Restaura subministraments"""
        self.supply_level = min(100, self.supply_level + amount)


@dataclass
class Battle:
    """
    Una batalla entre dues forces
    """
    year: int
    location: str
    attacker: str  # Nom civilització
    defender: str  # Nom civilització
    attacker_force: MilitaryForce
    defender_force: MilitaryForce
    outcome: Optional[BattleOutcome] = None
    victor: Optional[str] = None
    attacker_casualties: int = 0
    defender_casualties: int = 0
    description: str = ""

    def to_dict(self) -> Dict:
        """Serialitza la batalla"""
        return {
            'year': self.year,
            'location': self.location,
            'attacker': self.attacker,
            'defender': self.defender,
            'outcome': self.outcome.value if self.outcome else None,
            'victor': self.victor,
            'attacker_casualties': self.attacker_casualties,
            'defender_casualties': self.defender_casualties,
            'description': self.description
        }


@dataclass
class War:
    """
    Una guerra entre civilitzacions
    """
    war_id: int
    year_started: int
    aggressor: str
    defender: str
    casus_belli: str  # Causa de la guerra
    status: WarStatus = WarStatus.ONGOING
    battles: List[Battle] = field(default_factory=list)
    aggressor_warscore: int = 0  # -100 a +100
    year_ended: Optional[int] = None
    outcome: Optional[str] = None

    def add_battle(self, battle: Battle):
        """Afegeix batalla i actualitza warscore"""
        self.battles.append(battle)

        # Actualitza warscore segons resultat
        if battle.victor == self.aggressor:
            if battle.outcome == BattleOutcome.DECISIVE_VICTORY:
                self.aggressor_warscore += 20
            elif battle.outcome == BattleOutcome.VICTORY:
                self.aggressor_warscore += 10
            elif battle.outcome == BattleOutcome.PYRRHIC_VICTORY:
                self.aggressor_warscore += 5
        elif battle.victor == self.defender:
            if battle.outcome == BattleOutcome.DECISIVE_VICTORY:
                self.aggressor_warscore -= 20
            elif battle.outcome == BattleOutcome.VICTORY:
                self.aggressor_warscore -= 10
            elif battle.outcome == BattleOutcome.PYRRHIC_VICTORY:
                self.aggressor_warscore -= 5

        # Limita warscore
        self.aggressor_warscore = max(-100, min(100, self.aggressor_warscore))

        # Actualitza estat
        if abs(self.aggressor_warscore) > 70:
            self.status = WarStatus.DECISIVE
        elif abs(self.aggressor_warscore) < 10 and len(self.battles) > 3:
            self.status = WarStatus.STALEMATE
        else:
            self.status = WarStatus.ONGOING

    def get_duration(self, current_year: int) -> int:
        """Obté duració de la guerra"""
        end_year = self.year_ended if self.year_ended else current_year
        return end_year - self.year_started

    def is_active(self) -> bool:
        """Comprova si la guerra està activa"""
        return self.status == WarStatus.ONGOING or self.status == WarStatus.STALEMATE or self.status == WarStatus.DECISIVE

    def to_dict(self) -> Dict:
        """Serialitza la guerra"""
        return {
            'war_id': self.war_id,
            'year_started': self.year_started,
            'aggressor': self.aggressor,
            'defender': self.defender,
            'casus_belli': self.casus_belli,
            'status': self.status.value,
            'battles_count': len(self.battles),
            'aggressor_warscore': self.aggressor_warscore,
            'year_ended': self.year_ended,
            'outcome': self.outcome
        }


class WarfareSystem:
    """
    Sistema de guerra i conflictes militars
    """

    def __init__(self, diplomacy_system: DiplomacySystem):
        """
        Args:
            diplomacy_system: Sistema de diplomàcia
        """
        self.diplomacy = diplomacy_system
        self.wars: List[War] = []
        self.next_war_id = 1
        self.military_forces: Dict[str, MilitaryForce] = {}

    def register_military_force(
        self,
        civilization_name: str,
        soldiers: int,
        tech_level: int,
        morale: int = 50,
        experience: int = 0
    ) -> MilitaryForce:
        """Registra força militar d'una civilització"""
        force = MilitaryForce(
            civilization_name=civilization_name,
            soldiers=soldiers,
            tech_level=tech_level,
            morale=morale,
            experience=experience,
            supply_level=100
        )

        self.military_forces[civilization_name] = force
        return force

    def start_war(
        self,
        aggressor: str,
        defender: str,
        year: int,
        casus_belli: str = "Expansió territorial"
    ) -> War:
        """
        Inicia una guerra

        Args:
            aggressor: Civilització aggressora
            defender: Civilització defensora
            year: Any d'inici
            casus_belli: Causa de la guerra

        Returns:
            War creada
        """
        # Actualitza diplomàcia
        self.diplomacy.declare_war(aggressor, defender, year, casus_belli)

        # Crea guerra
        war = War(
            war_id=self.next_war_id,
            year_started=year,
            aggressor=aggressor,
            defender=defender,
            casus_belli=casus_belli
        )

        self.wars.append(war)
        self.next_war_id += 1

        return war

    def simulate_battle(
        self,
        war: War,
        year: int,
        location: str = "Frontera"
    ) -> Battle:
        """
        Simula una batalla

        Args:
            war: Guerra en curs
            year: Any de la batalla
            location: Localització

        Returns:
            Battle simulada
        """
        # Obté forces militars
        attacker_force = self.military_forces.get(war.aggressor)
        defender_force = self.military_forces.get(war.defender)

        if not attacker_force or not defender_force:
            raise ValueError("Forces militars no registrades")

        # Calcula forces
        attacker_strength = attacker_force.get_military_strength()
        defender_strength = defender_force.get_military_strength()

        # Bonus defensiu
        defender_strength *= 1.2

        # Determina victor i baixes
        total_strength = attacker_strength + defender_strength
        attacker_win_prob = attacker_strength / total_strength

        roll = random.random()

        if roll < attacker_win_prob:
            # Atacant guanya
            victor = war.aggressor
            strength_ratio = attacker_strength / defender_strength

            if strength_ratio > 2.0:
                outcome = BattleOutcome.DECISIVE_VICTORY
                attacker_casualties_pct = 0.05
                defender_casualties_pct = 0.30
            elif strength_ratio > 1.2:
                outcome = BattleOutcome.VICTORY
                attacker_casualties_pct = 0.10
                defender_casualties_pct = 0.20
            else:
                outcome = BattleOutcome.PYRRHIC_VICTORY
                attacker_casualties_pct = 0.15
                defender_casualties_pct = 0.15
        else:
            # Defensor guanya
            victor = war.defender
            strength_ratio = defender_strength / attacker_strength

            if strength_ratio > 2.0:
                outcome = BattleOutcome.DECISIVE_VICTORY
                defender_casualties_pct = 0.05
                attacker_casualties_pct = 0.30
            elif strength_ratio > 1.2:
                outcome = BattleOutcome.VICTORY
                defender_casualties_pct = 0.10
                attacker_casualties_pct = 0.20
            else:
                outcome = BattleOutcome.PYRRHIC_VICTORY
                defender_casualties_pct = 0.15
                attacker_casualties_pct = 0.15

        # Aplica baixes
        attacker_casualties = int(attacker_force.soldiers * attacker_casualties_pct)
        defender_casualties = int(defender_force.soldiers * defender_casualties_pct)

        attacker_force.apply_casualties(attacker_casualties_pct)
        defender_force.apply_casualties(defender_casualties_pct)

        # Guanya experiència
        attacker_force.gain_experience(10)
        defender_force.gain_experience(10)

        # Crea batalla
        battle = Battle(
            year=year,
            location=location,
            attacker=war.aggressor,
            defender=war.defender,
            attacker_force=attacker_force,
            defender_force=defender_force,
            outcome=outcome,
            victor=victor,
            attacker_casualties=attacker_casualties,
            defender_casualties=defender_casualties,
            description=f"Batalla de {location}: {victor} va guanyar ({outcome.value})"
        )

        # Afegeix batalla a guerra
        war.add_battle(battle)

        return battle

    def end_war(
        self,
        war: War,
        year: int,
        terms: Optional[Dict] = None
    ):
        """
        Finalitza una guerra

        Args:
            war: Guerra a finalitzar
            year: Any de finalització
            terms: Termes de pau
        """
        war.year_ended = year

        # Determina resultat segons warscore
        if war.aggressor_warscore > 50:
            war.status = WarStatus.ENDED_CONQUEST
            war.outcome = f"{war.aggressor} va conquistar territori"
        elif war.aggressor_warscore > 20:
            war.status = WarStatus.ENDED_PEACE
            war.outcome = f"{war.aggressor} va guanyar condicions favorables"
        elif war.aggressor_warscore > -20:
            war.status = WarStatus.ENDED_PEACE
            war.outcome = "Pau blanca (sense canvis territorials)"
        elif war.aggressor_warscore > -50:
            war.status = WarStatus.ENDED_PEACE
            war.outcome = f"{war.defender} va guanyar condicions favorables"
        else:
            war.status = WarStatus.ENDED_CONQUEST
            war.outcome = f"{war.defender} va reconquerir territori"

        # Signa tractat de pau
        self.diplomacy.make_peace(
            war.aggressor,
            war.defender,
            year,
            terms=terms
        )

    def get_active_wars(self) -> List[War]:
        """Obté llista de guerres actives"""
        return [war for war in self.wars if war.is_active()]

    def get_war_between(self, civ1_name: str, civ2_name: str) -> Optional[War]:
        """Obté guerra activa entre dues civilitzacions"""
        for war in self.get_active_wars():
            if (war.aggressor == civ1_name and war.defender == civ2_name) or \
               (war.aggressor == civ2_name and war.defender == civ1_name):
                return war
        return None

    def calculate_military_power(self, civ_name: str) -> float:
        """
        Calcula poder militar d'una civilització

        Returns:
            Score de poder militar (0.0-10.0)
        """
        force = self.military_forces.get(civ_name)
        if not force:
            return 0.0

        strength = force.get_military_strength()

        # Normalitza a 0-10
        # Assumeix que 50000 soldats amb tech 8 = 10.0
        max_strength = 50000 * (1 + 8 * 0.2) * 1.0 * 1.0 * 1.0  # ~130000
        score = (strength / max_strength) * 10.0

        return min(10.0, score)

    def get_statistics(self) -> Dict:
        """Obté estadístiques del sistema de guerra"""
        total_wars = len(self.wars)
        active_wars = len(self.get_active_wars())
        ended_wars = total_wars - active_wars

        total_battles = sum(len(war.battles) for war in self.wars)

        status_counts = {}
        for war in self.wars:
            status_counts[war.status.value] = status_counts.get(war.status.value, 0) + 1

        return {
            'total_wars': total_wars,
            'active_wars': active_wars,
            'ended_wars': ended_wars,
            'total_battles': total_battles,
            'war_statuses': status_counts,
            'registered_forces': len(self.military_forces)
        }
