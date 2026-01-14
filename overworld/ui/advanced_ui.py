"""
Advanced UI - Interfície gràfica avançada amb múltiples capes

Interfície pygame completa amb:
- 15+ modes de visualització
- Controls interactius
- Mini-mapa
- Panells d'informació
- Timeline temporal
- Zoom i pan
"""
import pygame
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
from dataclasses import dataclass
import math


class ViewMode(Enum):
    """Modes de visualització"""
    TERRAIN = "terrain"
    BIOMES = "biomes"
    RESOURCES = "resources"
    CIVILIZATIONS = "civilizations"
    POLITICAL = "political"
    RELIGIOUS = "religious"
    ECONOMIC = "economic"
    DEMOGRAPHICS = "demographics"
    CULTURE = "culture"
    DIPLOMACY = "diplomacy"
    WARFARE = "warfare"
    LANGUAGES = "languages"
    TECTONICS = "tectonics"
    CLIMATE = "climate"
    TEMPERATURE = "temperature"
    PRECIPITATION = "precipitation"
    WIND = "wind"


@dataclass
class UIButton:
    """Botó de la interfície"""
    x: int
    y: int
    width: int
    height: int
    text: str
    color: Tuple[int, int, int]
    text_color: Tuple[int, int, int] = (255, 255, 255)
    hover_color: Optional[Tuple[int, int, int]] = None
    callback: Optional[Callable] = None
    icon: Optional[str] = None

    def contains_point(self, px: int, py: int) -> bool:
        """Comprova si un punt està dins del botó"""
        return self.x <= px <= self.x + self.width and self.y <= py <= self.y + self.height

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, is_hover: bool = False):
        """Dibuixa el botó"""
        color = self.hover_color if is_hover and self.hover_color else self.color

        # Dibuixa rectangle
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)

        # Dibuixa text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect)


@dataclass
class InfoPanel:
    """Panell d'informació lateral"""
    x: int
    y: int
    width: int
    height: int
    title: str
    lines: List[str]
    background_color: Tuple[int, int, int] = (20, 20, 30)
    border_color: Tuple[int, int, int] = (100, 100, 120)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, title_font: pygame.font.Font):
        """Dibuixa el panell"""
        # Fons
        pygame.draw.rect(surface, self.background_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.width, self.height), 2)

        # Títol
        title_surface = title_font.render(self.title, True, (255, 255, 100))
        surface.blit(title_surface, (self.x + 10, self.y + 10))

        # Línies
        y_offset = 40
        for line in self.lines:
            if line.strip():
                text_surface = font.render(line, True, (255, 255, 255))
                surface.blit(text_surface, (self.x + 10, self.y + y_offset))
                y_offset += 20


