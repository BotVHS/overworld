"""
Leader AI - Intel·ligència artificial per a líders de civilitzacions

Usa Ollama per prendre decisions estratègiques contextuals
"""
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
import random
from .ollama_client import get_ollama_client


class DecisionType(Enum):
    """Tipus de decisions que pot prendre un líder"""
    WAR_DECLARATION = "guerra"
    PEACE_TREATY = "pau"
    TRADE_AGREEMENT = "comerç"
    POLITICAL_REFORM = "reforma_política"
    RELIGIOUS_REFORM = "reforma_religiosa"
    ECONOMIC_POLICY = "política_econòmica"
    DIPLOMATIC_STANCE = "postura_diplomàtica"
    TECHNOLOGY_FOCUS = "focus_tecnològic"
    EXPANSION = "expansió"
    INTERNAL_POLICY = "política_interna"


@dataclass
class LeaderPersonality:
    """
    Personalitat d'un líder que influeix en les seves decisions
    """
    name: str
    aggressiveness: int       # 1-10 (1=pacifista, 10=belicós)
    pragmatism: int          # 1-10 (1=idealista, 10=pragmàtic)
    religiosity: int         # 1-10 (1=secular, 10=teocrà tic)
    expansionism: int        # 1-10 (1=conservador, 10=expansionista)
    risk_tolerance: int      # 1-10 (1=cautiu, 10=temerari)
    diplomacy_skill: int     # 1-10 (1=pèssim diplomàtic, 10=mestre diplomàtic)

    def to_dict(self) -> Dict:
        """Serialitza la personalitat"""
        return {
            'name': self.name,
            'aggressiveness': self.aggressiveness,
            'pragmatism': self.pragmatism,
            'religiosity': self.religiosity,
            'expansionism': self.expansionism,
            'risk_tolerance': self.risk_tolerance,
            'diplomacy_skill': self.diplomacy_skill
        }


@dataclass
class DecisionContext:
    """
    Context complet per a una decisió del líder
    """
    civilization_name: str
    leader_personality: LeaderPersonality
    population: int
    tech_level: int

    # Sistemes emergents
    political_system: Optional[Dict] = None
    religious_system: Optional[Dict] = None
    economic_system: Optional[Dict] = None

    # Cultura
    culture_traits: Optional[Dict] = None

    # Situació actual
    current_resources: Optional[List[str]] = None
    neighbors: Optional[List[str]] = None
    recent_events: Optional[List[str]] = None
    military_strength: int = 5  # 1-10
    economic_strength: int = 5  # 1-10

    # Situació específica de la decisió
    decision_type: Optional[DecisionType] = None
    decision_prompt: Optional[str] = None  # Situació específica que requereix decisió


@dataclass
class LeaderDecision:
    """
    Decisió presa per un líder
    """
    decision_type: DecisionType
    action: str                    # Acció concreta a prendre
    reasoning: str                 # Raonament del líder
    expected_outcome: str          # Resultat esperat
    risk_level: int               # Nivell de risc (1-10)
    confidence: int               # Confiança en la decisió (1-10)


