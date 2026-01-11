"""
Religious Systems - Sistemes religiosos emergents

Genera religions úniques basades en la història, cultura i entorn
"""
from typing import Dict, Optional, List
from dataclasses import dataclass
import random
from ..ai.ollama_client import get_ollama_client


@dataclass
class ReligiousSystem:
    """
    Un sistema religiós únic generat proceduralment

    NO són religions històriques conegudes (cristianisme, islam, etc.),
    sinó sistemes de creences emergents únics per cada civilització
    """
    name: str                      # Nom de la religió
    deity_type: str               # Tipus de divinitat (monoteisme, panteó, animisme, etc.)
    core_doctrine: str            # Doctrina central
    creation_myth: str            # Mite de creació del món
    afterlife_belief: str         # Què passa després de la mort
    sacred_practices: List[str]   # Rituals i pràctiques sagrades
    taboos: List[str]             # Prohibicions i tabús
    clergy_structure: str         # Estructura del clergat
    historical_origin: str        # Com va sorgir aquesta religió
    influence_on_society: int     # Influència social (1-10)
    dogmatism: int               # Dogmatisme vs flexibilitat (1-10, 10=molt dogmàtic)

    def to_dict(self) -> Dict:
        """Serialitza el sistema religiós"""
        return {
            'name': self.name,
            'deity_type': self.deity_type,
            'core_doctrine': self.core_doctrine,
            'creation_myth': self.creation_myth,
            'afterlife_belief': self.afterlife_belief,
            'sacred_practices': self.sacred_practices,
            'taboos': self.taboos,
            'clergy_structure': self.clergy_structure,
            'historical_origin': self.historical_origin,
            'influence_on_society': self.influence_on_society,
            'dogmatism': self.dogmatism
        }