class AdvancedUI:
    """
    Interfície gràfica avançada amb múltiples funcionalitats
    """

    def __init__(self, screen_width: int = 1600, screen_height: int = 900):
        """
        Args:
            screen_width: Amplada de la pantalla
            screen_height: Alçada de la pantalla
        """
        pygame.init()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Overworld - Advanced Simulation")

        # Fonts
        self.font_small = pygame.font.Font(None, 18)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        self.font_title = pygame.font.Font(None, 48)

        # Mode de visualització actual
        self.current_view = ViewMode.TERRAIN

        # Camera
        self.camera_x = 0
        self.camera_y = 0
        self.zoom_level = 1.0
        self.tile_size = 4  # Píxels per tile

        # Mapa i mini-mapa
        self.map_surface = None
        self.minimap_size = 200
        self.minimap_x = screen_width - self.minimap_size - 10
        self.minimap_y = 10

        # UI panels
        self.info_panel = InfoPanel(
            x=10,
            y=screen_height - 250,
            width=350,
            height=240,
            title="Informació",
            lines=[]
        )

        self.stats_panel = InfoPanel(
            x=screen_width - 360,
            y=screen_height - 250,
            width=350,
            height=240,
            title="Estadístiques",
            lines=[]
        )

        # Timeline
        self.current_year = 0
        self.is_playing = False
        self.time_speed = 1.0

        # Botons
        self.buttons: List[UIButton] = []
        self._create_buttons()

        # Tile seleccionat
        self.selected_tile: Optional[Tuple[int, int]] = None
        self.hover_tile: Optional[Tuple[int, int]] = None

        # Dades del món
        self.world = None
        self.civilizations = None
        self.tectonics = None
        self.climate = None

        # Colors
        self.COLORS = {
            'water_deep': (0, 50, 100),
            'water_shallow': (0, 100, 150),
            'beach': (238, 214, 175),
            'plains': (180, 200, 120),
            'forest': (34, 139, 34),
            'mountain': (139, 137, 137),
            'snow': (255, 250, 250),
            'desert': (237, 201, 175)
        }

    def _create_buttons(self):
        """Crea botons de la interfície"""
        button_width = 120
        button_height = 30
        button_y = 10
        button_spacing = 5

        view_modes = [
            (ViewMode.TERRAIN, "🗺️ Terreny", (60, 60, 80)),
            (ViewMode.BIOMES, "🌳 Biomes", (40, 100, 40)),
            (ViewMode.CIVILIZATIONS, "🏛️ Civs", (150, 80, 30)),
            (ViewMode.POLITICAL, "⚖️ Política", (80, 80, 150)),
            (ViewMode.RELIGIOUS, "🕊️ Religió", (180, 150, 50)),
            (ViewMode.ECONOMIC, "💰 Economia", (200, 150, 30)),
            (ViewMode.DEMOGRAPHICS, "👥 Demografia", (100, 150, 200)),
            (ViewMode.CULTURE, "🎨 Cultura", (200, 100, 200)),
            (ViewMode.DIPLOMACY, "🤝 Diplomàcia", (100, 200, 100)),
            (ViewMode.TECTONICS, "🌋 Plaques", (200, 50, 50)),
            (ViewMode.CLIMATE, "🌡️ Clima", (100, 150, 250)),
            (ViewMode.LANGUAGES, "🗣️ Llengües", (150, 100, 150)),
        ]

        x = 10
        for mode, text, color in view_modes:
            button = UIButton(
                x=x,
                y=button_y,
                width=button_width,
                height=button_height,
                text=text,
                color=color,
                hover_color=tuple(min(255, c + 30) for c in color),
                callback=lambda m=mode: self.set_view_mode(m)
            )
            self.buttons.append(button)
            x += button_width + button_spacing

        # Botons de control temporal
        timeline_y = button_y + button_height + 10
        timeline_buttons = [
            ("⏮️ Start", (60, 60, 80), lambda: self.reset_time()),
            ("⏸️ Pause", (80, 60, 60), lambda: self.toggle_play()),
            ("▶️ Play", (60, 120, 60), lambda: self.toggle_play()),
            ("⏭️ +10y", (60, 80, 120), lambda: self.advance_years(10)),
            ("⏩ +100y", (60, 60, 150), lambda: self.advance_years(100)),
        ]

        x = 10
        for text, color, callback in timeline_buttons:
            button = UIButton(
                x=x,
                y=timeline_y,
                width=90,
                height=button_height,
                text=text,
                color=color,
                hover_color=tuple(min(255, c + 30) for c in color),
                callback=callback
            )
            self.buttons.append(button)
            x += 90 + button_spacing

    def set_view_mode(self, mode: ViewMode):
        """Canvia el mode de visualització"""
        self.current_view = mode
        print(f"📺 Canviat a mode: {mode.value}")

    def toggle_play(self):
        """Alterna reproducció temporal"""
        self.is_playing = not self.is_playing

    def reset_time(self):
        """Reinicia el temps"""
        self.current_year = 0
        self.is_playing = False

    def advance_years(self, years: int):
        """Avança anys"""
        self.current_year += years
        print(f"⏭️ Avanç a any {self.current_year}")

    def load_world(self, world, civilizations=None, tectonics=None, climate=None):
        """
        Carrega dades del món

        Args:
            world: Objecte World
            civilizations: CivilizationManager opcional
            tectonics: PlateTectonicsSystem opcional
            climate: ClimateSystem opcional
        """
        self.world = world
        self.civilizations = civilizations
        self.tectonics = tectonics
        self.climate = climate

        # Genera superfície del mapa
        self._generate_map_surface()

    def _generate_map_surface(self):
        """Genera superfície del mapa segons mode actual"""
        if not self.world:
            return

        width = self.world.width * self.tile_size
        height = self.world.height * self.tile_size

        self.map_surface = pygame.Surface((width, height))

        for x in range(self.world.width):
            for y in range(self.world.height):
                tile = self.world.get_tile(x, y)
                if not tile:
                    continue

                color = self._get_tile_color(tile, x, y)

                pygame.draw.rect(
                    self.map_surface,
                    color,
                    (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                )

    def _get_tile_color(self, tile, x: int, y: int) -> Tuple[int, int, int]:
        """Obté color d'un tile segons mode de visualització"""
        if self.current_view == ViewMode.TERRAIN:
            # Mapa d'altitud
            if tile.is_water:
                if tile.altitude < 0.3:
                    return self.COLORS['water_deep']
                else:
                    return self.COLORS['water_shallow']
            else:
                if tile.altitude < 0.4:
                    return self.COLORS['beach']
                elif tile.altitude < 0.6:
                    return self.COLORS['plains']
                elif tile.altitude < 0.8:
                    return self.COLORS['forest']
                else:
                    return self.COLORS['mountain']

        elif self.current_view == ViewMode.BIOMES:
            # Mapa de biomes
            from ..world.biome import BIOME_DEFINITIONS
            if tile.biome and tile.biome in BIOME_DEFINITIONS:
                return BIOME_DEFINITIONS[tile.biome].color
            return (100, 100, 100)

        elif self.current_view == ViewMode.TEMPERATURE:
            # Mapa de temperatura
            temp = tile.temperature
            if temp < -20:
                return (0, 0, 150)  # Molt fred
            elif temp < 0:
                return (100, 100, 200)  # Fred
            elif temp < 15:
                return (100, 200, 100)  # Temperat
            elif temp < 25:
                return (200, 200, 0)  # Càlid
            else:
                return (200, 0, 0)  # Molt càlid

        elif self.current_view == ViewMode.CIVILIZATIONS:
            # Mapa de civilitzacions
            if self.civilizations:
                for civ in self.civilizations.civilizations:
                    if (x, y) in [(c.x, c.y) for c in civ.cities]:
                        # Color únic per civilització
                        h = hash(civ.name) % 360
                        return self._hsv_to_rgb(h, 0.7, 0.9)

            # Terreny de fons
            return (50, 50, 50) if not tile.is_water else (0, 50, 100)

        elif self.current_view == ViewMode.TECTONICS:
            # Mapa de plaques tectòniques
            if self.tectonics:
                plate = self.tectonics.get_plate_at(x, y)
                if plate:
                    # Color per placa
                    h = (plate.plate_id * 40) % 360
                    s = 0.8 if plate.plate_type.value == "oceanic" else 0.5
                    return self._hsv_to_rgb(h, s, 0.7)

            return (50, 50, 50)

        elif self.current_view == ViewMode.CLIMATE:
            # Mapa climàtic Köppen
            if self.climate:
                climate_type = self.climate.get_climate_classification(x, y)
                climate_colors = {
                    'Tropical Rainforest': (0, 100, 0),
                    'Tropical Monsoon': (50, 150, 50),
                    'Tropical Savanna': (150, 200, 100),
                    'Desert': (237, 201, 175),
                    'Arid': (210, 180, 140),
                    'Steppe': (200, 200, 150),
                    'Mediterranean': (200, 150, 100),
                    'Humid Continental': (100, 150, 200),
                    'Oceanic': (100, 200, 250),
                    'Subarctic': (150, 200, 250),
                    'Tundra': (200, 230, 255),
                    'Polar': (255, 255, 255)
                }
                return climate_colors.get(climate_type, (100, 100, 100))

            return (100, 100, 100)

        # Mode per defecte
        return (100, 100, 100)

    def _hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Converteix HSV a RGB"""
        h = h / 60.0
        i = int(h)
        f = h - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))

        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q

        return (int(r * 255), int(g * 255), int(b * 255))

    def update_info_panel(self, tile_x: int, tile_y: int):
        """Actualitza panell d'informació amb dades del tile"""
        if not self.world:
            return

        tile = self.world.get_tile(tile_x, tile_y)
        if not tile:
            return

        lines = [
            f"Posició: ({tile_x}, {tile_y})",
            f"Altitud: {tile.altitude:.2f}",
            f"Temperatura: {tile.temperature:.1f}°C",
            f"Humitat: {tile.humidity:.1%}",
            ""
        ]

        # Bioma
        if tile.biome:
            from ..world.biome import BIOME_DEFINITIONS
            if tile.biome in BIOME_DEFINITIONS:
                lines.append(f"Bioma: {BIOME_DEFINITIONS[tile.biome].name}")

        # Recursos
        if tile.resources:
            lines.append("Recursos:")
            for resource, amount in list(tile.resources.items())[:3]:
                if amount > 10:
                    lines.append(f"  {resource}: {amount:.0f}")

        # Placa tectònica
        if self.tectonics:
            plate = self.tectonics.get_plate_at(tile_x, tile_y)
            if plate:
                lines.append("")
                lines.append(f"Placa {plate.plate_id} ({plate.plate_type.value})")
                lines.append(f"Velocitat: {plate.get_speed():.1f} cm/any")

        # Clima
        if self.climate:
            weather = self.climate.weather_patterns.get((tile_x, tile_y))
            if weather:
                lines.append("")
                lines.append(f"Clima: {self.climate.get_climate_classification(tile_x, tile_y)}")
                lines.append(f"Precipitació: {weather.precipitation:.1f} mm/mes")

        self.info_panel.lines = lines

    def draw(self):
        """Dibuixa tota la interfície"""
        # Fons negre
        self.screen.fill((10, 10, 15))

        # Dibuixa mapa
        if self.map_surface:
            # Calcula viewport
            viewport_width = self.screen_width
            viewport_height = self.screen_height - 100

            # Dibuixa porció visible del mapa
            self.screen.blit(
                self.map_surface,
                (0, 80),
                (self.camera_x, self.camera_y, viewport_width, viewport_height)
            )

        # Dibuixa mini-mapa
        self._draw_minimap()

        # Dibuixa botons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            is_hover = button.contains_point(*mouse_pos)
            button.draw(self.screen, self.font_small, is_hover)

        # Dibuixa panells
        self.info_panel.draw(self.screen, self.font_small, self.font_medium)
        self.stats_panel.draw(self.screen, self.font_small, self.font_medium)

        # Dibuixa timeline
        self._draw_timeline()

        # Dibuixa overlay d'informació
        self._draw_overlay_info()

        pygame.display.flip()

    def _draw_minimap(self):
        """Dibuixa mini-mapa"""
        if not self.map_surface:
            return

        # Escala el mapa sencer al mini-mapa
        minimap_surface = pygame.transform.scale(
            self.map_surface,
            (self.minimap_size, self.minimap_size)
        )

        # Dibuixa mini-mapa
        self.screen.blit(minimap_surface, (self.minimap_x, self.minimap_y))

        # Marc
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (self.minimap_x, self.minimap_y, self.minimap_size, self.minimap_size),
            2
        )

    def _draw_timeline(self):
        """Dibuixa línia temporal"""
        timeline_y = self.screen_height - 280
        timeline_x = 380
        timeline_width = self.screen_width - 760

        # Fons
        pygame.draw.rect(
            self.screen,
            (30, 30, 40),
            (timeline_x, timeline_y, timeline_width, 40)
        )
        pygame.draw.rect(
            self.screen,
            (100, 100, 120),
            (timeline_x, timeline_y, timeline_width, 40),
            2
        )

        # Text any actual
        year_text = self.font_large.render(f"Any: {self.current_year}", True, (255, 255, 100))
        self.screen.blit(year_text, (timeline_x + 10, timeline_y + 5))

        # Estat de reproducció
        status = "▶️ Reproduint" if self.is_playing else "⏸️ Pausat"
        status_text = self.font_medium.render(status, True, (200, 200, 200))
        self.screen.blit(status_text, (timeline_x + timeline_width - 150, timeline_y + 10))

    def _draw_overlay_info(self):
        """Dibuixa informació overlay (mode actual, FPS, etc.)"""
        # Mode actual
        mode_text = f"Mode: {self.current_view.value.upper()}"
        text_surface = self.font_medium.render(mode_text, True, (255, 255, 100))
        self.screen.blit(text_surface, (self.screen_width // 2 - 100, 10))

        # Llegenda segons mode
        legend_y = 60
        if self.current_view == ViewMode.TERRAIN:
            legends = [
                ("Profund", self.COLORS['water_deep']),
                ("Aigua", self.COLORS['water_shallow']),
                ("Platja", self.COLORS['beach']),
                ("Plains", self.COLORS['plains']),
                ("Bosc", self.COLORS['forest']),
                ("Muntanya", self.COLORS['mountain'])
            ]
            self._draw_legend(legends, legend_y)

    def _draw_legend(self, items: List[Tuple[str, Tuple[int, int, int]]], y: int):
        """Dibuixa llegenda de colors"""
        x = self.screen_width // 2 - 300

        for text, color in items:
            # Quadrat de color
            pygame.draw.rect(self.screen, color, (x, y, 20, 20))
            pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 20, 20), 1)

            # Text
            text_surface = self.font_small.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (x + 25, y + 2))

            x += 100

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Gestiona esdeveniments pygame

        Args:
            event: Esdeveniment pygame

        Returns:
            False si s'ha de tancar, True altrament
        """
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Comprova clicks en botons
            for button in self.buttons:
                if button.contains_point(*mouse_pos) and button.callback:
                    button.callback()
                    self._generate_map_surface()  # Regenera mapa amb nou mode
                    return True

            # Click en mapa - selecciona tile
            if mouse_pos[1] > 80:  # Sota la barra de botons
                map_x = (mouse_pos[0] + self.camera_x) // self.tile_size
                map_y = (mouse_pos[1] - 80 + self.camera_y) // self.tile_size

                if self.world and 0 <= map_x < self.world.width and 0 <= map_y < self.world.height:
                    self.selected_tile = (map_x, map_y)
                    self.update_info_panel(map_x, map_y)

        elif event.type == pygame.KEYDOWN:
            # Controls de càmera
            move_speed = 50

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.camera_x = max(0, self.camera_x - move_speed)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.camera_x = min(self.world.width * self.tile_size - self.screen_width,
                                   self.camera_x + move_speed)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.camera_y = max(0, self.camera_y - move_speed)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.camera_y = min(self.world.height * self.tile_size - (self.screen_height - 100),
                                   self.camera_y + move_speed)

            # Controls de temps
            elif event.key == pygame.K_SPACE:
                self.toggle_play()
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.advance_years(10)
            elif event.key == pygame.K_MINUS:
                self.current_year = max(0, self.current_year - 10)

            # Canvi de mode amb números
            elif event.key == pygame.K_1:
                self.set_view_mode(ViewMode.TERRAIN)
                self._generate_map_surface()
            elif event.key == pygame.K_2:
                self.set_view_mode(ViewMode.BIOMES)
                self._generate_map_surface()
            elif event.key == pygame.K_3:
                self.set_view_mode(ViewMode.CIVILIZATIONS)
                self._generate_map_surface()
            elif event.key == pygame.K_4:
                self.set_view_mode(ViewMode.TECTONICS)
                self._generate_map_surface()
            elif event.key == pygame.K_5:
                self.set_view_mode(ViewMode.CLIMATE)
                self._generate_map_surface()

        return True

    def run(self, max_fps: int = 60):
        """
        Executa el bucle principal de la UI

        Args:
            max_fps: FPS màxims
        """
        clock = pygame.time.Clock()
        running = True

        print("🖥️  UI iniciada")
        print("Controls:")
        print("  - Click: Selecciona tile")
        print("  - WASD/Fletxes: Mou càmera")
        print("  - Espai: Play/Pause")
        print("  - +/-: Avança/retrocedeix temps")
        print("  - 1-5: Canvia mode visualització")
        print("  - ESC: Surt")

        while running:
            for event in pygame.event.get():
                if not self.handle_event(event):
                    running = False
                    break

            # Actualitza simulació si està reproduint
            if self.is_playing:
                self.current_year += 1

            # Dibuixa
            self.draw()

            clock.tick(max_fps)

        pygame.quit()
        print("👋 UI tancada")
