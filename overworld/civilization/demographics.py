"""
Demographics System - Sistema demogràfic ultra-realista amb IA

Genera piràmides de població, migracions, taxes de natalitat/mortalitat amb Ollama
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import random
from ..ai.civilization_ai_models import CivilizationAISystem


class AgeGroup(Enum):
    """Grups d'edat per piràmide de població"""
    INFANT = "0-4"        # 0-4 anys
    CHILD = "5-14"        # 5-14 anys
    YOUTH = "15-24"       # 15-24 anys
    YOUNG_ADULT = "25-34" # 25-34 anys
    ADULT = "35-44"       # 35-44 anys
    MIDDLE_AGE = "45-54"  # 45-54 anys
    SENIOR = "55-64"      # 55-64 anys
    ELDERLY = "65+"       # 65+ anys


class MigrationReason(Enum):
    """Raons per migració"""
    ECONOMIC = "economic"           # Oportunitats econòmiques
    WAR = "war"                     # Guerra/conflicte
    FAMINE = "famine"               # Fam/desastre
    RELIGIOUS = "religious"         # Persecució religiosa
    POLITICAL = "political"         # Persecució política
    FAMILY = "family"               # Reunificació familiar
    CLIMATE = "climate"             # Canvi climàtic
    OPPORTUNITY = "opportunity"     # Millor vida


@dataclass
class PopulationPyramid:
    """
    Piràmide de població amb grups d'edat i gènere
    """
    civilization: str
    year: int
    male_distribution: Dict[AgeGroup, int] = field(default_factory=dict)
    female_distribution: Dict[AgeGroup, int] = field(default_factory=dict)

    def get_total_population(self) -> int:
        """Obté població total"""
        total = 0
        for group in AgeGroup:
            total += self.male_distribution.get(group, 0)
            total += self.female_distribution.get(group, 0)
        return total

    def get_working_age_population(self) -> int:
        """Obté població en edat de treballar (15-64)"""
        working_groups = [
            AgeGroup.YOUTH, AgeGroup.YOUNG_ADULT,
            AgeGroup.ADULT, AgeGroup.MIDDLE_AGE, AgeGroup.SENIOR
        ]
        total = 0
        for group in working_groups:
            total += self.male_distribution.get(group, 0)
            total += self.female_distribution.get(group, 0)
        return total

    def get_dependency_ratio(self) -> float:
        """Obté ràtio de dependència (infants+ancians / treballadors)"""
        dependent = 0
        for group in [AgeGroup.INFANT, AgeGroup.CHILD, AgeGroup.ELDERLY]:
            dependent += self.male_distribution.get(group, 0)
            dependent += self.female_distribution.get(group, 0)

        working = self.get_working_age_population()
        if working == 0:
            return 0.0

        return dependent / working

    def to_dict(self) -> Dict:
        """Serialitza piràmide"""
        return {
            'civilization': self.civilization,
            'year': self.year,
            'total_population': self.get_total_population(),
            'working_age': self.get_working_age_population(),
            'dependency_ratio': self.get_dependency_ratio(),
            'male_by_age': {group.value: count for group, count in self.male_distribution.items()},
            'female_by_age': {group.value: count for group, count in self.female_distribution.items()}
        }


@dataclass
class Migration:
    """
    Moviment migratori entre civilitzacions
    """
    source_civilization: str
    destination_civilization: str
    year: int
    migrants_count: int
    reason: MigrationReason
    age_profile: Dict[AgeGroup, float] = field(default_factory=dict)  # Percentatges
    description: str = ""

    def to_dict(self) -> Dict:
        """Serialitza migració"""
        return {
            'source': self.source_civilization,
            'destination': self.destination_civilization,
            'year': self.year,
            'migrants': self.migrants_count,
            'reason': self.reason.value,
            'description': self.description
        }