class LeaderAI:
    """
    IA per a líders de civilitzacions

    Usa Ollama per prendre decisions estratègiques contextuals basades en:
    - Personalitat del líder
    - Cultura i valors de la civilització
    - Sistemes polítics, religiosos i econòmics
    - Situació actual i història recent
    """

    def __init__(self, use_ollama: bool = True):
        """
        Args:
            use_ollama: Si usar Ollama o fallback procedural
        """
        self.use_ollama = use_ollama
        self.ollama = get_ollama_client() if use_ollama else None

    def make_decision(self, context: DecisionContext) -> LeaderDecision:
        """
        Pren una decisió basada en el context

        Args:
            context: Context complet de la decisió

        Returns:
            LeaderDecision amb l'acció a prendre
        """
        # Intenta amb IA
        if self.use_ollama and self.ollama and self.ollama.available:
            decision = self._make_decision_with_ai(context)
            if decision:
                return decision

        # Fallback procedural
        return self._make_decision_procedural(context)

    def _make_decision_with_ai(self, context: DecisionContext) -> Optional[LeaderDecision]:
        """Pren decisió amb Ollama"""

        # Construeix el prompt amb tot el context
        personality = context.leader_personality

        prompt = f"""Ets {personality.name}, líder de la civilització {context.civilization_name}.

PERSONALITAT:
- Agressivitat: {personality.aggressiveness}/10 {'(Belicós)' if personality.aggressiveness > 7 else '(Pacifista)' if personality.aggressiveness < 4 else '(Moderat)'}
- Pragmatisme: {personality.pragmatism}/10 {'(Pragmàtic)' if personality.pragmatism > 7 else '(Idealista)' if personality.pragmatism < 4 else '(Equilibrat)'}
- Religiositat: {personality.religiosity}/10 {'(Teocrà tic)' if personality.religiosity > 7 else '(Secular)' if personality.religiosity < 4 else '(Moderat)'}
- Expansionisme: {personality.expansionism}/10 {'(Expansionista)' if personality.expansionism > 7 else '(Conservador)' if personality.expansionism < 4 else '(Prudent)'}
- Tolerància al risc: {personality.risk_tolerance}/10 {'(Temerari)' if personality.risk_tolerance > 7 else '(Cautiu)' if personality.risk_tolerance < 4 else '(Calculador)'}

CIVILITZACIÓ:
Població: {context.population:,} habitants
Nivell tecnològic: {context.tech_level}/8

Sistema Polític: {context.political_system.get('name') if context.political_system else 'Desconegut'}
Sistema Religiós: {context.religious_system.get('name') if context.religious_system else 'Desconegut'}
Sistema Econòmic: {context.economic_system.get('name') if context.economic_system else 'Desconegut'}

Força Militar: {context.military_strength}/10
Força Econòmica: {context.economic_strength}/10

Veïns: {', '.join(context.neighbors) if context.neighbors else 'Cap'}
Recursos: {', '.join(context.current_resources[:5]) if context.current_resources else 'Cap'}

Història Recent:
{chr(10).join(f"- {event}" for event in context.recent_events[:5]) if context.recent_events else "- Sense esdeveniments recents"}

SITUACIÓ:
{context.decision_prompt or "Decideix la teva estratègia general"}

INSTRUCCIONS:
Com a líder, has de prendre una decisió. Tingues en compte:
1. La teva PERSONALITAT (ets agressiu? pragmàtic? religiós?)
2. Els teus VALORS culturals i sistemes polítics/religiosos/econòmics
3. La teva SITUACIÓ actual (forces militars, economia, veïns)
4. La teva HISTÒRIA recent

Respon NOMÉS en aquest format JSON (sense markdown):
{{
"accio": "descripció concreta de l'acció a prendre",
"raonament": "per què prens aquesta decisió (1-2 frases)",
"resultat_esperat": "què esperes aconseguir",
"nivell_risc": "1-10 (1=sense risc, 10=molt arriscat)",
"confianca": "1-10 (1=dubte, 10=total certesa)"
}}"""

        # Genera amb Ollama
        result = self.ollama.generate_json(prompt, temperature=0.8)

        if result:
            try:
                return LeaderDecision(
                    decision_type=context.decision_type or DecisionType.INTERNAL_POLICY,
                    action=result.get('accio', 'Mantenir l\'status quo'),
                    reasoning=result.get('raonament', ''),
                    expected_outcome=result.get('resultat_esperat', ''),
                    risk_level=int(result.get('nivell_risc', 5)),
                    confidence=int(result.get('confianca', 5))
                )
            except Exception as e:
                print(f"⚠️  Error creant LeaderDecision des de JSON: {e}")

        return None

    def _make_decision_procedural(self, context: DecisionContext) -> LeaderDecision:
        """Pren decisió proceduralment (fallback)"""

        personality = context.leader_personality
        decision_type = context.decision_type or DecisionType.INTERNAL_POLICY

        # Decisions basades en personalitat
        if decision_type == DecisionType.WAR_DECLARATION:
            if personality.aggressiveness > 7 and context.military_strength > context.economic_strength:
                action = f"Declarar guerra al veí més dèbil per expandir el territori"
                reasoning = "La força militar és superior i la nostra naturalesa agressiva ho demana"
                risk = 8
                confidence = 7
            elif personality.aggressiveness < 4:
                action = "Rebutjar la guerra i buscar solucions diplomàtiques"
                reasoning = "La pau és sempre preferible al conflicte"
                risk = 3
                confidence = 8
            else:
                action = "Preparar defensives però no atacar primer"
                reasoning = "Cal ser prudent i defensar els nostres interessos"
                risk = 5
                confidence = 6

        elif decision_type == DecisionType.TRADE_AGREEMENT:
            if context.economic_strength < 5:
                action = "Acceptar acords comercials favorables per millorar l'economia"
                reasoning = "Necessitem fortalecer la nostra economia"
                risk = 4
                confidence = 7
            else:
                action = "Negociar acords que maximitzin els nostres beneficis"
                reasoning = "Estem en posició de força per exigir millors termes"
                risk = 5
                confidence = 8

        elif decision_type == DecisionType.POLITICAL_REFORM:
            if personality.pragmatism > 7:
                action = "Implementar reformes graduals que millorin l'eficiència"
                reasoning = "Cal adaptar-se als temps moderns sense causar caos"
                risk = 5
                confidence = 7
            elif personality.religiosity > 7 and context.religious_system:
                action = f"Reforçar el {context.religious_system.get('name', 'sistema religiós')} en la política"
                reasoning = "La fe ha de guiar les nostres decisions polítiques"
                risk = 6
                confidence = 8
            else:
                action = "Mantenir l'estabilitat política actual"
                reasoning = "Els canvis bruscos poden ser perillosos"
                risk = 3
                confidence = 6

        elif decision_type == DecisionType.EXPANSION:
            if personality.expansionism > 7 and context.population > 5000:
                action = "Expandir agressivament cap a territoris veïns"
                reasoning = "El nostre poble necessita més terres i recursos"
                risk = 8
                confidence = 7
            elif personality.risk_tolerance < 4:
                action = "Expansió gradual només en territoris deshabitats"
                reasoning = "Cal minimitzar riscos i consolidar el que tenim"
                risk = 3
                confidence = 8
            else:
                action = "Colonitzar zones estratègiques de forma planificada"
                reasoning = "Equilibri entre creixement i seguretat"
                risk = 5
                confidence = 7

        else:  # INTERNAL_POLICY
            if context.economic_strength < 5:
                action = "Focus en desenvolupament econòmic i infraestructures"
                reasoning = "Cal enfortir l'economia abans de qualsevol altra cosa"
                risk = 3
                confidence = 8
            elif context.military_strength < 5 and len(context.neighbors or []) > 2:
                action = "Reforçar les forces militars per defensar-nos"
                reasoning = "Estem envoltats de veïns i cal estar preparats"
                risk = 4
                confidence = 7
            else:
                action = "Invertir en ciència i cultura per prosperar"
                reasoning = "El progrés cultural i científic assegura el futur"
                risk = 4
                confidence = 7

        return LeaderDecision(
            decision_type=decision_type,
            action=action,
            reasoning=reasoning,
            expected_outcome=f"Millorar la posició estratègica de {context.civilization_name}",
            risk_level=risk,
            confidence=confidence
        )


