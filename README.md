# 🌍 OVERWORLD - Advanced Procedural World Simulation

Simulació procedural completa d'un món amb generació dinàmica, sistemes emergents, civilitzacions amb IA i interfície gràfica avançada.

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![Pygame 2.5+](https://img.shields.io/badge/pygame-2.5%2B-green)
![License MIT](https://img.shields.io/badge/license-MIT-blue)

## 🚀 Característiques Principals

### 🗺️ Generació Procedural del Món
- **Mapes personalitzables**: Fins a 500x500 tiles
- **Noise Perlin** per altitud, humitat i temperatura
- **20+ biomes** diferents (oceà profund, muntanyes, deserts, boscos, tundra, etc.)
- **Recursos naturals**: Or, plata, ferro, coure, urani, carbó, petroli, gas, gemmes
- **Rius procedurals** següent gradients d'altitud

### 🌋 Tectònica de Plaques
- **6-12 plaques tectòniques** en moviment constant (2-10 cm/any)
- **3 tipus de límits**: Convergents (muntanyes/volcans), Divergents (rifts), Transformants (falles)
- **Esdeveniments geològics realistes**: Terratrèmols (escala Richter), erupcions volcàniques, formació de muntanyes
- **Modificació dinàmica del terreny**

### 🌡️ Sistema Climàtic Avançat
- **4 estacions** amb efectes diferenciats
- **Cicle complet de l'aigua**: Evaporació, condensació, precipitació, infiltració, escorrentia
- **Cel·les atmosfèriques** (Hadley, Ferrel, Polar) per vents globals
- **10 zones climàtiques Köppen**: Desert, Polar, Tundra, Tropical, Temperat, etc.
- **Patrons meteorològics**: Temperatura, precipitació, vents, núvols

### 🏛️ Civilitzacions amb IA
- **Creació dinàmica** de fins a 20 civilitzacions
- **Evolució cultural** segons l'entorn (guerrers en zones hostils, pacífics en zones fèrtils, navals a les costes)
- **Sistemes polítics emergents** generats proceduralment amb IA (Ollama)
- **Sistemes religiosos** únics per cada civilització
- **Sistemes econòmics** adaptat a recursos i cultura
- **Models IA únics** per civilització (llama3.2:3b, qwen2.5:3b, phi3:3.8b, gemma2:2b, mistral:7b)

### 🗣️ Llengües i Evolució Lingüística
- **Generació procedural** de llengües amb fonètica única
- **Famílies lingüístiques** amb evolució temporal
- **Préstecs lingüístics** entre civilitzacions properes
- **Deriva natural** (1-3% cada 100 anys)
- **Lingua franca** per globalització
- **Fonologia adaptativa** per loanwords

### 👥 Demografia Ultra-Realista
- **Piràmides de població** amb 8 grups d'edat i distribució per gènere
- **Tendències demogràfiques**: Taxa de natalitat, mortalitat, esperança de vida, fertilitat
- **Sistema de migracions** amb 8 raons diferents (guerra, fam, economia, religió, etc.)
- **Perfils d'edat** dels migrants segons raó

### 🎨 Cultura i Art
- **Moviments culturals** generats amb IA
- **8 formes d'art**: Arquitectura, escultura, pintura, música, literatura, teatre, dansa, poesia
- **Obres mestres** amb títols i artistes procedurals
- **Influència cultural** entre civilitzacions

### 🤝 Diplomàcia i Guerra
- **6 tipus de relacions**: Aliats, Amistós, Neutral, Desagradable, Hostil, En guerra
- **7 tipus de tractats**: Pau, comerç, pacte defensiu, aliança militar, no-agressió, vassallatge, intercanvi cultural
- **Sistema d'opinió** (-100 a +100)
- **Càlcul de forces militars**: Soldats × tecnologia × moral × experiència × subministraments
- **Simulació de batalles** amb casualties realistes
- **Warscore** per determinar victòria/derrota

### 🖥️ Interfície Gràfica Avançada (1600x900)

**12 MODES DE VISUALITZACIÓ:**
- 🗺️ **Terreny**: Altitud amb colors realistes
- 🌳 **Biomes**: Distribució de tots els biomes
- 🏛️ **Civilitzacions**: Territoris i ciutats
- ⚖️ **Política**: Sistemes polítics
- 🕊️ **Religió**: Sistemes religiosos
- 💰 **Economia**: Sistemes econòmics i recursos
- 👥 **Demografia**: Densitat i piràmides de població
- 🎨 **Cultura**: Moviments culturals i art
- 🤝 **Diplomàcia**: Relacions, aliances i guerres
- 🌋 **Plaques**: Plaques tectòniques amb colors
- 🌡️ **Clima**: Classificació Köppen
- 🗣️ **Llengües**: Famílies lingüístiques

**COMPONENTS UI:**
- ✅ 17 botons interactius amb hover effects
- ✅ 2 panells laterals (informació detallada + estadístiques globals)
- ✅ Mini-mapa amb vista general
- ✅ Timeline amb controls temporals
- ✅ Càmera amb pan (WASD/fletxes)
- ✅ Click per seleccionar tiles

## 📋 Requisits

- **Python 3.11+**
- **Ollama** (opcional però recomanat per IA): https://ollama.ai

## 🔧 Instal·lació

### 1. Clonar el repositori
```bash
git clone https://github.com/BotVHS/overworld.git
cd overworld
```

### 2. Instal·lar dependencies
```bash
pip install -r requirements.txt
```

### 3. Instal·lar Ollama (opcional)
```bash
# Linux/Mac
curl https://ollama.ai/install.sh | sh

# Windows: Descarrega l'instal·lador de https://ollama.ai

# Descarrega models recomanats
ollama pull llama3.2:3b
ollama pull qwen2.5:3b
ollama pull phi3:3.8b
```

**Nota**: Si Ollama no està disponible, tots els sistemes tenen fallback procedural automàtic.

## 🎮 Ús

### Llançar la interfície gràfica completa
```bash
python3 main_ui.py
```

### Controls
- **🖱️ Click**: Selecciona tile i mostra informació detallada
- **⌨️ WASD/Fletxes**: Mou càmera pel món
- **⌨️ Espai**: Play/Pause simulació temporal
- **⌨️ +/-**: Avança/retrocedeix 10 anys
- **⌨️ 1-5**: Canvi ràpid entre modes:
  - 1: Terreny
  - 2: Biomes
  - 3: Civilitzacions
  - 4: Tectònica
  - 5: Clima
- **⌨️ ESC**: Tanca aplicació

### Tests individuals
```bash
# Test de llengua i evolució lingüística
python3 test_language_evolution.py

# Test de diplomàcia i guerra
python3 test_diplomacy_warfare.py

# Test de cultura i demografia
python3 test_culture_demographics.py

# Test de tectònica i clima
python3 test_tectonics_climate.py

# Test d'inicialització de UI
python3 test_ui_init.py
```

## 📁 Estructura del Projecte

```
overworld/
├── overworld/
│   ├── ai/
│   │   ├── ollama_client.py          # Client Ollama per IA
│   │   └── civilization_ai_models.py  # Models IA únics per civilització
│   ├── civilization/
│   │   ├── civilization.py            # Sistema de civilitzacions
│   │   ├── culture.py                 # Cultures i trets
│   │   ├── leader.py                  # Líders amb IA
│   │   ├── political_system.py        # Sistemes polítics emergents
│   │   ├── religious_system.py        # Sistemes religiosos emergents
│   │   ├── economic_system.py         # Sistemes econòmics
│   │   ├── language.py                # Llengües procedurals
│   │   ├── language_evolution.py      # Evolució lingüística amb IA
│   │   ├── diplomacy.py               # Diplomàcia i tractats
│   │   ├── warfare.py                 # Sistema de guerra
│   │   ├── cultural_movements.py      # Moviments culturals i art
│   │   └── demographics.py            # Demografia i migracions
│   ├── world/
│   │   ├── world.py                   # Generació del món
│   │   ├── biome.py                   # Definicions de biomes
│   │   ├── plate_tectonics.py         # Tectònica de plaques
│   │   └── climate_system.py          # Sistema climàtic
│   └── ui/
│       ├── advanced_ui.py             # Interfície gràfica pygame
│       └── __init__.py
├── main_ui.py                         # Script principal amb UI
├── test_*.py                          # Tests de cada sistema
├── requirements.txt                   # Dependencies Python
└── README.md                          # Aquest fitxer
```

## 🎯 Estat del Projecte

### ✅ Implementat (81% completat)

1. ✅ **Generació procedural del món** (altitud, humitat, temperatura, biomes, recursos)
2. ✅ **Tectònica de plaques** (12 plaques, límits, esdeveniments geològics)
3. ✅ **Sistema climàtic** (4 estacions, cicle de l'aigua, vents, Köppen)
4. ✅ **Civilitzacions** (creació dinàmica, ciutats, expansió)
5. ✅ **Sistemes polítics emergents** (generats amb IA procedural)
6. ✅ **Sistemes religiosos** (generats amb IA procedural)
7. ✅ **Sistemes econòmics** (adaptats a recursos i cultura)
8. ✅ **Líders amb IA** (decisions contextuals amb Ollama)
9. ✅ **Llengües i evolució** (fonètica única, préstecs, deriva)
10. ✅ **Diplomàcia** (relacions, tractats, opinions)
11. ✅ **Guerra** (forces militars, batalles, warscore)
12. ✅ **Cultura i art** (moviments culturals, obres mestres)
13. ✅ **Demografia** (piràmides, migracions, tendències)
14. ✅ **Models IA únics** (cada civilització amb model diferent)
15. ✅ **Interfície gràfica** (12 modes, controls, panells)

### 🚧 Pendent

- **Àrbre tecnològic** (progressió: pedra → bronze → ferro → industrial)
- **Editor de Déu** (mode debug per modificar món en temps real)
- **Save/Load** (persistència de simulacions)
- **Optimització** (threading, spatial hashing, LOD)

## 🔬 Exemples de Sortida

### Llengües Generades
```
Thaldran: "Kethros" (salutació), "Velmara" (aigua), "Thunor" (cel)
Ithrath: "Marelos" (mar), "Ventaris" (vent), "Solmar" (sol)
```

### Sistemes Polítics Emergents
```
Jardran: "Consell dels Ancians Savis"
  - Govern per consens de 7 ancians
  - Decisions basades en coneixement acumulat
  - Estabilitat: 8/10, Popularitat: 7/10
```

### Esdeveniments Geològics
```
Any 1: 🌋 Erupció volcànica en zona de subducció a (90, 98)
Any 2: 🌍 Terratrèmol de magnitud 8.5 a (13, 78)
Any 3: ⛰️ Formació de muntanyes per col·lisió a (54, 146)
```

## 🤝 Contribucions

Les contribucions són benvingudes! Si us plau:
1. Fork el projecte
2. Crea una branca (`git checkout -b feature/NovaFuncionalitat`)
3. Commit els canvis (`git commit -m 'Afegeix nova funcionalitat'`)
4. Push a la branca (`git push origin feature/NovaFuncionalitat`)
5. Obre un Pull Request

## 📝 Llicència

Aquest projecte està sota llicència MIT. Vegeu el fitxer `LICENSE` per més detalls.

## 🙏 Agraïments

- **Ollama** per la integració IA local
- **Pygame** per la interfície gràfica
- **Perlin Noise** per generació procedural
- Comunitat de simulacions procedurals

## 📧 Contacte

Per preguntes o suggeriments, obre un issue a GitHub.

---

**Fet amb ❤️ i Python**
