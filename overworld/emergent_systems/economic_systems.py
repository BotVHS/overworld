"""
Economic Systems - Sistemes econòmics emergents

Genera sistemes econòmics únics basats en recursos, geografia i cultura
"""
from typing import Dict, Optional, List
from dataclasses import dataclass
import random
from ..ai.ollama_client import get_ollama_client


@dataclass
class EconomicSystem:
    """
    Un sistema econòmic únic generat proceduralment

    NO són sistemes econòmics estàndards (capitalisme, socialisme, etc.),
    sinó sistemes emergents únics per cada civilització
    """
    name: str                        # Nom del sistema econòmic
    economic_model: str             # Model base (mercat, planejat, mixt, etc.)
    primary_resources: List[str]    # Recursos principals de l'economia
    trade_focus: str                # Focus comercial (marítim, terrestre, autàrquic)
    currency_type: str              # Tipus de moneda (or, plata, troc, crèdit)
    wealth_distribution: str        # Distribució de la riquesa
    taxation_system: str            # Sistema d'impostos
    guild_structure: str            # Estructura de gremis/corporacions
    market_regulation: str          # Regulació del mercat
    historical_origin: str          # Com va sorgir aquest sistema
    advantages: List[str]           # Avantatges del sistema
    disadvantages: List[str]        # Desavantatges
    prosperity_index: int           # Índex de prosperitat (1-10)
    inequality_index: int           # Índex de desigualtat (1-10)

    def to_dict(self) -> Dict:
        """Serialitza el sistema econòmic"""
        return {
            'name': self.name,
            'economic_model': self.economic_model,
            'primary_resources': self.primary_resources,
            'trade_focus': self.trade_focus,
            'currency_type': self.currency_type,
            'wealth_distribution': self.wealth_distribution,
            'taxation_system': self.taxation_system,
            'guild_structure': self.guild_structure,
            'market_regulation': self.market_regulation,
            'historical_origin': self.historical_origin,
            'advantages': self.advantages,
            'disadvantages': self.disadvantages,
            'prosperity_index': self.prosperity_index,
            'inequality_index': self.inequality_index
        }


class EconomicSystemGenerator:
    """
    Genera sistemes econòmics emergents

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
        is_coastal: bool,
        available_resources: List[str],
        culture_traits: Dict,
        tech_level: int,
        recent_history: List[str],
        neighbors_count: int = 0
    ) -> EconomicSystem:
        """
        Genera un sistema econòmic únic

        Args:
            civilization_name: Nom de la civilització
            population: Població total
            environment_type: Tipus d'entorn
            is_coastal: Si té accés al mar
            available_resources: Recursos naturals disponibles
            culture_traits: Trets culturals (dict)
            tech_level: Nivell tecnològic (0-8)
            recent_history: Esdeveniments recents
            neighbors_count: Nombre de civilitzacions veïnes

        Returns:
            EconomicSystem generat
        """
        # Intenta generar amb IA
        if self.use_ollama and self.ollama and self.ollama.available:
            system = self._generate_with_ai(
                civilization_name,
                population,
                environment_type,
                is_coastal,
                available_resources,
                culture_traits,
                tech_level,
                recent_history,
                neighbors_count
            )

            if system:
                return system

        # Fallback: generació procedural
        return self._generate_procedural(
            civilization_name,
            environment_type,
            is_coastal,
            available_resources,
            culture_traits,
            tech_level,
            neighbors_count
        )

    def _generate_with_ai(
        self,
        civilization_name: str,
        population: int,
        environment_type: str,
        is_coastal: bool,
        available_resources: List[str],
        culture_traits: Dict,
        tech_level: int,
        recent_history: List[str],
        neighbors_count: int
    ) -> Optional[EconomicSystem]:
        """Genera sistema econòmic amb Ollama"""

        resources_str = ', '.join(available_resources[:10]) if available_resources else "Cap recurs destacat"
        coastal_str = "amb accés al mar" if is_coastal else "sense accés al mar"

        # Construeix el prompt
        prompt = f"""Ets un economista i antropòleg creatiu. Genera un sistema econòmic INNOVADOR i ÚNIC (no usis capitalisme, socialisme, comunisme estàndards llevat que siguin absolutament òbvies).

CONTEXT DE LA CIVILITZACIÓ:

Nom: {civilization_name}
Població: {population:,} habitants
Entorn: {environment_type} - {coastal_str}
Recursos disponibles: {resources_str}
Nivell tecnològic: {tech_level}/8
Civilitzacions veïnes: {neighbors_count}

Història recent:
{chr(10).join(f"- {event}" for event in recent_history[:5]) if recent_history else "- Sense esdeveniments registrats"}

Valors culturals:
- Comerç: {culture_traits.get('commerce', 50):.0f}/100
- Navegació: {culture_traits.get('navigation', 50):.0f}/100
- Mineria: {culture_traits.get('mining', 50):.0f}/100
- Agricultura: {culture_traits.get('agriculture', 50):.0f}/100
- Artesania: {culture_traits.get('craftsmanship', 50):.0f}/100
- Autoritarisme: {culture_traits.get('authoritarianism', 50):.0f}/100