@dataclass
class DemographicTrends:
    """
    Tendències demogràfiques d'una civilització
    """
    civilization: str
    birth_rate: float  # Per 1000 habitants
    death_rate: float  # Per 1000 habitants
    infant_mortality: float  # Per 1000 naixements
    life_expectancy: float  # Anys
    fertility_rate: float  # Fills per dona
    urbanization_rate: float  # % població urbana

    def get_natural_growth_rate(self) -> float:
        """Taxa de creixement natural (naixements - morts)"""
        return self.birth_rate - self.death_rate


class DemographicsSystem:
    """
    Sistema demogràfic ultra-realista amb IA
    """

    def __init__(self, ai_system: CivilizationAISystem):
        """
        Args:
            ai_system: Sistema de models IA per civilització
        """
        self.ai_system = ai_system
        self.pyramids: Dict[str, PopulationPyramid] = {}
        self.migrations: List[Migration] = []
        self.trends: Dict[str, DemographicTrends] = {}

    def generate_population_pyramid(
        self,
        civilization_name: str,
        year: int,
        total_population: int,
        culture_traits: Dict,
        environment_type: str,
        tech_level: int,
        recent_events: List[str],
        use_ai: bool = True
    ) -> PopulationPyramid:
        """
        Genera piràmide de població amb IA

        Args:
            civilization_name: Nom de la civilització
            year: Any actual
            total_population: Població total
            culture_traits: Trets culturals
            environment_type: Tipus d'entorn
            tech_level: Nivell tecnològic (0-8)
            recent_events: Esdeveniments recents
            use_ai: Si usar IA

        Returns:
            PopulationPyramid generada
        """
        if use_ai:
            pyramid = self._generate_pyramid_with_ai(
                civilization_name,
                year,
                total_population,
                culture_traits,
                environment_type,
                tech_level,
                recent_events
            )

            if pyramid:
                self.pyramids[civilization_name] = pyramid
                return pyramid

        # Fallback procedural
        return self._generate_pyramid_procedural(
            civilization_name,
            year,
            total_population,
            culture_traits,
            tech_level
        )

    def _generate_pyramid_with_ai(
        self,
        civilization_name: str,
        year: int,
        total_population: int,
        culture_traits: Dict,
        environment_type: str,
        tech_level: int,
        recent_events: List[str]
    ) -> Optional[PopulationPyramid]:
        """Genera piràmide amb el model IA de la civilització"""

        # Construeix prompt
        prompt = f"""Genera distribució demogràfica realista per la civilització {civilization_name}.

CONTEXT:
Any: {year}
Població total: {total_population:,} habitants
Entorn: {environment_type}
Nivell tecnològic: {tech_level}/8

Cultura:
Militarisme: {culture_traits.get('militarism', 50):.0f}/100
Innovació: {culture_traits.get('innovation', 50):.0f}/100
Tradició: {culture_traits.get('tradition', 50):.0f}/100
Sanitat bàsica: {'Alta' if tech_level >= 5 else 'Mitja' if tech_level >= 3 else 'Baixa'}

Esdeveniments recents:
{chr(10).join(f"- {event}" for event in recent_events[:5]) if recent_events else "- Cap esdeveniment"}

INSTRUCCIONS:
Genera una distribució de població per grups d'edat (percentatges).
- Nivell tec baix (0-2): Alta mortalitat infantil, esperança vida 35-45 anys, molts infants
- Nivell tec mitjà (3-5): Mortalitat moderada, esperança vida 50-60 anys
- Nivell tec alt (6-8): Baixa mortalitat, esperança vida 65-75 anys, envelliment

Guerres recents → menys homes adults (25-44)
Alta tradició → més infants, més ancians respectats

Respon NOMÉS en format JSON (sense markdown):
{{
"infant_0_4": "5-15 (% de població total)",
"child_5_14": "10-20",
"youth_15_24": "10-18",
"young_adult_25_34": "10-16",
"adult_35_44": "10-15",
"middle_age_45_54": "8-14",
"senior_55_64": "6-12",
"elderly_65_plus": "2-10",
"birth_rate": "15-45 (per 1000)",
"death_rate": "8-35 (per 1000)",
"infant_mortality": "20-150 (per 1000 naixements)",
"life_expectancy": "35-75 (anys)",
"fertility_rate": "2.0-6.0 (fills per dona)",
"urbanization": "10-80 (% urbà)"
}}"""

        result = self.ai_system.generate_with_civ_model(
            civilization_name=civilization_name,
            prompt=prompt
        )

        if not result:
            return None

        try:
            # Parseja percentatges
            age_percentages = {
                AgeGroup.INFANT: float(result.get('infant_0_4', '10').split('-')[0]),
                AgeGroup.CHILD: float(result.get('child_5_14', '15').split('-')[0]),
                AgeGroup.YOUTH: float(result.get('youth_15_24', '14').split('-')[0]),
                AgeGroup.YOUNG_ADULT: float(result.get('young_adult_25_34', '13').split('-')[0]),
                AgeGroup.ADULT: float(result.get('adult_35_44', '12').split('-')[0]),
                AgeGroup.MIDDLE_AGE: float(result.get('middle_age_45_54', '11').split('-')[0]),
                AgeGroup.SENIOR: float(result.get('senior_55_64', '9').split('-')[0]),
                AgeGroup.ELDERLY: float(result.get('elderly_65_plus', '6').split('-')[0])
            }

            # Normalitza percentatges
            total_pct = sum(age_percentages.values())
            if total_pct > 0:
                age_percentages = {k: (v / total_pct) * 100 for k, v in age_percentages.items()}

            # Distribueix població per gènere (aproximadament 50-50, lleugerament més homes neixen)
            pyramid = PopulationPyramid(
                civilization=civilization_name,
                year=year
            )

            for group, percentage in age_percentages.items():
                count = int(total_population * percentage / 100.0)

                # Homes lleugerament més als infants, equilibri després
                male_ratio = 0.51 if group in [AgeGroup.INFANT, AgeGroup.CHILD] else 0.50

                # Guerres recents redueixen homes adults
                if group in [AgeGroup.YOUNG_ADULT, AgeGroup.ADULT]:
                    for event in recent_events[-5:]:
                        if 'guerra' in event.lower() or 'batalla' in event.lower():
                            male_ratio -= 0.05
                            break

                male_ratio = max(0.40, min(0.60, male_ratio))

                pyramid.male_distribution[group] = int(count * male_ratio)
                pyramid.female_distribution[group] = count - pyramid.male_distribution[group]

            # Guarda tendències
            self.trends[civilization_name] = DemographicTrends(
                civilization=civilization_name,
                birth_rate=float(result.get('birth_rate', '25').split('-')[0]),
                death_rate=float(result.get('death_rate', '15').split('-')[0]),
                infant_mortality=float(result.get('infant_mortality', '50').split('-')[0]),
                life_expectancy=float(result.get('life_expectancy', '55').split('-')[0]),
                fertility_rate=float(result.get('fertility_rate', '3.5').split('-')[0]),
                urbanization_rate=float(result.get('urbanization', '30').split('-')[0])
            )

            self.pyramids[civilization_name] = pyramid
            return pyramid

        except Exception as e:
            print(f"⚠️  Error creant PopulationPyramid: {e}")
            return None

    def _generate_pyramid_procedural(
        self,
        civilization_name: str,
        year: int,
        total_population: int,
        culture_traits: Dict,
        tech_level: int
    ) -> PopulationPyramid:
        """Genera piràmide proceduralment"""

        pyramid = PopulationPyramid(
            civilization=civilization_name,
            year=year
        )

        # Distribució segons nivell tecnològic
        if tech_level <= 2:
            # Pre-modern: Piràmide expansiva
            percentages = {
                AgeGroup.INFANT: 0.12,
                AgeGroup.CHILD: 0.18,
                AgeGroup.YOUTH: 0.16,
                AgeGroup.YOUNG_ADULT: 0.14,
                AgeGroup.ADULT: 0.12,
                AgeGroup.MIDDLE_AGE: 0.10,
                AgeGroup.SENIOR: 0.08,
                AgeGroup.ELDERLY: 0.10
            }
        elif tech_level <= 5:
            # Industrial: Piràmide transicional
            percentages = {
                AgeGroup.INFANT: 0.10,
                AgeGroup.CHILD: 0.15,
                AgeGroup.YOUTH: 0.14,
                AgeGroup.YOUNG_ADULT: 0.13,
                AgeGroup.ADULT: 0.13,
                AgeGroup.MIDDLE_AGE: 0.12,
                AgeGroup.SENIOR: 0.10,
                AgeGroup.ELDERLY: 0.13
            }
        else:
            # Post-industrial: Piràmide constrictiva
            percentages = {
                AgeGroup.INFANT: 0.08,
                AgeGroup.CHILD: 0.12,
                AgeGroup.YOUTH: 0.12,
                AgeGroup.YOUNG_ADULT: 0.12,
                AgeGroup.ADULT: 0.14,
                AgeGroup.MIDDLE_AGE: 0.14,
                AgeGroup.SENIOR: 0.13,
                AgeGroup.ELDERLY: 0.15
            }

        # Distribueix població
        for group, percentage in percentages.items():
            count = int(total_population * percentage)
            pyramid.male_distribution[group] = int(count * 0.50)
            pyramid.female_distribution[group] = count - pyramid.male_distribution[group]

        self.pyramids[civilization_name] = pyramid
        return pyramid

    def generate_migration(
        self,
        source_civ: str,
        destination_civ: str,
        year: int,
        source_population: int,
        reason: MigrationReason,
        context: Dict,
        use_ai: bool = True
    ) -> Optional[Migration]:
        """
        Genera migració amb IA

        Args:
            source_civ: Civilització origen
            destination_civ: Civilització destí
            year: Any
            source_population: Població origen
            reason: Raó de migració
            context: Context (guerra, economia, etc.)
            use_ai: Si usar IA

        Returns:
            Migration generada
        """
        if use_ai:
            migration = self._generate_migration_with_ai(
                source_civ,
                destination_civ,
                year,
                source_population,
                reason,
                context
            )

            if migration:
                self.migrations.append(migration)
                return migration

        # Fallback procedural
        return self._generate_migration_procedural(
            source_civ,
            destination_civ,
            year,
            source_population,
            reason
        )

    def _generate_migration_with_ai(
        self,
        source_civ: str,
        destination_civ: str,
        year: int,
        source_population: int,
        reason: MigrationReason,
        context: Dict
    ) -> Optional[Migration]:
        """Genera migració amb IA"""

        prompt = f"""Genera migració realista de {source_civ} a {destination_civ}.

CONTEXT:
Any: {year}
Població origen: {source_population:,}
Raó: {reason.value}

Detalls:
{chr(10).join(f"- {k}: {v}" for k, v in context.items())}

INSTRUCCIONS:
Determina quants migrants es mouen i per què.
- Guerra: 5-20% de població pot fugir
- Fam: 10-30% poden migrar
- Econòmica: 1-5% busquen oportunitats
- Religiosa/política: 0.5-10% perseguits

Profil d'edat varia segons raó:
- Guerra: Famílies senceres, molts infants
- Econòmica: Joves adults (20-35 anys)
- Fam: Supervivents més forts (teens-adults)

Respon en JSON (sense markdown):
{{
"migrants_percentage": "0.5-30 (% de població)",
"description": "Descripció curta de la migració (1-2 frases)",
"age_profile": {{
  "infant_0_4": "0-30 (% dels migrants)",
  "child_5_14": "0-25",
  "youth_15_24": "10-40",
  "young_adult_25_34": "15-50",
  "adult_35_44": "5-30",
  "middle_age_45_54": "0-20",
  "senior_55_64": "0-10",
  "elderly_65_plus": "0-5"
}}
}}"""

        result = self.ai_system.generate_with_civ_model(
            civilization_name=source_civ,
            prompt=prompt
        )

        if not result:
            return None

        try:
            migrants_pct = float(result.get('migrants_percentage', '5').split('-')[0])
            migrants_count = int(source_population * migrants_pct / 100.0)

            # Perfil d'edat
            age_profile = {}
            profile_data = result.get('age_profile', {})

            for group_key, group_enum in [
                ('infant_0_4', AgeGroup.INFANT),
                ('child_5_14', AgeGroup.CHILD),
                ('youth_15_24', AgeGroup.YOUTH),
                ('young_adult_25_34', AgeGroup.YOUNG_ADULT),
                ('adult_35_44', AgeGroup.ADULT),
                ('middle_age_45_54', AgeGroup.MIDDLE_AGE),
                ('senior_55_64', AgeGroup.SENIOR),
                ('elderly_65_plus', AgeGroup.ELDERLY)
            ]:
                pct_str = profile_data.get(group_key, '10')
                pct = float(pct_str.split('-')[0])
                age_profile[group_enum] = pct

            # Normalitza
            total = sum(age_profile.values())
            if total > 0:
                age_profile = {k: v / total for k, v in age_profile.items()}

            migration = Migration(
                source_civilization=source_civ,
                destination_civilization=destination_civ,
                year=year,
                migrants_count=migrants_count,
                reason=reason,
                age_profile=age_profile,
                description=result.get('description', '')
            )

            self.migrations.append(migration)
            return migration

        except Exception as e:
            print(f"⚠️  Error creant Migration: {e}")
            return None

    def _generate_migration_procedural(
        self,
        source_civ: str,
        destination_civ: str,
        year: int,
        source_population: int,
        reason: MigrationReason
    ) -> Migration:
        """Genera migració proceduralment"""

        # Percentatge segons raó
        reason_percentages = {
            MigrationReason.WAR: 0.15,
            MigrationReason.FAMINE: 0.20,
            MigrationReason.ECONOMIC: 0.03,
            MigrationReason.RELIGIOUS: 0.05,
            MigrationReason.POLITICAL: 0.04,
            MigrationReason.FAMILY: 0.01,
            MigrationReason.CLIMATE: 0.10,
            MigrationReason.OPPORTUNITY: 0.02
        }

        migrants_pct = reason_percentages.get(reason, 0.05)
        migrants_count = int(source_population * migrants_pct)

        # Perfil d'edat segons raó
        if reason in [MigrationReason.WAR, MigrationReason.FAMINE]:
            # Famílies senceres
            age_profile = {
                AgeGroup.INFANT: 0.15,
                AgeGroup.CHILD: 0.18,
                AgeGroup.YOUTH: 0.16,
                AgeGroup.YOUNG_ADULT: 0.18,
                AgeGroup.ADULT: 0.15,
                AgeGroup.MIDDLE_AGE: 0.10,
                AgeGroup.SENIOR: 0.06,
                AgeGroup.ELDERLY: 0.02
            }
        else:
            # Joves adults busquen oportunitats
            age_profile = {
                AgeGroup.INFANT: 0.05,
                AgeGroup.CHILD: 0.08,
                AgeGroup.YOUTH: 0.25,
                AgeGroup.YOUNG_ADULT: 0.35,
                AgeGroup.ADULT: 0.18,
                AgeGroup.MIDDLE_AGE: 0.07,
                AgeGroup.SENIOR: 0.02,
                AgeGroup.ELDERLY: 0.00
            }

        migration = Migration(
            source_civilization=source_civ,
            destination_civilization=destination_civ,
            year=year,
            migrants_count=migrants_count,
            reason=reason,
            age_profile=age_profile,
            description=f"Migració de {migrants_count:,} persones per {reason.value}"
        )

        self.migrations.append(migration)
        return migration

    def get_statistics(self) -> Dict:
        """Obté estadístiques demogràfiques"""
        total_migrants = sum(m.migrants_count for m in self.migrations)

        return {
            'total_civilizations_tracked': len(self.pyramids),
            'total_migrations': len(self.migrations),
            'total_migrants': total_migrants,
            'average_life_expectancy': sum(t.life_expectancy for t in self.trends.values()) / len(self.trends) if self.trends else 0,
            'average_fertility_rate': sum(t.fertility_rate for t in self.trends.values()) / len(self.trends) if self.trends else 0
        }
