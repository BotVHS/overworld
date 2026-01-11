"""
Political Systems - Sistemes polítics emergents

Genera sistemes polítics únics basats en la història i cultura
"""
from typing import Dict, Optional, List
from dataclasses import dataclass
import random
from ..ai.ollama_client import get_ollama_client


@dataclass
class PoliticalSystem:
    """
    Un sistema polític únic generat proceduralment

    NO són sistemes predefinits com democràcia o monarquia,
    sinó sistemes emergents únics per cada civilització
    """
    name: str                    # Nom del sistema (inventat)
    description: str             # Descripció curta
    how_it_works: str           # Com funciona al dia a dia
    historical_origin: str       # Com va sorgir aquest sistema
    advantages: List[str]        # Avantatges del sistema
    disadvantages: List[str]     # Desavantatges
    stability: int              # 1-10 (1=inestable, 10=molt estable)
    popular_satisfaction: int    # 1-10 (1=odiat, 10=adorat)

    def to_dict(self) -> Dict:
        """Serialitza el sistema polític"""
        return {
            'name': self.name,
            'description': self.description,
            'how_it_works': self.how_it_works,
            'historical_origin': self.historical_origin,
            'advantages': self.advantages,
            'disadvantages': self.disadvantages,
            'stability': self.stability,
            'popular_satisfaction': self.popular_satisfaction
        }


