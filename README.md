# overworld
Crea una simulació procedural completa d'un món en Python amb interfície gràfica, alt nivell de detall i sistemes emergents innovadors.

=== ARQUITECTURA DEL PROJECTE ===
Estructura modular amb els següents components:
- Core: Motor de simulació, gestió de temps, sistema de esdeveniments
- World: Generació procedural, biomes, clima, recursos, geologia
- Biology: Genètica, espècies animals/vegetals, evolució, ecosistemes, microorganismes
- Civilization: IA per raça intel·ligent, ciutats, economies, política
- Graphics: Interfície gràfica amb pygame o pyglet
- Persistence: Sistema de save/load amb pickle o JSON
- AI: Integració amb Ollama (model Llama 3.2 3B o Llama 3.1 8B) per decisions de civilitzacions
- EmergentSystems: Sistemes polítics, religiosos, econòmics i culturals emergents

=== GENERACIÓ DEL MÓN ===
- Mapa gran: mínim 500x500 tiles (ajustable)
- Generació procedural amb noise (Perlin/Simplex) per:
  * Altitud (muntanyes, valls, planes)
  * Humitat (deserts, boscos, aiguamolls)
  * Temperatura (zones glacials, temperades, tropicals)
- Biomes resultants: mínim 15 tipus diferents
- Sistema de recursos naturals per tile: minerals (or, plata, ferro, coure, urani), fusta, aigua, fertilitat, petroli, carbó, gas
- Rius generats seguint gradients d'altitud
- Índex d'hostilitat per zona (calculat segons clima extrem, depredadors, desastres)
- Índex de fertilitat per zona (qualitat sòl, aigua, clima moderat)

