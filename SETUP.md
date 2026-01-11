# Guia d'Instal·lació i Configuració - Overworld

## Requisits del Sistema

- **Python**: 3.8 o superior
- **Sistema Operatiu**: Linux, macOS, Windows
- **GPU**: Recomanada per Ollama (RTX 2060 o superior)
- **RAM**: Mínim 8GB, recomanat 16GB
- **Espai en disc**: ~5GB per models d'Ollama

## Instal·lació

### 1. Clonar el repositori

```bash
git clone <repository-url>
cd overworld
```

### 2. Crear entorn virtual (recomanat)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate  # Windows
```

### 3. Instal·lar dependències Python

```bash
pip install -r requirements.txt
```

### 4. Instal·lar Ollama

#### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### macOS

```bash
brew install ollama
```

#### Windows

Descarrega l'instal·lador des de: https://ollama.com/download

### 5. Descarregar el model d'IA

```bash
# Model ràpid (recomanat per començar)
ollama pull llama3.2:3b

# O model més intel·ligent (requereix més memòria)
ollama pull llama3.1:8b
```

### 6. Iniciar el servidor Ollama

```bash
ollama serve
```

Deixa aquesta terminal oberta. Ollama escoltarà a `http://localhost:11434`

## Execució

En una **nova terminal**:

```bash
cd overworld
source venv/bin/activate  # Si fas servir entorn virtual
python main.py
```

## Verificar la instal·lació

El programa hauria de mostrar:

```
============================================================
  OVERWORLD - Simulació Procedural de Món
  Versió 0.1.0 - En desenvolupament
============================================================

Provant sistemes bàsics...

✓ Configuració carregada
✓ Gestor de temps inicialitzat
✓ Sistema d'esdeveniments inicialitzat
...
```

## Configuració

Pots modificar la configuració editant `overworld/core/config.py`:

- **Mida del mapa**: `WorldConfig.width` i `WorldConfig.height`
- **Nombre de plaques**: `WorldConfig.num_plates`
- **Model d'Ollama**: `OllamaConfig.model`
- **Resolució**: `GraphicsConfig.window_width` i `window_height`

## Resolució de problemes

### Ollama no connecta

1. Verifica que el servidor està actiu: `curl http://localhost:11434`
2. Assegura't que el model està descarregat: `ollama list`

### Error de memòria

- Redueix la mida del mapa a `WorldConfig`
- Usa el model més petit: `llama3.2:3b`
- Desactiva Ollama temporalment: `OllamaConfig.enabled = False`

### Problemes amb pygame

```bash
# Linux: pot necessitar dependències SDL
sudo apt-get install python3-pygame

# macOS
brew install sdl2 sdl2_image sdl2_ttf

# Windows: hauria de funcionar amb pip install pygame
```

## Desenvolupament

### Executar tests (quan estiguin implementats)

```bash
pytest tests/
```

### Formatació de codi

```bash
black overworld/
isort overworld/
```

## Estat del Projecte

- [x] Estructura bàsica
- [ ] Generació del món
- [ ] Rendering amb pygame
- [ ] Sistema climàtic
- [ ] Biologia
- [ ] Civilitzacions amb IA
- [ ] Interfície completa
- [ ] Save/Load

Més informació: veure `README.md`