class PoliticalSystemGenerator:
    """
    Genera sistemes polítics emergents

    Usa IA (Ollama) per crear sistemes únics basats en context
    """

    def __init__(self, use_ollama: bool = True):
        """
        Args:
            use_ollama: Si usar Ollama o fallback procedural
        """
        self.use_ollama = use_ollama
        self.ollama = get_ollama_client() if use_ollama else None

    def generate_system(
        self,
        civilization_name: str,
        population: int,
        environment_type: str,
        hostility: float,
        fertility: float,
        culture_traits: Dict,
        recent_history: List[str],
        traumas: Optional[List[str]] = None,
        glories: Optional[List[str]] = None
    ) -> PoliticalSystem:
        """
        Genera un sistema polític únic

        Args:
            civilization_name: Nom de la civilització
            population: Població total
            environment_type: Tipus d'entorn (hostil, fèrtil, marítim, etc.)
            hostility: Índex d'hostilitat (0-10)
            fertility: Índex de fertilitat (0-10)
            culture_traits: Trets culturals (dict)
            recent_history: Esdeveniments recents
            traumas: Traumes col·lectius
            glories: Moments de glòria

        Returns:
            PoliticalSystem generat
        """
        # Intenta generar amb IA
        if self.use_ollama and self.ollama and self.ollama.available:
            system = self._generate_with_ai(
                civilization_name,
                population,
                environment_type,
                hostility,
                fertility,
                culture_traits,
                recent_history,
                traumas or [],
                glories or []
            )

            if system:
                return system

        # Fallback: generació procedural
        return self._generate_procedural(
            civilization_name,
            environment_type,
            hostility,
            culture_traits
        )

    def _generate_with_ai(
        self,
        civilization_name: str,
        population: int,
        environment_type: str,
        hostility: float,
        fertility: float,
        culture_traits: Dict,
        recent_history: List[str],
        traumas: List[str],
        glories: List[str]
    ) -> Optional[PoliticalSystem]:
        """Genera sistema polític amb Ollama"""

        # Construeix el prompt segons el README
        prompt = f"""Ets un antropòleg i politòleg creatiu. Genera un sistema polític INNOVADOR i ÚNIC (no usis sistemes històrics humans estàndards com democràcia, monarquia, etc. llevat que siguin absolutament òbvies).

CONTEXT DE LA CIVILITZACIÓ:

Nom: {civilization_name}
Població: {population:,} habitants
Entorn: {environment_type} - Hostilitat: {hostility:.1f}/10 - Fertilitat: {fertility:.1f}/10

Història recent (últims 200 anys):
{chr(10).join(f"- {event}" for event in recent_history[:5]) if recent_history else "- Sense esdeveniments registrats"}

Trauma col·lectiu més gran: {traumas[0] if traumas else "Cap trauma registrat"}
Moment de glòria més gran: {glories[0] if glories else "Cap glòria registrada"}

Valors culturals dominants: {', '.join(culture_traits.get('core_values', ['equilibri']))}
Militarisme: {culture_traits.get('militarism', 50):.0f}/100
Comerç: {culture_traits.get('commerce', 50):.0f}/100
Autoritarisme: {culture_traits.get('authoritarianism', 50):.0f}/100

INSTRUCCIONS:

Basant-te en aquest context, proposa un sistema polític que emergeixi NATURALMENT de la història i entorn d'aquesta civilització.

El sistema ha de ser:
1. ÚNIC i CREATIU (evita democràcia, monarquia, etc. estàndards)
2. COHERENT amb la seva història
3. PRÀCTIC (com funciona al dia a dia?)
4. AMB NOM ORIGINAL (inventa un terme nou)

Respon NOMÉS en aquest format JSON (sense markdown, sense explicacions extra):
{{
"nom_sistema": "nom inventat del sistema",
"descripció_curta": "1-2 frases explicant l'essència",
"funcionament": "com es prenen decisions, qui governa, com s'escull",
"origen_històric": "quin esdeveniment/trauma va causar aquest sistema",
"avantatges": ["avantatge1", "avantatge2"],
"desavantatges": ["desavantatge1", "desavantatge2"],
"estabilitat": "1-10 (1=molt inestable, 10=molt estable)",
"satisfacció_popular": "1-10 (1=odiada, 10=adorada)"
}}"""

        # Genera amb Ollama
        result = self.ollama.generate_json(prompt, temperature=0.9)

        if result:
            try:
                return PoliticalSystem(
                    name=result.get('nom_sistema', 'Sistema Desconegut'),
                    description=result.get('descripció_curta', ''),
                    how_it_works=result.get('funcionament', ''),
                    historical_origin=result.get('origen_històric', ''),
                    advantages=result.get('avantatges', []),
                    disadvantages=result.get('desavantatges', []),
                    stability=int(result.get('estabilitat', 5)),
                    popular_satisfaction=int(result.get('satisfacció_popular', 5))
                )
            except Exception as e:
                print(f"⚠️  Error creant PoliticalSystem des de JSON: {e}")

        return None

    def _generate_procedural(
        self,
        civilization_name: str,
        environment_type: str,
        hostility: float,
        culture_traits: Dict
    ) -> PoliticalSystem:
        """Genera sistema polític proceduralment (fallback)"""

        # Genera sistema basat en trets culturals
        militarism = culture_traits.get('militarism', 50)
        authoritarianism = culture_traits.get('authoritarianism', 50)
        commerce = culture_traits.get('commerce', 50)

        # Noms procedurals
        prefixes = ["Consul", "Tribun", "Concili", "Assemblea", "Consell",
                   "Sindicat", "Gremial", "Corporació", "Federació"]
        suffixes = ["ocràcia", "arquat", "isme", "at", "ia"]

        name = f"{random.choice(prefixes)}{random.choice(suffixes)}"

        # Genera sistema segons cultura
        if militarism > 70:
            description = "Un sistema basat en la força militar i el mèrit de guerra"
            how_it_works = "Els líders són escollits per les seves victòries militars"
            origin = "Va sorgir després de constants guerres i invasions"
            advantages = ["Fort davant amenaces externes", "Disciplina social"]
            disadvantages = ["Repressió interna", "Escalada de conflictes"]
            stability = 7
            satisfaction = 4

        elif commerce > 70:
            description = "Un sistema dominat per mercaders i gremis comercials"
            how_it_works = "El poder polític està lligat a la riquesa comercial"
            origin = "Va emergir quan els mercaders van guanyar influència econòmica"
            advantages = ["Prosperitat econòmica", "Xarxes comercials"]
            disadvantages = ["Corrupció", "Desigualtat econòmica"]
            stability = 6
            satisfaction = 6

        elif authoritarianism > 70:
            description = "Un sistema centralitzat amb poder concentrat"
            how_it_works = "Un petit grup pren totes les decisions importants"
            origin = "Va néixer de la necessitat d'ordre en temps caòtics"
            advantages = ["Decisions ràpides", "Ordre social"]
            disadvantages = ["Manca de llibertat", "Risc de tirania"]
            stability = 8
            satisfaction = 3

        else:
            description = "Un sistema equilibrat amb participació distribuïda"
            how_it_works = "Diversos grups socials comparteixen el poder"
            origin = "Va evolucionar gradualment sense crisis majors"
            advantages = ["Estabilitat moderada", "Acceptació general"]
            disadvantages = ["Decisions lentes", "Compromisos constants"]
            stability = 6
            satisfaction = 6

        return PoliticalSystem(
            name=name,
            description=description,
            how_it_works=how_it_works,
            historical_origin=origin,
            advantages=advantages,
            disadvantages=disadvantages,
            stability=stability,
            popular_satisfaction=satisfaction
        )