INSTRUCCIONS:

Basant-te en aquest context, crea un sistema econòmic que emergeixi NATURALMENT dels recursos, geografia i cultura.

El sistema ha de ser:
1. ÚNIC i CREATIU (evita capitalisme/socialisme estàndards)
2. COHERENT amb recursos i geografia
3. PRÀCTIC (com funciona al dia a dia?)
4. AMB NOM ORIGINAL (inventa un terme nou)

Respon NOMÉS en aquest format JSON (sense markdown, sense explicacions extra):
{{
"nom_sistema": "nom inventat del sistema econòmic",
"model_economic": "descripció breu del model (mercat, planejat, mixt, etc.)",
"recursos_primaris": ["recurs1", "recurs2", "recurs3"],
"focus_comerc": "marítim / terrestre / autàrquic / mixt",
"tipus_moneda": "què usen com a moneda (or, plata, troc, crèdit, etc.)",
"distribucio_riquesa": "com es distribueix la riquesa",
"sistema_impostos": "com funcionen els impostos",
"estructura_gremis": "com s'organitzen els comerciants i artesans",
"regulacio_mercat": "com es regula l'economia",
"origen_historic": "quin esdeveniment va causar aquest sistema",
"avantatges": ["avantatge1", "avantatge2"],
"desavantatges": ["desavantatge1", "desavantatge2"],
"index_prosperitat": "1-10 (1=pobre, 10=molt ric)",
"index_desigualtat": "1-10 (1=igualitari, 10=molt desigual)"
}}"""

        # Genera amb Ollama
        result = self.ollama.generate_json(prompt, temperature=0.9)

        if result:
            try:
                return EconomicSystem(
                    name=result.get('nom_sistema', 'Sistema Econòmic Desconegut'),
                    economic_model=result.get('model_economic', ''),
                    primary_resources=result.get('recursos_primaris', []),
                    trade_focus=result.get('focus_comerc', 'mixt'),
                    currency_type=result.get('tipus_moneda', 'or'),
                    wealth_distribution=result.get('distribucio_riquesa', ''),
                    taxation_system=result.get('sistema_impostos', ''),
                    guild_structure=result.get('estructura_gremis', ''),
                    market_regulation=result.get('regulacio_mercat', ''),
                    historical_origin=result.get('origen_historic', ''),
                    advantages=result.get('avantatges', []),
                    disadvantages=result.get('desavantatges', []),
                    prosperity_index=int(result.get('index_prosperitat', 5)),
                    inequality_index=int(result.get('index_desigualtat', 5))
                )
            except Exception as e:
                print(f"⚠️  Error creant EconomicSystem des de JSON: {e}")

        return None

    def _generate_procedural(
        self,
        civilization_name: str,
        environment_type: str,
        is_coastal: bool,
        available_resources: List[str],
        culture_traits: Dict,
        tech_level: int,
        neighbors_count: int
    ) -> EconomicSystem:
        """Genera sistema econòmic proceduralment (fallback)"""

        # Extreu trets culturals
        commerce = culture_traits.get('commerce', 50)
        navigation = culture_traits.get('navigation', 50)
        mining = culture_traits.get('mining', 50)
        agriculture = culture_traits.get('agriculture', 50)
        authoritarianism = culture_traits.get('authoritarianism', 50)
        craftsmanship = culture_traits.get('craftsmanship', 50)

        # Determina recursos primaris
        if available_resources:
            primary_resources = available_resources[:3]
        else:
            primary_resources = ["agricultura", "pesca", "comerç"]

        # Noms procedurals
        prefixes = ["Mercat", "Gremial", "Corporatiu", "Feudal", "Comunal", "Imperial"]
        suffixes = ["ocràcia", "isme", "at", "ia", "arxia"]

        # === TALASSOCRÀCIA (costa + alta navegació) ===
        if is_coastal and navigation > 70:
            name = f"Talasso{random.choice(suffixes)}"
            economic_model = "Economia marítima basada en comerç naval i monopolis comercials"
            trade_focus = "marítim"
            currency_type = "monedes de plata i lletres de canvi"
            wealth_distribution = "Concentrada en mercaders i armadors navals"
            taxation = "Tarifes portuàries i impostos sobre comerç exterior"
            guild_structure = "Gremis de navegants i companyies comercials marítimes"
            market_regulation = "Regulació estricta de rutes comercials i monopolis"
            origin = "Va sorgir quan els navegants van dominar les rutes comercials"
            advantages = ["Rutes comercials llunyanes", "Monopolis lucratius"]
            disadvantages = ["Dependència del mar", "Pirates i competència naval"]
            prosperity = 8
            inequality = 7

        # === ECONOMIA MINERA (recursos minerals + mineria alta) ===
        elif mining > 70 or any(r in ['Gold', 'Silver', 'Iron', 'Copper', 'Gems'] for r in available_resources):
            name = f"Gremial{random.choice(suffixes)}"
            economic_model = "Economia basada en extracció i exportació de minerals"
            trade_focus = "terrestre"
            currency_type = "monedes d'or i plata"
            wealth_distribution = "Controlada per gremis miners i comerciants de metalls"
            taxation = "Regalia reial sobre minerals extrets"
            guild_structure = "Gremis miners molt poderosos amb monopolis"
            market_regulation = "Regulació estricta de l'extracció i preu dels metalls"
            origin = "Va emergir quan es van descobrir grans jaciments minerals"
            advantages = ["Riquesa mineral abundant", "Exportació lucrativa"]
            disadvantages = ["Esgotament de recursos", "Dependència d'un sol sector"]
            prosperity = 7
            inequality = 8

        # === ECONOMIA COMERCIAL (alt comerç) ===
        elif commerce > 70:
            name = f"Mercat{random.choice(suffixes)}"
            economic_model = "Economia de mercat lliure dominada per mercaders"
            trade_focus = "mixt" if is_coastal else "terrestre"
            currency_type = "monedes d'or amb sistema bancari incipient"
            wealth_distribution = "Molt desigual, concentrada en mercaders rics"
            taxation = "Impostos sobre transaccions comercials"
            guild_structure = "Gremis comercials amb gran poder polític"
            market_regulation = "Regulació mínima, mercat lliure"
            origin = "Va sorgir quan els mercaders van acumular poder econòmic"
            advantages = ["Dinamisme econòmic", "Innovació comercial"]
            disadvantages = ["Alta desigualtat", "Cicles econòmics inestables"]
            prosperity = 7
            inequality = 8

        # === ECONOMIA PLANIFICADA (alt autoritarisme) ===
        elif authoritarianism > 70:
            name = f"Imperial{random.choice(suffixes)}"
            economic_model = "Economia planificada centralment per l'estat"
            trade_focus = "autàrquic"
            currency_type = "moneda estatal amb valor fix"
            wealth_distribution = "Controlada per l'estat i l'elit dirigent"
            taxation = "Tributs obligatoris i treballs forçats"
            guild_structure = "Corporacions estatals obligatòries"
            market_regulation = "Planificació central de producció i preus"
            origin = "Va ser imposat per un govern autoritari centralitzador"
            advantages = ["Ordre econòmic", "Mobilització de recursos"]
            disadvantages = ["Ineficiència", "Manca de llibertats econòmiques"]
            prosperity = 5
            inequality = 9

        # === ECONOMIA AGRÀRIA (alta agricultura) ===
        elif agriculture > 70:
            name = f"Feudal{random.choice(suffixes)}"
            economic_model = "Economia agrària amb sistema de terres i serfs"
            trade_focus = "autàrquic"
            currency_type = "troc i monedes limitades"
            wealth_distribution = "Concentrada en terratinents i senyors"
            taxation = "Rendes agrícoles i delmes"
            guild_structure = "Gremis agrícoles i artesans rurals"
            market_regulation = "Regulació feudal de terres i producció"
            origin = "Va evolucionar del sistema de propietat de terres"
            advantages = ["Autosuficiència alimentària", "Estabilitat rural"]
            disadvantages = ["Baixa mobilitat social", "Estancament tecnològic"]
            prosperity = 5
            inequality = 8

        # === ECONOMIA ARTESANAL (alta artesania) ===
        elif craftsmanship > 70:
            name = f"Corporatiu{random.choice(suffixes)}"
            economic_model = "Economia basada en gremis artesanals especialitzats"
            trade_focus = "terrestre"
            currency_type = "monedes de plata i sistemes de crèdit gremial"
            wealth_distribution = "Distribuïda entre mestres artesans"
            taxation = "Impostos sobre producció artesanal"
            guild_structure = "Gremis artesanals amb gran autonomia"
            market_regulation = "Regulació de qualitat per gremis"
            origin = "Va sorgir quan els artesans es van organitzar en gremis"
            advantages = ["Alta qualitat de productes", "Innovació artesanal"]
            disadvantages = ["Proteccionisme gremial", "Costos elevats"]
            prosperity = 6
            inequality = 6

        # === ECONOMIA EQUILIBRADA (defecte) ===
        else:
            name = f"Comunal{random.choice(suffixes)}"
            economic_model = "Economia mixta amb elements de mercat i cooperació"
            trade_focus = "mixt"
            currency_type = "troc i monedes locals"
            wealth_distribution = "Moderadament distribuïda"
            taxation = "Impostos comunals progressius"
            guild_structure = "Cooperatives de productors"
            market_regulation = "Regulació comunitària equilibrada"
            origin = "Va evolucionar gradualment de pràctiques tradicionals"
            advantages = ["Equilibri social", "Estabilitat moderada"]
            disadvantages = ["Creixement lent", "Manca d'especialització"]
            prosperity = 5
            inequality = 5

        return EconomicSystem(
            name=name,
            economic_model=economic_model,
            primary_resources=primary_resources,
            trade_focus=trade_focus,
            currency_type=currency_type,
            wealth_distribution=wealth_distribution,
            taxation_system=taxation,
            guild_structure=guild_structure,
            market_regulation=market_regulation,
            historical_origin=origin,
            advantages=advantages,
            disadvantages=disadvantages,
            prosperity_index=prosperity,
            inequality_index=inequality
        )
