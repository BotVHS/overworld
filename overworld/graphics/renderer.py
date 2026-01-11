"""
Renderer - Sistema de renderització amb pygame

Renderitza el món i proporciona interacció bàsica
"""
import pygame
from typing import Optional, Tuple, List
from enum import Enum
from ..world.world import World
from ..world.biome import BIOME_DEFINITIONS
from ..core.time_manager import TimeManager


class RenderLayer(Enum):
    """Capes de visualització disponibles"""
    BIOMES = "biomes"
    ALTITUDE = "altitude"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    FERTILITY = "fertility"
    HOSTILITY = "hostility"
    RESOURCES_WOOD = "resources_wood"
    RESOURCES_WATER = "resources_water"
    RESOURCES_MINERALS = "resources_minerals"


class WorldRenderer:
    """Renderitzador del món amb pygame"""

    def __init__(
        self,
        world: World,
        time_manager: Optional[TimeManager] = None,
        screen_width: int = 1280,
        screen_height: int = 720,
        tile_size: int = 4
    ):
        """
        Args:
            world: Món a renderitzar
            time_manager: Gestor de temps (opcional)
            screen_width: Amplada de la finestra
            screen_height: Alçada de la finestra
            tile_size: Mida de cada tile en píxels
        """
        self.world = world
        self.time_manager = time_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = tile_size

        # Inicialitza pygame
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Overworld - Simulació Procedural")

        # Font per text
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)

        # Càmera (offset i zoom)
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0

        # Capa actual
        self.current_layer = RenderLayer.BIOMES

        # Tile seleccionat
        self.selected_tile: Optional[Tuple[int, int]] = None

        # Colors UI
        self.ui_bg_color = (30, 30, 40, 200)
        self.ui_text_color = (220, 220, 220)
        self.ui_highlight_color = (100, 150, 255)

        # Superfície per al mapa (cache)
        self.map_surface: Optional[pygame.Surface] = None
        self.needs_redraw = True

    def handle_events(self) -> bool:
        """
        Gestiona esdeveniments de pygame

        Returns:
            False si cal tancar la finestra, True altrament
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                # Canvi de capa
                if event.key == pygame.K_1:
                    self.current_layer = RenderLayer.BIOMES
                    self.needs_redraw = True
                elif event.key == pygame.K_2:
                    self.current_layer = RenderLayer.ALTITUDE
                    self.needs_redraw = True
                elif event.key == pygame.K_3:
                    self.current_layer = RenderLayer.TEMPERATURE
                    self.needs_redraw = True
                elif event.key == pygame.K_4:
                    self.current_layer = RenderLayer.HUMIDITY
                    self.needs_redraw = True
                elif event.key == pygame.K_5:
                    self.current_layer = RenderLayer.FERTILITY
                    self.needs_redraw = True
                elif event.key == pygame.K_6:
                    self.current_layer = RenderLayer.HOSTILITY
                    self.needs_redraw = True
                elif event.key == pygame.K_7:
                    self.current_layer = RenderLayer.RESOURCES_MINERALS
                    self.needs_redraw = True

                # Moviment de càmera
                elif event.key == pygame.K_LEFT:
                    self.camera_x -= 50
                elif event.key == pygame.K_RIGHT:
                    self.camera_x += 50
                elif event.key == pygame.K_UP:
                    self.camera_y -= 50
                elif event.key == pygame.K_DOWN:
                    self.camera_y += 50

                # Zoom
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.zoom = min(self.zoom * 1.2, 10.0)
                    self.needs_redraw = True
                elif event.key == pygame.K_MINUS:
                    self.zoom = max(self.zoom / 1.2, 0.1)
                    self.needs_redraw = True

                # Reset càmera
                elif event.key == pygame.K_HOME:
                    self.camera_x = 0
                    self.camera_y = 0
                    self.zoom = 1.0
                    self.needs_redraw = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click esquerre
                    # Converteix posició del ratolí a tile
                    mouse_x, mouse_y = event.pos
                    tile_x, tile_y = self.screen_to_tile(mouse_x, mouse_y)
                    if 0 <= tile_x < self.world.width and 0 <= tile_y < self.world.height:
                        self.selected_tile = (tile_x, tile_y)

                elif event.button == 4:  # Roda amunt (zoom in)
                    self.zoom = min(self.zoom * 1.1, 10.0)
                    self.needs_redraw = True
                elif event.button == 5:  # Roda avall (zoom out)
                    self.zoom = max(self.zoom / 1.1, 0.1)
                    self.needs_redraw = True

        # Moviment continu amb tecles premudes
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.camera_x -= 5
        if keys[pygame.K_d]:
            self.camera_x += 5
        if keys[pygame.K_w]:
            self.camera_y -= 5
        if keys[pygame.K_s]:
            self.camera_y += 5

        return True

    def screen_to_tile(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Converteix coordenades de pantalla a coordenades de tile"""
        tile_size_zoomed = int(self.tile_size * self.zoom)
        tile_x = int((screen_x + self.camera_x) / tile_size_zoomed)
        tile_y = int((screen_y + self.camera_y) / tile_size_zoomed)
        return tile_x, tile_y

    def tile_to_screen(self, tile_x: int, tile_y: int) -> Tuple[int, int]:
        """Converteix coordenades de tile a coordenades de pantalla"""
        tile_size_zoomed = int(self.tile_size * self.zoom)
        screen_x = tile_x * tile_size_zoomed - self.camera_x
        screen_y = tile_y * tile_size_zoomed - self.camera_y
        return screen_x, screen_y

    def get_tile_color(self, tile_x: int, tile_y: int) -> Tuple[int, int, int]:
        """Obté el color d'un tile segons la capa actual"""
        tile = self.world.get_tile(tile_x, tile_y)

        if self.current_layer == RenderLayer.BIOMES:
            if tile.biome:
                return BIOME_DEFINITIONS[tile.biome].color
            return (100, 100, 100)

        elif self.current_layer == RenderLayer.ALTITUDE:
            value = tile.altitude
            if tile.is_water:
                # Tons de blau segons profunditat
                intensity = int(value * 255)
                return (0, intensity // 2, 100 + intensity // 2)
            else:
                # Gradient de verd a marró a blanc
                if value < 0.6:
                    intensity = int((value - 0.35) / 0.25 * 255)
                    return (intensity // 2, 100 + intensity // 2, intensity // 4)
                elif value < 0.8:
                    intensity = int((value - 0.6) / 0.2 * 255)
                    return (100 + intensity // 2, 80 + intensity // 3, 60)
                else:
                    intensity = int((value - 0.8) / 0.2 * 255)
                    return (200 + intensity // 4, 200 + intensity // 4, 200 + intensity // 4)

        elif self.current_layer == RenderLayer.TEMPERATURE:
            value = tile.temperature
            # Blau (fred) a vermell (càlid)
            if value < 0.5:
                blue = int((0.5 - value) * 2 * 255)
                red = int(value * 2 * 100)
                return (red, 50, blue)
            else:
                red = int((value - 0.5) * 2 * 255)
                green = int((1.0 - value) * 2 * 100)
                return (100 + red, green, 0)

        elif self.current_layer == RenderLayer.HUMIDITY:
            value = tile.humidity
            # Marró (sec) a blau (humit)
            if value < 0.5:
                brown = int((0.5 - value) * 2 * 200)
                blue = int(value * 2 * 100)
                return (100 + brown, 80 + brown // 2, blue)
            else:
                green = int((value - 0.5) * 2 * 150)
                blue = int(value * 255)
                return (0, green, blue)

        elif self.current_layer == RenderLayer.FERTILITY:
            value = tile.fertility_index / 10.0
            # Vermell (infèrtil) a verd (fèrtil)
            if value < 0.5:
                red = int((0.5 - value) * 2 * 255)
                green = int(value * 2 * 150)
                return (red, green, 0)
            else:
                green = int(150 + (value - 0.5) * 2 * 105)
                return (0, green, 0)

        elif self.current_layer == RenderLayer.HOSTILITY:
            value = tile.hostility / 10.0
            # Verd (segur) a vermell (hostil)
            if value < 0.5:
                green = int((0.5 - value) * 2 * 255)
                red = int(value * 2 * 100)
                return (red, green, 0)
            else:
                red = int(100 + (value - 0.5) * 2 * 155)
                return (red, 0, 0)

        elif self.current_layer == RenderLayer.RESOURCES_MINERALS:
            # Mostra dipòsits minerals
            if tile.resources["gold"] > 0:
                return (255, 215, 0)  # Or
            elif tile.resources["silver"] > 0:
                return (192, 192, 192)  # Plata
            elif tile.resources["iron"] > 0:
                return (139, 69, 19)  # Ferro (marró)
            elif tile.resources["copper"] > 0:
                return (184, 115, 51)  # Coure
            elif tile.resources["uranium"] > 0:
                return (0, 255, 0)  # Urani (verd)
            elif tile.resources["coal"] > 0:
                return (50, 50, 50)  # Carbó
            elif tile.resources["oil"] > 0:
                return (0, 0, 0)  # Petroli
            elif tile.resources["gems"] > 0:
                return (255, 0, 255)  # Gemmes (magenta)
            else:
                # Sense recursos
                if tile.biome:
                    color = BIOME_DEFINITIONS[tile.biome].color
                    return (color[0] // 3, color[1] // 3, color[2] // 3)
                return (40, 40, 40)

        return (100, 100, 100)

    def render_map(self):
        """Renderitza el mapa complet"""
        if not self.needs_redraw and self.map_surface:
            return

        tile_size_zoomed = int(self.tile_size * self.zoom)

        # Crea superfície per al mapa
        map_width = self.world.width * tile_size_zoomed
        map_height = self.world.height * tile_size_zoomed
        self.map_surface = pygame.Surface((map_width, map_height))

        # Renderitza cada tile
        for y in range(self.world.height):
            for x in range(self.world.width):
                color = self.get_tile_color(x, y)
                rect = pygame.Rect(
                    x * tile_size_zoomed,
                    y * tile_size_zoomed,
                    tile_size_zoomed,
                    tile_size_zoomed
                )
                pygame.draw.rect(self.map_surface, color, rect)

        self.needs_redraw = False

    def render_ui(self):
        """Renderitza la interfície d'usuari"""
        # Panel superior (informació general)
        panel_height = 80
        panel_surface = pygame.Surface((self.screen_width, panel_height))
        panel_surface.set_alpha(200)
        panel_surface.fill((30, 30, 40))
        self.screen.blit(panel_surface, (0, 0))

        # Títol
        title_text = self.font_large.render("OVERWORLD", True, self.ui_highlight_color)
        self.screen.blit(title_text, (10, 10))

        # Informació de temps
        if self.time_manager:
            time_text = f"Any {self.time_manager.year}, Dia {self.time_manager.day} ({self.time_manager.get_season()})"
            time_surface = self.font_medium.render(time_text, True, self.ui_text_color)
            self.screen.blit(time_surface, (10, 45))

        # Capa actual
        layer_text = f"Capa: {self.current_layer.value.upper()}"
        layer_surface = self.font_medium.render(layer_text, True, self.ui_text_color)
        self.screen.blit(layer_surface, (self.screen_width - 300, 10))

        # Controls
        controls_text = "1-7: Capes | WASD/Fletxes: Mou | +/-: Zoom | Clic: Selecciona"
        controls_surface = self.font_small.render(controls_text, True, (150, 150, 150))
        self.screen.blit(controls_surface, (self.screen_width - 600, 45))

        # Panel lateral (tile seleccionat)
        if self.selected_tile:
            panel_width = 300
            panel_x = self.screen_width - panel_width
            panel_y = panel_height + 10

            tile_x, tile_y = self.selected_tile
            tile = self.world.get_tile(tile_x, tile_y)

            # Fons del panel
            panel_surface = pygame.Surface((panel_width, 500))
            panel_surface.set_alpha(220)
            panel_surface.fill((30, 30, 40))
            self.screen.blit(panel_surface, (panel_x, panel_y))

            y_offset = panel_y + 10

            # Títol
            title = self.font_medium.render(f"Tile ({tile_x}, {tile_y})", True, self.ui_highlight_color)
            self.screen.blit(title, (panel_x + 10, y_offset))
            y_offset += 30

            # Bioma
            if tile.biome:
                biome_name = BIOME_DEFINITIONS[tile.biome].name
                biome_text = self.font_small.render(f"Bioma: {biome_name}", True, self.ui_text_color)
                self.screen.blit(biome_text, (panel_x + 10, y_offset))
                y_offset += 25

            # Propietats
            props = [
                f"Altitud: {tile.altitude:.2f}",
                f"Temperatura: {tile.temperature:.2f}",
                f"Humitat: {tile.humidity:.2f}",
                f"Fertilitat: {tile.fertility_index:.1f}/10",
                f"Hostilitat: {tile.hostility:.1f}/10",
            ]

            for prop in props:
                prop_text = self.font_small.render(prop, True, self.ui_text_color)
                self.screen.blit(prop_text, (panel_x + 10, y_offset))
                y_offset += 22

            # Recursos
            y_offset += 10
            resources_title = self.font_small.render("Recursos:", True, self.ui_highlight_color)
            self.screen.blit(resources_title, (panel_x + 10, y_offset))
            y_offset += 22

            resources_to_show = [
                ("Fusta", "wood"),
                ("Aigua", "water"),
                ("Or", "gold"),
                ("Plata", "silver"),
                ("Ferro", "iron"),
                ("Coure", "copper"),
                ("Urani", "uranium"),
                ("Carbó", "coal"),
                ("Petroli", "oil"),
                ("Gas", "gas"),
                ("Gemmes", "gems"),
            ]

            for name, key in resources_to_show:
                value = tile.resources[key]
                if value > 0:
                    res_text = self.font_small.render(f"  {name}: {value:.0f}", True, self.ui_text_color)
                    self.screen.blit(res_text, (panel_x + 10, y_offset))
                    y_offset += 20

    def render(self):
        """Renderitza tot"""
        # Fons negre
        self.screen.fill((0, 0, 0))

        # Renderitza el mapa
        self.render_map()

        # Dibuixa el mapa amb offset de càmera
        if self.map_surface:
            self.screen.blit(self.map_surface, (-self.camera_x, -self.camera_y))

        # Marca el tile seleccionat
        if self.selected_tile:
            tile_x, tile_y = self.selected_tile
            screen_x, screen_y = self.tile_to_screen(tile_x, tile_y)
            tile_size_zoomed = int(self.tile_size * self.zoom)
            pygame.draw.rect(
                self.screen,
                (255, 255, 0),
                (screen_x, screen_y, tile_size_zoomed, tile_size_zoomed),
                2
            )

        # Renderitza UI
        self.render_ui()

        # Actualitza pantalla
        pygame.display.flip()

    def run(self, fps: int = 60):
        """
        Bucle principal de renderització

        Args:
            fps: Frames per segon
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            running = self.handle_events()
            self.render()
            clock.tick(fps)

        pygame.quit()