class ReligiousSystemGenerator:
    """
    Genera sistemes religiosos emergents

    Usa IA (Ollama) per crear religions úniques basades en context
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
        glories: Optional[List[str]] = None,
        natural_disasters: Optional[List[str]] = None
    ) -> ReligiousSystem:
        """
        Genera un sistema religiós únic

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
            natural_disasters: Desastres naturals experimentats

        Returns:
            ReligiousSystem generat
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
                glories or [],
                natural_disasters or []
            )

            if system:
                return system

        # Fallback: generació procedural
        return self._generate_procedural(
            civilization_name,
            environment_type,
            hostility,
            fertility,
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
        glories: List[str],
        natural_disasters: List[str]
    ) -> Optional[ReligiousSystem]:
        """Genera sistema religiós amb Ollama"""

        # Construeix el prompt segons el README
        prompt = f"""Ets un antropòleg i teòleg creatiu. Genera un sistema religiós INNOVADOR i ÚNIC (no usis religions històriques humanes com cristianisme, islam, etc.).

CONTEXT DE LA CIVILITZACIÓ:

Nom: {civilization_name}
Població: {population:,} habitants
Entorn: {environment_type} - Hostilitat: {hostility:.1f}/10 - Fertilitat: {fertility:.1f}/10

Història recent (últims 200 anys):
{chr(10).join(f"- {event}" for event in recent_history[:5]) if recent_history else "- Sense esdeveniments registrats"}

Trauma col·lectiu més gran: {traumas[0] if traumas else "Cap trauma registrat"}
Moment de glòria més gran: {glories[0] if glories else "Cap glòria registrada"}
Desastres naturals: {', '.join(natural_disasters[:3]) if natural_disasters else "Cap desastre registrat"}

Valors culturals dominants: {', '.join(culture_traits.get('core_values', ['equilibri']))}
Religiositat cultural: {culture_traits.get('religion', 50):.0f}/100
Militarisme: {culture_traits.get('militarism', 50):.0f}/100
Ciència: {culture_traits.get('science', 50):.0f}/100

INSTRUCCIONS:

Basant-te en aquest context, crea una religió que emergeixi NATURALMENT de la història, entorn i experiències d'aquesta civilització.

La religió ha de:
1. SER ÚNICA i ORIGINAL (evita cristianisme, islam, budisme, etc.)
2. REFLECTIR l'entorn (desert→culte a l'aigua, muntanya→esperits de pedra, etc.)
3. RESPONDRE als traumes (guerra→déu protector, fam→divinitat de l'abundància)
4. TENIR COHERÈNCIA INTERNA (mites, rituals i doctrina han d'encaixar)
5. NOM INVENTAT (crea un terme nou per la religió)

Respon NOMÉS en aquest format JSON (sense markdown, sense explicacions extra):
{{
"nom_religio": "nom inventat de la religió",
"tipus_divinitat": "monoteisme / panteó / animisme / dualisme / altres",
"doctrina_central": "1-2 frases sobre la creença fonamental",
"mite_creacio": "com explica aquesta religió l'origen del món",
"creenca_mes_enlla": "què creuen que passa després de la mort",
"practiques_sagrades": ["ritual1", "ritual2", "ritual3"],
"tabus": ["prohibició1", "prohibició2"],
"estructura_clerge": "com s'organitza el clergat (sacerdots, xamans, etc.)",
"origen_historic": "quin esdeveniment va causar l'aparició d'aquesta religió",
"influencia_social": "1-10 (1=marginal, 10=controla la societat)",
"dogmatisme": "1-10 (1=flexible, 10=molt dogmàtic)"
}}"""

        # Genera amb Ollama
        result = self.ollama.generate_json(prompt, temperature=0.9)

        if result:
            try:
                return ReligiousSystem(
                    name=result.get('nom_religio', 'Religió Desconeguda'),
                    deity_type=result.get('tipus_divinitat', 'panteó'),
                    core_doctrine=result.get('doctrina_central', ''),
                    creation_myth=result.get('mite_creacio', ''),
                    afterlife_belief=result.get('creenca_mes_enlla', ''),
                    sacred_practices=result.get('practiques_sagrades', []),
                    taboos=result.get('tabus', []),
                    clergy_structure=result.get('estructura_clerge', ''),
                    historical_origin=result.get('origen_historic', ''),
                    influence_on_society=int(result.get('influencia_social', 5)),
                    dogmatism=int(result.get('dogmatisme', 5))
                )
            except Exception as e:
                print(f"⚠️  Error creant ReligiousSystem des de JSON: {e}")

        return None

    def _generate_procedural(
        self,
        civilization_name: str,
        environment_type: str,
        hostility: float,
        fertility: float,
        culture_traits: Dict
    ) -> ReligiousSystem:
        """Genera sistema religiós proceduralment (fallback)"""

        # Genera sistema basat en entorn i cultura
        religion_val = culture_traits.get('religion', 50)
        science_val = culture_traits.get('science', 50)
        militarism = culture_traits.get('militarism', 50)

        # Noms procedurals
        prefixes = ["Credo", "Culte", "Ordre", "Fe", "Doctrina", "Camí", "Saviesa"]
        deity_names = ["l'Etern", "els Ancestres", "la Naturalesa", "el Cicle",
                      "la Llum", "l'Equilibri", "les Estrelles", "la Muntanya"]

        name = f"{random.choice(prefixes)} de {random.choice(deity_names)}"

        # Tipus de divinitat segons entorn
        if "desert" in environment_type.lower() or hostility > 7:
            deity_type = "monoteisme"
            core_doctrine = "Un únic déu tot-poderós que prova la fe dels fidels"
            creation_myth = "El déu va crear el món de la pols i el foc per forjar ànimes resistents"
            clergy_structure = "Sacerdots ascètics que viuen al desert"
            sacred_practices = ["Dejuni", "Pelegrinatge al desert", "Oració a l'alba"]
            taboos = ["Malbaratament d'aigua", "Abandonar els febles"]

        elif "oceà" in environment_type.lower() or "costa" in environment_type.lower():
            deity_type = "panteó marítim"
            core_doctrine = "Els déus del mar controlen el destí dels mortals"
            creation_myth = "El món va néixer de les ones primordials quan els déus van separar cel i aigua"
            clergy_structure = "Sacerdots navegants que llegeixen els auguris de les marees"
            sacred_practices = ["Ofrenes al mar", "Rituals de navegació", "Cants marineros"]
            taboos = ["Voltar l'esquena al mar", "Matar dofins"]

        elif "muntanya" in environment_type.lower():
            deity_type = "animisme de muntanya"
            core_doctrine = "Cada muntanya té esperit propi que cal respectar"
            creation_myth = "Els gegants de pedra van aixecar les muntanyes amb les seves mans"
            clergy_structure = "Xamans de muntanya que viuen en cims sagrats"
            sacred_practices = ["Escalada ritual", "Ofrenes de pedres", "Meditació a les altures"]
            taboos = ["Trencar pedres sagrades", "Cridar a la muntanya"]

        elif fertility > 7:
            deity_type = "culte de la fertilitat"
            core_doctrine = "La vida és sagrada i cal celebrar-la amb abundància"
            creation_myth = "La mare terra va donar a llum tots els éssers vius"
            clergy_structure = "Sacerdotesses que celebren els cicles de la collita"
            sacred_practices = ["Festivals de collita", "Danses de fertilitat", "Ofrenes de fruita"]
            taboos = ["Malmetre cultius", "Negar aliment als necessitats"]

        elif science_val > 70:
            deity_type = "filosofia còsmica"
            core_doctrine = "L'univers és un sistema d'ordre i raó que cal comprendre"
            creation_myth = "El cosmos es va originar d'un principi matemàtic primordial"
            clergy_structure = "Filòsofs-sacerdots que estudien els fenòmens naturals"
            sacred_practices = ["Observació astronòmica", "Debat filosòfic", "Meditació racional"]
            taboos = ["Superstició", "Rebutjar el coneixement"]

        elif militarism > 70:
            deity_type = "culte del guerrer"
            core_doctrine = "Només els valents mereixen l'honor etern"
            creation_myth = "El món va néixer d'una batalla còsmica entre ordre i caos"
            clergy_structure = "Sacerdots-guerrers que lideren en batalla"
            sacred_practices = ["Benedicció d'armes", "Ritus de combat", "Sacrifici de valor"]
            taboos = ["Covardia", "Deshonor en combat"]

        else:
            deity_type = "dualisme"
            core_doctrine = "El món és un equilibri constant entre forces oposades"
            creation_myth = "Dos principis primordials (llum i foscor) van crear el món en harmonia"
            clergy_structure = "Consell de savis que mantenen l'equilibri"
            sacred_practices = ["Rituals d'equinoci", "Meditació dual", "Ofrenes equilibrades"]
            taboos = ["Extremisme", "Trencar pactes"]

        # Creença en el més enllà
        if religion_val > 70:
            afterlife = "Els morts van a un paradís etern si han viscut segons la doctrina"
        elif science_val > 70:
            afterlife = "L'ànima es dissol i retorna a l'energia còsmica"
        else:
            afterlife = "Els esperits dels morts romanen vigilant els vius"

        # Origen històric genèric
        if hostility > 7:
            origin = "Va sorgir després d'una crisi existencial causada per l'entorn hostil"
        elif fertility > 7:
            origin = "Va evolucionar de rituals agrícoles de celebració de la collita"
        else:
            origin = "Va emergir gradualment dels mites i llegendes dels ancestres"

        # Influència i dogmatisme
        influence = int(religion_val / 10)  # 0-10
        dogmatism = int(10 - science_val / 10)  # Més ciència = menys dogmatisme

        return ReligiousSystem(
            name=name,
            deity_type=deity_type,
            core_doctrine=core_doctrine,
            creation_myth=creation_myth,
            afterlife_belief=afterlife,
            sacred_practices=sacred_practices,
            taboos=taboos,
            clergy_structure=clergy_structure,
            historical_origin=origin,
            influence_on_society=max(1, min(10, influence)),
            dogmatism=max(1, min(10, dogmatism))
        )