def generate_leader_personality(
    civilization_name: str,
    culture_traits: Dict
) -> LeaderPersonality:
    """
    Genera una personalitat de líder basada en la cultura

    Args:
        civilization_name: Nom de la civilització
        culture_traits: Trets culturals

    Returns:
        LeaderPersonality generada
    """
    # Noms procedurals
    prefixes = ["Rex", "Imperator", "Kan", "Sultan", "Autarch", "Tyran", "Princep", "Duc"]
    suffixes = ["us", "or", "on", "ix", "el", "ar"]

    name = f"{random.choice(prefixes)}{random.choice(suffixes)}"

    # Personalitat basada en cultura amb variació
    militarism = culture_traits.get('militarism', 50)
    authoritarianism = culture_traits.get('authoritarianism', 50)
    religion = culture_traits.get('religion', 50)
    expansionism_val = culture_traits.get('expansionism', 50)

    # Converteix a 1-10 amb variació aleatòria
    def to_scale(value: float) -> int:
        base = int(value / 10)  # 0-100 → 0-10
        variation = random.randint(-2, 2)
        return max(1, min(10, base + variation))

    return LeaderPersonality(
        name=name,
        aggressiveness=to_scale(militarism),
        pragmatism=to_scale(100 - authoritarianism),  # Menys autoritari = més pragmàtic
        religiosity=to_scale(religion),
        expansionism=to_scale(expansionism_val),
        risk_tolerance=random.randint(3, 8),  # Més aleatori
        diplomacy_skill=random.randint(3, 8)   # Més aleatori
    )