**TECTÒNICA DE PLAQUES:**
- 5-12 plaques continentals que es mouen lentament (1-10cm/any simulat)
- Zones de subducció (creació de muntanyes i volcans)
- Zones de separació (rift valleys, nous oceans)
- Terratrèmols més freqüents en límits de plaques
- Deriva continental visible a llarg termini (milers d'anys)

**EROSIÓ I GEOLOGIA DINÀMICA:**
- Muntanyes que s'erosionen (velocitat segons precipitació)
- Rius que canvien de curs amb inundacions
- Deltes que creixen
- Canyons formats per erosió fluvial
- Coves i sistemes subterranis
- Aqüífers subterranis (aigua potable finita)

=== SISTEMA CLIMÀTIC AVANÇAT ===
- 4-6 estacions personalitzades amb:
  * Duració variable (no cal que siguin iguals)
  * Efectes únics (pluges, sequeres, vents, nevades, calor extrem)
  * Impacte en agricultura, migracions animals, salut de poblacions

**CICLE DE L'AIGUA:**
- Evaporació d'oceans (més en zones càlides)
- Núvols que es mouen amb vents dominants
- Precipitació basada en temperatura, humitat i altitud
- Efecte d'ombra pluviomètrica (muntanyes bloquegen pluja)
- Inundacions i sequeres més realistes
- Pujada/baixada del nivell del mar

**CORRENTS I VENTS:**
- Corrents oceàniques (equivalents al Corrent del Golf)
- Vents dominants (alisis, vents de l'oest)
- Monzons estacionals
- Fenòmens climàtics cíclics (equivalent El Niño/La Niña)

**CANVI CLIMÀTIC:**
- Eres glacials i interglaciacions (cicles de 10.000-100.000 anys)
- Escalfament per activitat volcànica intensa
- Canvi climàtic antropogènic (civilitzacions industrials contaminen)
- Desertificació per sobreexplotació
- Efecte d'albedo (gel reflecteix → més fred)

=== BIODIVERSITAT AVANÇADA ===

**MICROORGANISMES:**
- Bacteris del sòl (fertilitat, descomposició)
- Fongs (micorizes que ajuden plantes)
- Virus i patògens que evolucionen
- Plagues que muten i desenvolupen resistències

**ANIMALS (40-60 espècies):**
- Genoma: gens per mida, velocitat, agressivitat, intel·ligència, resistència, camuflatge, venó
- Atributs derivats: esperança de vida, taxa de reproducció, dieta
- Comportament complex:
  * Migració basada en memòria generacional
  * Territorialitat i marcatge
  * Comportament de grup (ramats, bancs, colònies)
  * Cria selectiva per humans (domesticació)
  * Intel·ligència animal (alguns poden usar eines simples)
- Cadenes tròfiques dinàmiques
- Mutacions (1-5% per generació)
- Especiació per aïllament geogràfic
- Extinció en cascada (pèrdua de depredador clau → sobrepoблació presa)

**PLANTES (25-40 espècies):**
- Cicles de creixement lligats a estacions
- Requisits: temperatura, humitat, tipus de sòl
- Simbiosi (micorizes, pol·linització per insectes/ocells)
- Dispersió de llavors (vent, animals, aigua)
- Plantes parasítiques
- Espècies invasores que poden desplaçar locals

**ECOLOGIA PROFUNDA:**
- Cicle del nitrogen (leguminoses fixen nitrogen)
- Cicle del carboni (boscos absorbeixen CO2)
- Eutrofització (excés de nutrients → algues)
- Biomagnificació (toxines s'acumulen en depredadors superiors)

=== RAÇA INTEL·LIGENT AMB EVOLUCIÓ CONTEXTUAL ===

**EVOLUCIÓ SEGONS ENTORN** (CRÍTIC):
Cada civilització evoluciona els seus trets culturals segons l'entorn on es desenvolupa:

**Entorns hostils** (deserts, tundra, muntanyes altes, zones amb depredadors):
- Cultura guerrera/espartana (militar +50%, diplomàcia -30%)
- Jerarquies estrictes i governs autoritaris
- Tecnologia militar prioritzada
- Població baixa però ciutadans resistents
- Valors: honor, força, supervivència, sacrifici, disciplina
- Economia: autosuficiència, recursos estratègics
- Expansionisme agressiu o aïllacionisme defensiu

**Entorns fèrtils i tranquils** (valls fluvials, planes temperades):
- Cultura pacífica/il·lustrada (comerç +50%, ciència +30%, militar -30%)
- Governs democràtics, repúbliques mercantils
- Tecnologia agrícola, científica, artística prioritzada
- Alta densitat de població
- Valors: prosperitat, coneixement, art, comerç, llibertat
- Economia: especialització, luxes, comerç internacional
- Expansió per soft power (influència cultural/econòmica)

**Entorns marítims** (illes, costes):
- Cultura naval/exploradora (navegació +60%, comerç marítim +40%)
- Talassocràcies (govern basat en poder naval)
- Tecnologia naval i cartogràfica
- Xarxes comercials extenses
- Valors: exploració, aventura, llibertat individual
- Economia: pesca, comerç marítim, pirateria ocasional

**Entorns de jungla:**
- Cultura guerrilla/xamànica (medicina natural +50%, guerrilla +40%)
- Governs tribals o teocràtics
- Coneixement de plantes medicinals
- Aïllament cultural
- Valors: harmonia amb natura, tradició, espiritualitat

**Entorns de muntanya:**
- Cultura minera/defensiva (mineria +50%, fortificacions +40%)
- Clans o federacions de valls
- Tecnologia metal·lúrgica avançada
- Economia basada en metalls i gemmes

**DINÀMICA D'EVOLUCIÓ CULTURAL:**
- Trets culturals canvien gradualment (50-200 anys) si l'entorn canvia
- Migracions porten cultura a nous entorns → adaptació o col·lapse
- Contacte cultural causa:
  * Hibridació (fusió de trets)
  * Assimilació (cultura dominant absorbeix la feble)
  * Conflicte (rebuig mutu)
- Catàstrofes radicalitzen cultures
- Èpoques daurades (pau + prosperitat) fan cultures més obertes

Integració amb Ollama:
- Model: Llama 3.2 3B (ràpid) o Llama 3.1 8B (més intel·ligent)
- API local: http://localhost:11434
- Configuració GPU automàtica (RTX 2060)

**CAPACITATS COGNITIVES:**
- Coneixement acumulatiu (mapes, calendaris, història oral/escrita)
- Memòria generacional (mites, llegendes)
- Nivells tecnològics: pedra → bronze → ferro → pólvora → vapor → electricitat → informàtica → biotecnologia
- Progressió tecnològica influenciada per entorn i cultura

=== ESTRUCTURA SOCIAL PROFUNDA ===

**ORGANITZACIÓ SOCIAL EMERGENT:**

Nivells de complexitat social (evolució natural):
1. **Bandes Nòmades** (10-30 individus):
   - Sense jerarquia formal, lideratge per edat/experiència
   - Decisions per consens informal
   - Propietat comunal total
   - Mobilitat alta, sense assentaments permanents
   - Economia: caça-recol·lecció pura

2. **Tribus Sedentàries** (50-150 individus):
   - Líder tribal (xaman, ancià, guerrer)
   - Primeres divisions de treball (caçadors, recol·lectors, artesans)
   - Propietat familiar de terres/eines
   - Assentaments semi-permanents
   - Economia: agricultura primitiva, pastoreig
   - Estructura de clans (famílies extenses)

3. **Cacicats** (500-2000 individus):
   - Jerarquia estratificada: cacic → noble → plebeu
   - Especialització laboral clara
   - Tribut al cacic (menjar, treball)
   - Assentaments permanents amb centre cerimonial
   - Primeres lluites de poder (successió, usurpació)
   - Artesans especialitzats

4. **Ciutats-Estat** (2.000-20.000 individus):
   - Govern complex (rei, consell, burocràcia)
   - Classes socials diferenciades
   - Economia monetària emergent
   - Muralles, temples, palaus
   - Exèrcit organitzat
   - Comerç amb altres ciutats

5. **Regnes** (20.000-200.000 individus):
   - Múltiples ciutats sota un monarca
   - Aristocràcia terratinent
   - Codi legal escrit
   - Administració provincial
   - Redistribució de recursos

6. **Imperis** (200.000-5.000.000+ individus):
   - Múltiples nacions/ètnies sota un emperador
   - Burocràcia massiva
   - Xarxa de carreteres i comunicacions
   - Exèrcit professional
   - Assimilació cultural forçada o tolerància
   - Províncies amb governadors

7. **Federacions/Unions** (variable):
   - Estats semi-autònoms cooperant
   - Govern central limitat
   - Diversitat cultural preservada
   - Exèrcit conjunt
   - Zona de comerç unificat

8. **Estats-Nació** (100.000-50.000.000):
   - Identitat nacional forta
   - Ciutadania definida
   - Servei militar obligatori (sovint)
   - Sistema educatiu nacional
   - Símbolos nacionals (bandera, himne)

**ESTRUCTURA FAMILIAR EMERGENT:**
(Evoluciona segons economia i cultura)

- **Família nuclear** (2 adults + fills):
  - Predominant en cultures industrials/urbanitzades
  - Mobilitat laboral alta
  - Propietat privada individual

- **Família extensa** (avis, tios, cosins en una llar):
  - Predominant en cultures agrícoles
  - Terres familiars
  - Cura col·lectiva d'infants i ancians

- **Clans** (diverses famílies emparentades):
  - Predominant en cultures tribals/nòmades
  - Lleialtat al clan sobre l'individu
  - Vendettas entre clans

- **Poligàmia** (1 home, múltiples esposes):
  - Emergeix en cultures guerreres (molts homes moren)
  - Símbols d'estatus
  - O en cultures on homes són escassos

- **Poliàndria** (1 dona, múltiples homes):
  - Molt rar, pot emergir si dones són escasses
  - O en cultures on recursos són tan limitats que múltiples germans comparteixen esposa

- **Matrimonis arranjats**:
  - Comuns en aristocràcies (aliances polítiques)
  - En cultures amb forta autoritat parental

- **Matrimonis d'amor**:
  - Emergeix en cultures individualistes/urbanes

**XARXES SOCIALS (no digitals!):**
- **Gremis**: artesans de la mateixa professió (ferrers, fusters)
  - Controlen qualitat, preus, formació
  - Poden esdevenir molt poderosos políticament
  
- **Confraries religioses**: membres amb la mateixa fe
  - Suport mutu, caritat
  - Poden ser radicals o moderats

- **Clubs d'elit**: aristocràcia i burgesia
  - Accés per invitació/herència
  - On es fan acords polítics/econòmics

- **Sindicats**: treballadors organitzats
  - Emergeixen amb industrialització
  - Lluita per drets laborals
  - Poden fer vagues

- **Societats secretes**: 
  - Maçons, Il·luminati equivalents
  - Conspiracions reals o imaginades
  - Poden tenir poder real o ser paranoia

**MOBILITAT SOCIAL:**
(Varia enormement segons sistema)

- **Rígida** (castes, estaments feudals):
  - Impossible canviar de classe
  - Heredada al néixer
  - Pot causar revolucions si massa injust

- **Moderada** (monarquies constitucionals):
  - Difícil però possible ascendir
  - Via educació, servei militar, matrimoni
  - Burgesia pot comprar títols nobles

- **Alta** (democràcies capitalistes):
  - Meritocracia (teòricament)
  - Via educació, emprenedoria, sort
  - "Self-made man" idealitzat

- **Igualitària** (comunismes, anarquies):
  - Teòricament sense classes
  - Pràcticament sempre hi ha elits (comitè central, etc.)

**ESTRATIFICACIÓ PER CRITERIS:**

- **Econòmica**: rics vs pobres (universal)
- **Ocupacional**: guerrers > comerciants > agricultors (varia)
- **Ètnica**: grup dominant vs minoritats
- **Religiosa**: fidels vs infidels, sacerdots vs laics
- **De gènere**: patriarcat, matrilinealitat, igualitarisme
- **D'edat**: gerontocracia, cultura juvenil
- **De naixement**: aristocràcia hereditària

=== DEMOGRAFIA ULTRA-REALISTA ===

**PIRÀMIDES DE POBLACIÓ DINÀMIQUES:**

Estructura per edat i gènere que evoluciona:

- **Piràmide expansiva** (alta natalitat, alta mortalitat):
  - Base ampla (molts nens)
  - Punta estreta (pocs ancians)
  - Típic: societats pre-modernes, alta fertilitat
  - Població jove, creixement ràpid

- **Piràmide estacionària** (natalitat i mortalitat moderades):
  - Més rectangular
  - Típic: societats en transició
  - Creixement lent

- **Piràmide regressiva** (baixa natalitat, baixa mortalitat):
  - Base estreta (pocs nens)
  - Punta ampla (molts ancians)
  - Típic: societats industrials avançades
  - Població envellida, decreixement

**FACTORS DEMOGRÀFICS:**

**Taxa de Natalitat** (influenciada per):
- Accés a anticoncepció (tecnologia)
- Normes religioses (alguns cultes pro-natalistes)
- Urbanització (ciutats → menys fills)
- Educació femenina (més educació → menys fills)
- Economia (pobresa extrema → molts fills com a mà d'obra)
- Guerres (baby boom post-guerra)
- Polítiques natalistes (incentius a tenir fills)

**Taxa de Mortalitat** (influenciada per):
- Medicina (antibiotics, vacunes, cirurgia)
- Nutrició (fams → mortalitat massiva)
- Higiene (clavegueram, aigua potable)
- Guerres i genocidis
- Epidèmies (pesta, verola, grip)
- Infanticidi (en algunes cultures, control població)
- Sacrificis humans (cultures ritualístiques)

**Esperança de Vida:**
- **Paleolític**: 25-30 anys (molts moren de nadó)
- **Agrícola**: 30-35 anys
- **Medieval**: 30-40 anys
- **Pre-industrial**: 35-45 anys
- **Industrial primerenc**: 40-50 anys
- **Modern**: 60-70 anys
- **Avançat**: 75-85+ anys

(Nota: mortalitat infantil distorsiona; si sobrevius a la infància, pots viure 60+ anys fins i tot en èpoques antigues)

**ESTRUCTURA PER GÈNERE:**

- **Equilibri normal**: ~50% homes, 50% dones
- **Desequilibri per guerra**: menys homes (poden causar poligàmia)
- **Desequilibri per infanticidi selectiu**: menys dones o homes segons cultura
- **Desequilibri per migració**: homes migrants → més homes en fronteres

**COHORTS GENERACIONALS:**

Rastreja generacions amb experiències compartides:
- **Generació de la Gran Guerra**: traumatitzada, pacifista o revengista
- **Baby Boomers**: generació post-guerra, optimista
- **Generació de la Fam**: marcada per escassetat
- **Generació Digital**: primera amb tecnologia X

**TRANSICIÓ DEMOGRÀFICA:**

Model clàssic (4 etapes):
1. **Alta natalitat, alta mortalitat**: població estable però jove
2. **Alta natalitat, mortalitat en descens**: explosió demogràfica (medicina millora)
3. **Natalitat en descens, mortalitat baixa**: creixement lent
4. **Baixa natalitat, baixa mortalitat**: població envellida, potencial decreixement

**MIGRACIONS:**

**Tipus:**
- **Emigració rural-urbana**: camps → ciutats (industrialització)
- **Refugiats**: fugen de guerra/fam/persecució
- **Migrants econòmics**: busquen treball millor
- **Colonització**: ocupar terres "buides" o conquerides
- **Exili**: expulsats (deportacions, diàspores)

**Efectes:**
- **Al país d'origen**: pèrdua de mà d'obra (brain drain si són educats)
- **Al país destí**: creixement, diversitat, tensions
- **Remeses**: diners enviats a famílies
- **Asimilació vs guetos**: integració o comunitats aïllades
- **Generació 1.5**: fills de migrants, entre dues cultures

**CONTROL DE POBLACIÓ:**

- **Natural**: fam, guerra, malaltia
- **Cultural**: tabús sexuals, matrimoni tardà
- **Tecnològic**: anticoncepció, avortament
- **Polític**: llei del fill únic, esterilització forçada (distòpic)

**DEMOGRAFIA I POLÍTICA:**

- **Dividend demogràfic**: població jove treballadora → creixement econòmic
- **Bomba demogràfica**: població massa gran → col·lapse
- **Envelliment**: pensioners > treballadors → crisi fiscal
- **Infanticidi femení**: futur manca de dones → inestabilitat

=== LLENGÜES I LINGÜÍSTICA ===

**EVOLUCIÓ LINGÜÍSTICA REALISTA:**

**Proto-llengua:**
- Totes les llengües de l'espècie intel·ligent deriven d'UNA llengua primordial
- Llengua simple: 200-500 paraules, gramàtica bàsica
- Parlada per la primera tribu/bandes

**DIVERGÈNCIA PER AÏLLAMENT:**

Quan poblacions es separen (muntanyes, rius, migracions):
- **100 anys**: dialectes intel·ligibles
- **500 anys**: dialectes marcats, alguna dificultat
- **1000 anys**: llengües diferents, vagament emparentades
- **5000 anys**: famílies lingüístiques separades

**FAMÍLIES LINGÜÍSTIQUES:**

Exemple (procedural):
Proto-Mundial
├─ Família Nordica
│  ├─ Norsk
│  ├─ Islandès
│  └─ Frissi
├─ Família Meridional
│  ├─ Castellà
│  ├─ Català
│  └─ Occità
└─ Família Oriental
├─ Rus
├─ Ucraïnès
└─ Bielorús

**FACTORS D'EVOLUCIÓ:**

- **Deriva lingüística**: canvi natural amb el temps
- **Contacte**: préstecs lèxics (palabras de altres llengües)
- **Substrat**: llengua conquerida influeix conqueridors
- **Superstrat**: llengua conqueridors s'imposa
- **Creolització**: llengües noves de barreja (ex: pidgin → criollo)

**DIALECTES:**

Variacions dins la mateixa llengua:
- **Dialectes regionals**: Nord vs Sud, Ciutat vs Camp
- **Sociolectes**: classe alta vs baixa
- **Idiolectes**: manera personal de parlar

**LLENGÜES FRANQUES:**

Llengües de comunicació inter-ètnica:
- **Comercial**: ruta de la seda → llengua mercant
- **Imperial**: llengua de l'imperi (llatí, mandarí)
- **Diplomàtica**: llengua de tractats
- **Religiosa**: llengua sagrada (àrab, llatí, sànscrit)

**ESCRIPTURA:**

Evolució (no totes les cultures la desenvolupen!):
1. **Oral**: memòria, tradició oral, poesia
2. **Pictogrames**: dibuixos literals (sol = sol)
3. **Ideogrames**: símbols abstractes (cor = amor)
4. **Logo-sil·làbics**: barreja (xinès, maia)
5. **Sil·làbaris**: símbols per síl·labes (japonès kana)
6. **Abjads**: només consonants (hebreu, àrab)
7. **Alfabets**: consonants + vocals (llatí, ciríl·lic)

**FACTORS PER DESENVOLUPAR ESCRIPTURA:**
- Necessitat administrativa (comptar collites, tributs)
- Religió (preservar textos sagrats)
- Comerç (contractes, deutes)
- Conquesta (imposar llengua escrita)

**ALFABETITZACIÓ:**

- **Pre-escriptura**: 0% (només oral)
- **Elits només**: 1-5% (sacerdots, escribes, nobles)
- **Ciutadana**: 30-60% (ciutats, burgesia)
- **Universal**: 90-99% (educació obligatòria)

**PÈRDUA DE LLENGÜES:**

- **Genocidi**: extermini de parlants
- **Assimilació forçada**: prohibició, escola en llengua dominant
- **Assimilació voluntària**: prestigio de llengua dominant
- **Orfandat lingüística**: ancians parlen, joves no

**REVITALITZACIÓ:**

- **Revival**: recuperar llengua morta (hebreu modern)
- **Resistència**: moviments nacionalistes
- **Oficialització**: fer-la llengua d'estat

**MULTILINGÜISME:**

- **Individual**: persones parlen 2-5 llengües
- **Social**: país amb múltiples llengües oficials
- **Diglòssia**: llengua alta (formal) vs baixa (col·loquial)

**LLENGÜES ARTIFICIALS:**

- **Planificades**: esperanto equivalents (fraternitat universal)
- **Codis secrets**: llengües militars/espies
- **Llenguatges rituals**: només per sacerdots

**NOMS PROCEDURALS:**

Sistema per generar noms que "sonen" a una família lingüística:
- Fonologia: sons permesos (ex: japonès no té L)
- Morfologia: prefixos/sufixos típics (-ez, -son, -ovich)
- Semàntica: significats típics (colors, animals, topografia)

Exemple:
```python
# Família Nordica: consonants dures, dígrafs
noms = generar_nom(fonemes=['k','t','s','r','l'], vocals=['a','o','u'], estructura='CVC-CVC')
# Resultat: "Kartor", "Soluk", "Talras"

# Família Meridional: vocals obertes, líquides
noms = generar_nom(fonemes=['l','r','m','n'], vocals=['a','e','i','o'], estructura='CV-CV-CV')
# Resultat: "Melina", "Lorano", "Rimola"
```

=== CLASSES SOCIALS PROFUNDES ===

**SISTEMES DE CLASSES EMERGENTS:**

(No predefinits, emergen segons economia i història)

**1. SOCIETATS IGUALITÀRIES** (bandes caçadores-recol·lectores):
- Cap estratificació formal
- Prestigi per habilitats (caçador, xaman)
- Propietat comunal
- Decisions per consens
- Màxim 2-3 "nivells" informals

**2. SOCIETATS DE RANGS** (tribus, cacicats):
- Jerarquia hereditària
- **Nobles/Aristocràcia**: descendents del fundador, guerrers
- **Plebeus/Comuns**: agricultors, artesans
- Mobilitat limitada (podssibilitat d'ascens per mèrits guerrers)

**3. SOCIETATS ESTRATIFICADES** (ciutats-estat, regnes):

**Sistema de castes** (rígid, religiós):
- **Sacerdots**: contacte amb el diví, intocables
- **Guerrers**: defensa, conquesta
- **Comerciants**: producció, comerç
- **Agricultors**: alimentació
- **Intocables**: treballs impurs (carronyers, escorxadors)
- Mobilitat: ZERO (pecado canviar de casta)
- Matrimoni endogàmic (dins la casta)

**Sistema feudal** (medieval):
- **Alta noblesa**: reis, ducs, comtes (terres extenses)
- **Baixa noblesa**: cavallers, senyors locals (castells)
- **Clergat**: bisbes, abats, monjos (terres eclesiàstiques)
- **Burgesia** (emergent): mercaders rics, banquers
- **Artesans/Gremials**: mestres, oficials, aprenents
- **Camperols lliures**: petits propietaris
- **Serfs**: lligats a la terra, no esclaus però tampoc lliures
- **Esclaus**: propietat legal d'altri (si existeix esclavitud)
- Mobilitat: molt baixa (possible via església o guerra)

**4. SOCIETATS CAPITALISTES** (industrial, moderna):

- **Oligarquia/Plutocràcia**: ultra-rics (magnats, CEOs)
- **Alta burgesia**: professionals d'èxit (advocats, metges, directors)
- **Petita burgesia**: petits negocis, funcionaris
- **Classe treballadora**: obrers industrials, empleats
- **Precariat**: treballs temporals, pobresa laboral
- **Subproletariat**: desocupats crònics, indigents
- Mobilitat: variable (idealment alta, pràcticament moderada)

**5. SOCIETATS COMUNISTES** (teòriques):

- **Ideal**: classe única (proletariat)
- **Realitat**: 
  - **Nomenklatura**: elit del partit
  - **Apparatchiks**: buròcrates
  - **Proletariat**: treballadors
  - **Dissidents**: perseguits
- Mobilitat: alta dins el partit, nul·la fora

**FACTORS DE CLASSE:**

**Capital Econòmic**:
- Riquesa, propietats, rendes
- Control de mitjans de producció

**Capital Cultural**:
- Educació, gustos, maneres
- "Distinció" (Bourdieu)
- Accent, vocabulari

**Capital Social**:
- Contactes, xarxes
- "Qui coneixes"

**Capital Simbòlic**:
- Prestigi, reputació
- Títols nobiliaris, honors

**CONFLICTE DE CLASSES:**

- **Lluita de classes**: Marx (burgesia vs proletariat)
- **Revolucions**: canvi violent de sistema
- **Reformisme**: canvi gradual (socialdemocràcia)
- **Revolta**: espontània, desorganitzada
- **Guerra civil**: classe vs classe armada

**CONSCIÈNCIA DE CLASSE:**

- **Classe en si**: objectivament comparteixen condicions
- **Classe per si**: subjectivament s'identifiquen com a classe
- **Falsa consciència**: classe baixa defensa interessos de l'alta

**ESTILS DE VIDA:**

- **Consum ostentós**: mostrar riquesa (Veblen)
- **Cultura d'elit**: òpera, art, literatura clàssica
- **Cultura popular**: futbol, televisió, música pop
- **Contracultura**: rebuig de normes dominants

**MOBILITAT SOCIAL DETALLADA:**

**Ascendent**:
- **Via educació**: universitat → professió liberal
- **Via emprenedoria**: negoci d'èxit
- **Via matrimoni**: casar-se amb classe superior (hipergàmia)
- **Via militar**: ascens per mèrits
- **Via religiosa**: bisbe d'origen humil
- **Via artística**: músic/actor famós

**Descendent**:
- **Ruïna econòmica**: fallida, deutes
- **Escàndol**: pèrdua de reputació
- **Adiccions**: joc, drogues
- **Desinheretació**: expulsió de família noble

**ESTIGMA I DISCRIMINACIÓ:**

- **Classisme**: prejudicis contra classe baixa
- **Esnobisme**: menyspreu de classe alta
- **Gueto**: segregació espacial
- **Escola segregada**: educació diferent per classe

=== EDUCACIÓ I CONEIXEMENT ===

**SISTEMES EDUCATIUS EMERGENTS:**

**1. EDUCACIÓ INFORMAL** (societats pre-lletrades):
- **Mètode**: observació, imitació
- **Contingut**: supervivència (caça, recol·lecció, artesania)
- **Mestres**: pares, ancians, xaman
- **Accés**: universal dins la tribu
- **Durada**: infància-adolescència
- **Resultats**: coneixement pràctic, tradicions orals

**2. ESCOLES RELIGIOSES** (temples, monestirs):
- **Mètode**: memorització, recitació
- **Contingut**: textos sagrats, filosofia, astronomia
- **Mestres**: sacerdots, monjos
- **Accés**: elits religioses, nois de famílies nobles
- **Durada**: 5-20 anys
- **Resultats**: alfabetització, teologia, llei

**3. GREMIS I APRENENTATGE** (artesans):
- **Mètode**: pràctica supervisada
- **Contingut**: ofici específic (fuster, ferrer, etc.)
- **Mestres**: mestre artesà
- **Estructura**: aprenent (7-10 anys) → oficial → mestre
- **Accés**: fills d'artesans o pagant
- **Durada**: 7-14 anys
- **Resultats**: habilitat tècnica, ingrés al gremi

**4. ESCOLES PRIVADES** (burgesia):
- **Mètode**: classes magistrals, tutoria
- **Contingut**: llatí, matemàtiques, retòrica, música
- **Mestres**: tutors privats, professors
- **Accés**: només rics
- **Durada**: infància-joventut
- **Resultats**: preparació per universitat o negocis

**5. UNIVERSITATS** (edat moderna):
- **Mètode**: lliçons, disputatio, exàmens
- **Contingut**: trivium (gramàtica, retòrica, lògica) + quadrivium (aritmètica, geometria, astronomia, música), després especialització
- **Facultats**: arts, teologia, dret, medicina
- **Accés**: nois (inicialment), elits, després burgesia
- **Durada**: 4-8 anys (+ doctorat)
- **Resultats**: graus acadèmics, professionals

**6. EDUCACIÓ PÚBLICA OBLIGATÒRIA** (estat-nació):
- **Mètode**: classes massives, currículum estandarditzat
- **Contingut**: lectura, escriptura, aritmètica, història nacional, moral cívica
- **Mestres**: professors formats per l'estat
- **Accés**: universal (teòricament)
- **Durada**: 6-12 anys
- **Objectiu**: crear ciutadans lleials i treballadors disciplinats
- **Resultats**: alfabetització massiva, homogeneïtzació cultural

**7. SISTEMES MODERNS** (diversos):

**Capitalista**:
- Educació pública bàsica
- Universitats d'elit privades (molt cares)
- Desigualtat educativa (rics → millor educació)

**Socialista**:
- Educació gratuïta tots els nivells
- Meritocracia (teòrica)
- Adoctrinament ideològic

**Tecnocràtic**:
- Educació ultra-especialitzada
- Tracking (alumnes seleccionats per habilitats)
- STEM prioritzat sobre humanitats

**EVOLUCIÓ DEL CONEIXEMENT:**

**Edat Heroica** (oral):
- Poesia èpica, mites
- Saviesa dels ancians
- Coneixement pràctic
- Cap registre permanent

**Edat Clàssica** (escrita):
- Filosofia, ciència, matemàtiques
- Biblioteques (Alexandria equivalents)
- Escolàstica, debat
- Coneixement elitista

**Edat Fosca** (col·lapse):
- Pèrdua de textos
- Coneixement preservat en monestirs
- Regressió tècnica
- Superstició creixent

**Renaixement** (redescoberta):
- Recuperació de textos antics
- Traducció (àrab → llatí, etc.)
- Humanisme
- Primeres universitats

**Il·lustració** (raó):
- Mètode científic
- Enciclopèdies
- Secularització del saber
- Academies científiques

**Industrial** (tècnica):
- Escoles d'enginyeria
- Alfabetització massiva
- Coneixement aplicat
- Patents, propietat intel·lectual

**Digital** (informació):
- Internet equivalent
- Democratització del saber
- Sobrecàrrega informativa
- Fake news, desinformació

**INSTITUCIONS DEL CONEIXEMENT:**

**Biblioteques**:
- Reials/imperials (Alexandria)
- Monàstiques (preservació)
- Públiques (accés popular)
- Digitals

**Museus**:
- Col·leccions privades → públiques
- Patrimoni cultural
- Poden ser saquejats en guerres

**Acadèmies científiques**:
- Recerca organitzada
- Publicacions (journals)
- Peer review
- Competència per prestigi

**Laboratoris**:
- Experimentació
- R+D corporatiu o estatal
- Secrets industrials

**PÈRDUA DE CONEIXEMENT:**

**Causes**:
- **Foc**: Biblioteca d'Alexandria, bombes incendiàries
- **Conquesta**: destrucció cultural deliberada
- **Oblit**: coneixements no escrits moren amb parlants
- **Supressió**: inquisicions, censura
- **Desastre natural**: inundacions, terratrèmols
- **Format obsolet**: ja no es poden llegir (equivalent a disquets)

**Recuperació**:
- Arqueologia
- Desxifrar llengües mortes
- Reverse engineering
- Tradició oral persistent

**GENIS I INNOVADORS:**

Sistema per generar individus excepcionals:
- **Científics**: Newton, Einstein equivalents
  - Descobriment que canvia paradigma
  - Poden ser ignorats inicialment
  
- **Inventors**: Edison, Tesla equivalents
  - Tecnologia revolucionària
  - Patents, fortunes

- **Filòsofs**: Sòcrates, Kant equivalents
  - Idees que transformen cultura
  - Poden ser perseguits (Sòcrates condemnat)

- **Artistes**: Da Vinci, Shakespeare equivalents
  - Obres mestres
  - Influència duradora

**Factors**:
- **Geni innato**: atzar genètic
- **Educació**: accés a coneixement
- **Context**: renaixement vs edat fosca
- **Mecenatge**: suport financer
- **Xarxa**: col·laboració amb altres genis

**ALFABETITZACIÓ I IMPACTE:**

**Taxes**:
- 0-10%: elits només
- 10-30%: burgesia i clergat
- 30-60%: majoria urbana
- 60-90%: majoria incloent rural
- 90-99%: quasi universal

**Efectes socials**:
- Premsa (pamflets, diaris)
- Opinió pública
- Nacionalisme (llengua escrita comuna)
- Revolucions (idees radicals es difonen)
- Ciència (publicacions)

**DIFERÈNCIES DE GÈNERE:**

- **Patriarcals**: només nois educats formalment
  - Noies: costura, música, moral (si elits)
  - Camperoles: res
  
- **Progressistes**: co-educació
  - Encara biaixos (nois → STEM, noies → humanitats)
  
- **Igualitàries**: mateix accés i expectatives

**EDUCACIÓ I MOBILITAT:**

- **Meritocracia**: educació permet ascens
- **Reproducció social**: elits monopolitzen millor educació
- **Beques**: estat finança talents pobres
- **Debt**: préstecs estudiantils (endeutament)

=== LÒGICA D'EMERGÈNCIA AMB IA (MILLORADA) ===

**SISTEMA DE PROMPTS CONTEXTUALS AVANÇATS:**

**1. GENERACIÓ DE SISTEMES POLÍTICS EMERGENTS:**

Prompt a IA (Ollama):
Ets un antropòleg i politòleg creatiu. Genera un sistema polític INNOVADOR i ÚNIC (no usis sistemes històrics humans estàndards com democràcia, monarquia, etc. llevat que siguin absolutament òbvies).
CONTEXT DE LA CIVILITZACIÓ:

Nom: [NOM_CIVILITZACIÓ]
Població: [NOMBRE] habitants
Entorn: [TIPUS_BIOMA] - Hostilitat: [1-10] - Fertilitat: [1-10]
Història recent (últims 200 anys):






Trauma col·lectiu més gran: [DESCRIPCIÓ]
Moment de glòria més gran: [DESCRIPCIÓ]
Valors culturals dominants: [LISTA]
Nivell tecnològic: [EDAT_PEDRA / BRONZE / FERRO / INDUSTRIAL / DIGITAL]
Religió dominant: [DESCRIPCIÓ_BREU]
Estructura social actual: [CLASSES]
Líder actual: [NOM] - Personalitat: [TRETS]

SISTEMA POLÍTIC ACTUAL (per comparar):
[DESCRIPCIÓ_ACTUAL o "Cap (tribu primitiva)"]
INSTRUCCIONS:

Basant-te en aquest context, proposa un sistema polític que emergeixi NATURALMENT de la història i entorn d'aquesta civilització.
El sistema ha de ser:

ÚNIC i CREATIU (evita democràcia, monarquia, etc. estàndards)
COHERENT amb la seva història
PRÀCTIC (com funciona al dia a dia?)
AMB NOM ORIGINAL (inventa un terme nou)


Respon NOMÉS en aquest format JSON (sense markdown, sense explicacions extra):
{
"nom_sistema": "nom inventat del sistema",
"descripció_curta": "1-2 frases explicant l'essència",
"funcionament": "com es prenen decisions, qui governa, com s'escull",
"origen_històric": "quin esdeveniment/trauma va causar aquest sistema",
"avantatges": ["avantatge1", "avantatge2"],
"desavantatges": ["desavantatge1", "desavantatge2"],
"estabilitat": "1-10 (1=molt inestable, 10=molt estable)",
"satisfacció_popular": "1-10 (1=odiada, 10=adorada)"
}


**2. DECISIONS DE LÍDERS CONTEXTUALS:**

Prompt a IA:
Ets [NOM_LÍDER], líder de [CIVILITZACIÓ].
PERFIL:

Personalitat: [AMBICIÓS/PACIFISTA/PARANOIC/VISIONARI/TIRÀNIC/etc.]
Edat: [EDAT] anys
Anys al poder: [ANYS]
Popularitat: [1-10]
Salut: [BO/MALALT/MORIBUND]

CULTURA DE LA TEVA CIVILITZACIÓ:

Tipus cultural: [GUERRERA/PACÍFICA/MERCANTIL/RELIGIOSA/etc.] ([PERCENTATGES])
Valors: [LLISTA]
Entorn: [DESCRIPCIÓ]
Sistema polític: [NOM_SISTEMA] - [DESCRIPCIÓ]

SITUACIÓ ACTUAL:
Economia: [PROSPERA/ESTANCADA/CRISI]
Militar: [FORT/MODERAT/DÈBIL] comparada amb veïns
Població: [CREIXENT/ESTABLE/DECREIXENT]
Amenaces: [LLISTA o "Cap"]
ESDEVENIMENT:
[DESCRIPCIÓ_DETALLADA_SITUACIÓ]
OPCIONS:
A) [OPCIÓ_A]
B) [OPCIÓ_B]
C) [OPCIÓ_C]
[D) OPCIÓ_D - si aplicable]
Decideix quin camí prens com a líder. Tingues en compte:

La teva personalitat
Els valors de la teva cultura
Les conseqüències a curt i llarg termini
El que els teus ciutadans esperarien

Respon en JSON:
{
"decisió": "A/B/C/D",
"raonament": "2-3 frases explicant per què (des del punt de vista del líder)",
"motivació_principal": "PODER/SUPERVIVÈNCIA/IDEOLOGIA/ECONOMIA/RELIGIÓ/LLEGAT"
}

**3. GENERACIÓ DE RELIGIONS EMERGENTS:**

Prompt a IA:
Genera una religió/espiritualitat ÚNICA per a [CIVILITZACIÓ].
CONTEXT:

Entorn: [BIOMA] - [CARACTERÍSTIQUES CLIMÀTIQUES]
Desastres naturals freqüents: [LLISTA]
Recursos clau: [LLISTA]
Esdeveniments traumàtics: [LLISTA]
Fauna/Flora destacada: [LLISTA]
Nivell de coneixement astronòmic: [NINGÚ/BÀSIC/AVANÇAT]

PSICOLOGIA CULTURAL:

Què els fa por?: [LLISTA]
Què valoren més?: [LLISTA]
Misteris que no entenen?: [LLISTA]

Crea una religió que expliqui el seu món i doni sentit a la seva experiència.
JSON:
{
"nom": "nom de la religió/culte",
"deïtats": [
{"nom": "...", "domini": "...", "simbolisme": "..."},
...
],
"creences_nucli": ["creença1", "creença2", ...],
"pràctiques": ["ritual1", "ritual2", ...],
"tabus": ["tabú1", "tabú2", ...],
"sacerdoci": "estructura i rol dels sacerdots",
"escatologia": "què passa després de la mort",
"origen_mític": "com es va crear el món segons ells",
"to": "APOCALÍPTIC/OPTIMISTA/MÍSTIC/PRÀCTIC/FATALISTA"
}

**4. GENERACIÓ DE LLENGÜES/NOMS:**

Prompt a IA:
Genera noms que sonin naturals per a [TIPUS: persones/ciutats/regions/artefactes] de [CIVILITZACIÓ].
FONOLOGIA DE LA CULTURA:

Inspiració vaga: [CULTURA_TERRESTRE_SIMILAR] (no copiïs, només inspira't)
Entorn: [DESCRIPCIÓ]
Cultura: [TRETS]

Genera 10 noms diversos que segueixin un patró fonològic coherent però siguin únics.
JSON:
{
"noms": ["nom1", "nom2", ..., "nom10"],
"patró_fonològic": "descripció breu del so típic (ex: 'consonants dures + vocals obertes')"
}

**5. GESTIÓ DE CRISIS I ESDEVENIMENTS:**

Prompt a IA:
Ha ocorregut: [ESDEVENIMENT_DRAMÀTIC]
A [CIVILITZACIÓ]:

Població afectada: [PERCENTATGE]%
Morts estimats: [NOMBRE]
Recursos perduts: [LLISTA]
Infraestructura danyada: [DESCRIPCIÓ]

Com reacciona la població i els líders?
JSON:
{
"reacció_popular": "PÀNIC/RESILIÈNCIA/DESESPERACIÓ/FÚRIA/RESIGNACIÓ",
"resposta_governamental": "mesures preses",
"efecte_cultural_llarg_termini": "com això canvia la cultura (si canvia)",
"nous_mites_llegendes": "històries que sorgiran d'això",
"potencial_canvi_polític": "true/false - si això podria causar revolució"
}

**6. EVOLUCIÓ CULTURAL GRADUAL:**

Prompt executat cada 50-100 anys (simulats):
[CIVILITZACIÓ] ha experimentat [ANYS] anys des de l'última avaluació cultural.
CANVIS AMBIENTALS:

Clima: [CANVIS]
Recursos: [APARICIÓ/ESGOTAMENT]
Veïns: [NOVES_CIVILITZACIONS/GUERRES/PAU]

ESDEVENIMENTS MAJORS:
[LLISTA_CRONOLÒGICA]
CULTURA ACTUAL:
[DESCRIPCIÓ_DETALLADA]
Com ha evolucionat la cultura? Proposa ajustos graduals (NO revolucions llevat que siguin necessàries).
JSON:
{
"canvis_valors": {"valor": "direcció_canvi (+/-5 punts màxim)", ...},
"noves_tradicions": ["tradició1", ...],
"tradicions_perdudes": ["tradició1", ...],
"canvi_religiós": "descripció si n'hi ha",
"canvi_lingüístic": "nous termes, llengües que moren, etc.",
"narrativa": "2-3 frases narrant l'evolució"
}

**SISTEMA DE CACHING I OPTIMITZACIÓ:**

Per evitar trucar a Ollama massa:
- **Cache de decisions similars**: si situació és 90% igual, reutilitza resposta anterior
- **Batch processing**: decidir per múltiples líders simultàniament
- **Decisió automàtica per esdeveniments trivials**: només usar IA per decisions crítiques
- **Cooldown**: mateix líder no pot fer 2 decisions majors en menys de X dies

**FALLBACK SI OLLAMA NO DISPONIBLE:**

Sistema de decisions ponderades:
```python
if not ollama_available():
    # Decisió basada en personalitat i cultura
    if leader.personality == "AGGRESSIVE" and culture.military > 60:
        return "OPCIÓ_GUERRA"
    elif culture.commercial > 70:
        return "OPCIÓ_COMERÇ"
    # etc.
```

**VALIDACIÓ DE RESPOSTES IA:**
```python
response = ollama.generate(prompt)
try:
    data = json.loads(response)
    # Validar camps obligatoris
    assert "nom_sistema" in data
    assert 1 <= int(data["estabilitat"]) <= 10
    return data
except:
    # Retry o fallback
    return fallback_decision()

=== ECONOMIA EMERGENT ===

**SISTEMES ECONÒMICS NOUS:**

1. **ECONOMIA DE DONS RITUALITZADA**:
   - Intercanvi basat en regals que creen deute social
   - Més valor simbòlic que material
   - Emergeix en cultures comunitàries

2. **CAPITALISME DE RECURSOS TEMPORALS**:
   - Recursos tenen "data de caducitat" (simulant perecibilitat)
   - Monopolitzar és impossible
   - Emergeix en zones amb recursos abundants però inestables

3. **COMUNISME SELECTIU**:
   - Alguns recursos comunals (aigua, menjar bàsic)
   - Altres privats (luxes, tecnologia)
   - Barreja pràctica segons necessitat

4. **ECONOMIA DE REPUTACIÓ**:
   - Moneda basada en prestigi social, no material
   - "Ric" = respectat, no amb or
   - Emergeix en societats post-escassetat

5. **FEUDALISME CORPORATIU**:
   - Gremlis com a senyors feudals
   - Lleialtat a empresa, no a territori
   - Emergeix amb industrialització ràpida

6. **TRUEQUE COMPUTAT**:
   - Intercanvis sense moneda però amb algoritmes d'equivalència
   - Civilització avançada que rebutja diners
   - Blockchain primitiu

**RECURSOS ÚNICS:**
- **Cristalls Energètics**: només en certes coves, usen per tecnologia avançada
- **Fusta Flotant**: arbres d'una espècie rara, permeten vaixells voladors
- **Metall Viu**: mineral que "creix", revoluciona construcció

=== RELIGIÓ I ESPIRITUALITAT EMERGENT ===

**SISTEMES RELIGIOSOS NOUS:**

1. **POLITEISME DEMOCRÀTIC**:
   - Déus són "votats" pels fidels
   - Déus menys populars "moren" i en neixen de nous
   - Pantheon canviant segons necessitats socials

2. **MONOTEISME FRACTAL**:
   - Un déu que és simultàniament tots els éssers
   - Panteisme extrem
   - Emergeix en cultures filosòfiques

3. **ATEISME RITUALISTA**:
   - Cap déu però rituals complexes per ordre social
   - Quasi-religió sense supernatural
   - Sorgeix en cultures científiques que valoren tradició

4. **CULTE AL CICLE**:
   - Adoració del temps i les estacions
   - Rituals per "mantenir" el món girant
   - Emergeix en cultures agrícoles obsessionades amb calendaris

5. **VENERADORS DEL DESASTRE**:
   - Catàstrofes naturals com a déus
   - Sacrificis per aplacar volcans/terratrèmols
   - Sorgeix en zones amb desastres freqüents

6. **DUALISME EXTREM**:
   - Bé vs Mal com a forces còsmiques iguals
   - Cada individu tria bàndol conscientment
   - Guerra santa permanent

7. **TOTEMISME GENÈTIC**:
   - Cada família/clan té un animal totèmic
   - Creuen que comparteixen gens amb aquest animal
   - Tabús sobre matar el tòtem

**DINÀMICA RELIGIOSA:**
- Cismes quan sectes discrepa sobre doctrina
- Guerres de religió (croades, jihads)
- Missioners que converteixen
- Sincretisme (fusió de religions en contacte)
- Heretgies i inquisicions
- Profetes carismàtics

=== GUERRA I CONFLICTE ===

**EVOLUCIÓ MILITAR:**
- Falange → Legions → Cavalleria → Arcers → Artilleria → Armes de foc → Tancs → Aviació → (potencialment) Armes nuclears

**ESTRATÈGIA EMERGENT:**
- Logística (línies de subministrament vulnerables)
- Fortificacions (muralles, castells, búnkers)
- Setges prolongats
- Guerrilla en terreny muntanyós/jungla
- Guerra naval
- Propaganda i guerra psicològica

**CONSEQÜÈNCIES REALS:**
- Trauma col·lectiu (PTSD en societat)
- Orfes, vídues, mutilats
- Pèrdua generacional (manca de joves)
- Memorials i culte als caiguts
- Crimis de guerra i jutges
- Reparacions econòmiques

**TIPUS DE CONFLICTE:**
- Guerres de conquesta
- Guerres de religió
- Guerres comercials
- Guerres civils
- Revolucions
- Genocidis
- Resistències i guerrilles

=== DIPLOMÀCIA I POLÍTICA INTERNACIONAL ===

**IDEOLOGIES EMERGENTS:**
- Generació procedural d'ideologies segons història
- Exemple: "Harmonia Verdista" = ecologisme extrem després de deforestació massiva
- "Imperialisme Benevolent" = cultura que creu conquerir és ajudar
- "Nacionalisme Èlfico" = superioritat racial emergent

**INSTITUCIONS INTERNACIONALS:**
- Lliga de Nacions equivalent (després de gran guerra)
- Tribunal Internacional (jutjar crimis de guerra)
- Organització de Comerç Mundial
- Tractats de no proliferació (armes nuclears)

**ESPIONATGE:**
- Xarxes d'espies infiltrats
- Robatori de tecnologia
- Assassinats polítics
- Cops d'estat finançats per potències estrangeres
- Secrets d'estat (fórmules, plans militars)

**TRACTATS:**
- Pau (poden trencar-se)
- Aliança militar
- Zona de comerç lliure
- Unió aduanera
- Federació (fusió de països)
- Vassallatge (estat titella)

=== CIÈNCIA I TECNOLOGIA ===

**ÀRBRE TECNOLÒGIC DINÀMIC:**
- Foc → Roda → Escriptura → Metal·lúrgia → Agricultura avançada → Impressora → Pólvora → Motor de vapor → Electricitat → Informàtica → Internet → IA → Biotecnologia → Fusió nuclear

**REQUISITS PREVIS:**
- Necessites metal·lúrgia per fer motors
- Necessites escriptura per ciència complexa
- Necessites electricitat per computadors

**GENIS CIENTÍFICS:**
- Individus excepcionals que acceleren descobriments
- Newton, Einstein, Curie equivalents
- Poden morir en guerres (pèrdua per civilització)

**REVOLUCIONS TECNOLÒGIQUES:**
- Revolució agrícola (arades, reg)
- Revolució industrial (màquines, fàbriques)
- Revolució digital (ordinadors, internet)
- Revolució biotecnològica (modificació genètica)

**APLICACIONS:**
- Medicina: sagnies → cirurgia → antibiotics → vacunes → òrgans artificials
- Transport: a peu → cavalls → vaixells → trens → cotxes → avions → coets
- Comunicació: correus → telègraf → telèfon → ràdio → televisió → internet

=== CULTURA I ART ===

**MOVIMENTS ARTÍSTICS EMERGENTS:**
- Generats proceduralment segons èpoques
- "Brutalisme Rocós" després de guerra en muntanyes
- "Impressionisme Aquàtic" en cultures marines
- Genis artístics individuals

**ESPORTS:**
- Jocs Olímpics equivalents
- Gladiadors (cultures guerreres)
- Esports autòctons (futbol, beisbol equivalents)
- Rivalitats nacionals

**CUINA:**
- Gastronomia regional
- Intercanvi d'ingredients (Ruta de les Espècies)
- Plats nacionals emblemàtics
- Restaurants i chefs famosos

=== ASTRONOMIA ===

**SISTEMA SOLAR SIMULAT:**
- 1-3 llunes visibles
- 5-8 planetes visibles
- Eclipsis solars/lunars (calculats realment)
- Cometes periòdiques
- Calendaris basats en astronomia

**EXPLORACIÓ ESPACIAL:**
- Civilitzacions avançades envien satèl·lits
- Aterratge a lluna(es)
- Potencialment colonització espacial en fases tardanes

=== URBANISME ===

**CIUTATS REALISTES:**
- Barris: aristocràtic, burgès, obrer, marginal
- Infrastructures: clavegueram, aquaductes, ponts
- Transport públic (tramvies, metro en ciutats grans)
- Contaminació industrial
- Expansió urbana (suburbs)
- Gentrificació

**MONUMENTS:**
- Piràmides, temples, colossus
- Meravelles del món (UNESCO equivalent)
- Poden destruir-se en guerres (Biblioteca d'Alexandria)

=== HISTÒRIA I ARQUEOLOGIA ===

**MEMÒRIA COL·LECTIVA:**
- Mites fundacionals
- Herois i villans llegendaris
- Dies festius commemoratius
- Revisionisme històric

**ARQUEOLOGIA:**
- Civilitzacions antigues deixen ruïnes
- Artefactes descoberts
- Desxiframent d'escriptures mortes
- "Trobar" tecnologies perdudes

=== DESASTRES I RESILIÈNCIA ===

**MEGADESASTRES:**
- Erupcions supervolcàniques (invern volcànic global)
- Impactes d'asteroides (extinció massiva)
- Pandèmies globals (pesta negra equivalent)
- Glaciacions
- Inundacions massives per desglaç

**RECUPERACIÓ:**
- Renaixement després de col·lapse
- Històries de supervivència heroiques
- Llegat de civilitzacions perdudes (mites)

=== ESDEVENIMENTS NARRATIUS ===

**HISTÒRIES INDIVIDUALS:**
- Tracking de personatges importants (reis, profetes, científics)
- Biografies amb esdeveniments clau
- Dinasties familiars
- Assassinats, matrimonis polítics, traïcions personals

**MORALITAT EVOLUTIVA:**
- Esclavitud acceptable → abolida
- Drets de la dona evolucionen
- Drets animals en civilitzacions avançades
- Ecologisme emergent després de desastres ambientals

=== INTERFÍCIE GRÀFICA ===

Vista principal (pygame):
- Mapa renderitzat amb zoom/pan
- Capes: biomes, altitud, temperatura, humitat, ciutats, fronteres, recursos, tectònica, **hostilitat ambiental**, **fertilitat**, **trets culturals**, **corrents oceàniques**, **vents**

Panell d'informació:
- Temps (any, estació, dia)
- Controls velocitat: pausa, 1x, 10x, 100x, 1000x, 10000x
- Estadístiques globals

Mode d'inspecció (clic):
- Tile: bioma, recursos, espècies, clima
- Ciutat: població, economia, tecnologia, líder, **sistema polític**, **religió dominant**, **trets culturals**
- Esdeveniments recents

Timeline:
- Log històric filtrable
- **Canvis de sistemes polítics/religiosos destacats**

Editor de Déu:
- Modificar gens, clima, terreny
- **Modificar cultura/política directament**
- Forçar esdeveniments
- **Crear nous sistemes polítics/religiosos custom**
- Teletransportar civilitzacions

=== SISTEMA DE TEMPS ===
- Tick = 1 dia
- Velocitats ajustables
- Events: clima → geologia → biologia → economia → política → cultura → IA decisions
- Recalcul cultural cada 10-50 anys

=== PERSISTÈNCIA ===
- Save/load complet (estat del món, història, genomes, cultura)
- Format: pickle comprimit
- Autosave configurable
- Slots múltiples

=== INTEGRACIÓ OLLAMA ===
- Verificar instal·lació
- `ollama pull llama3.2:3b`
- Prompts contextuals:
  * "Proposa un sistema polític innovador per [civilització] amb història [X], entorn [Y], trauma [Z]"
  * "Decideix com a líder [nom] amb cultura [detalls] i personalitat [X] davant situació [Y]"
- Fallback si Ollama no disponible

=== OPTIMITZACIÓ ===
- Quadtree/spatial hashing
- Update selectiu
- Threading per IA
- LOD segons zoom
- Profiling

=== INSTRUCCIONS ===
1. Estructura del projecte
2. Generació món amb geologia dinàmica
3. Rendering amb totes les capes
4. Sistema de temps i clima
5. Biologia amb genètica i ecologia
6. Raça intel·ligent amb cultura emergent
7. **Sistema de generació procedural de sistemes polítics/religiosos/econòmics**
8. Ollama amb prompts emergents
9. Economia, política, guerra
10. Demografia, llengües, classes socials
11. Esdeveniments, catàstrofes, resiliència
12. Interfície completa amb editor
13. Save/load
14. Polish i optimització

**PRIORITAT MÀXIMA:**
- Sistemes emergents (política, religió, economia) han de ser GENERATS, no predefinits
- Usa IA per crear noms de sistemes, descripcions, mecàniques
- Cada civilització ha de ser única culturalment
- Història ha de sentir-se orgànica, no scriptada

Proporciona codi modular, ben comentat, amb type hints. README amb instal·lació Ollama i guia d'ús.

COMENÇA PAS A PAS: estructura, món, rendering bàsic, després afegeix complexitat gradualment.
