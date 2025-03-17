import pygame
import pytmx
from menu import *
from game_functions import *

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 576
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = 'Linear-Algebra-Project\\Extra_Assests\\04B_30__.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        # Game-specific initialization
        self.TILE_SIZE = 16
        self.MAP_WIDTH = 25
        self.MAP_HEIGHT = 18
        self.GRAVITY = 0.2
        self.JUMP_STRENGTH = -5
        self.CHARACTER_SPEED = 3
        self.FPS = 60

        self.scale_factor_x = self.DISPLAY_W / (self.MAP_WIDTH * self.TILE_SIZE)
        self.scale_factor_y = self.DISPLAY_H / (self.MAP_HEIGHT * self.TILE_SIZE)
        self.scale_factor = min(self.scale_factor_x, self.scale_factor_y)

        self.DEFAULT_CHARACTER_SIZE = (int(16 * self.scale_factor), int(16 * self.scale_factor))
        self.MAX_CHARACTER_SIZE = (int(64 * self.scale_factor), int(64 * self.scale_factor))
        self.MIN_CHARACTER_SIZE = (int(8 * self.scale_factor), int(8 * self.scale_factor))

        self.screen = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.RESIZABLE)
        self.tmx_data = pytmx.load_pygame('Linear-Algebra-Project\\Tile_Maps\\Test_Environment.tmx')
        self.character_sprite = pygame.image.load('Linear-Algebra-Project\\Sprites\\Slime_1.png')
        self.character_sprite = pygame.transform.scale(self.character_sprite, self.DEFAULT_CHARACTER_SIZE)

        self.character_rect = self.character_sprite.get_rect()
        self.character_rect.center = (self.DISPLAY_W // 2, self.DISPLAY_H // 2)
        self.character_velocity_y = 0
        self.on_ground = False

        self.clock = pygame.time.Clock()

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.character_rect.x -= self.CHARACTER_SPEED
            if keys[pygame.K_d]:
                self.character_rect.x += self.CHARACTER_SPEED
            if keys[pygame.K_SPACE] and self.on_ground:
                self.character_velocity_y = self.JUMP_STRENGTH
                self.on_ground = False
            if keys[pygame.K_w]:
                new_width = min(self.character_rect.width * 2, self.MAX_CHARACTER_SIZE[0])
                new_height = min(self.character_rect.height * 2, self.MAX_CHARACTER_SIZE[1])
                self.character_sprite = pygame.transform.scale(self.character_sprite, (new_width, new_height))
                self.character_rect = self.character_sprite.get_rect(center=self.character_rect.center)
            if keys[pygame.K_s]:
                new_width = max(self.character_rect.width // 2, self.MIN_CHARACTER_SIZE[0])
                new_height = max(self.character_rect.height // 2, self.MIN_CHARACTER_SIZE[1])
                self.character_sprite = pygame.transform.scale(self.character_sprite, (new_width, new_height))
                self.character_rect = self.character_sprite.get_rect(center=self.character_rect.center)
            if keys[pygame.K_r]:
                self.character_sprite = pygame.transform.scale(self.character_sprite, self.DEFAULT_CHARACTER_SIZE)
                self.character_rect = self.character_sprite.get_rect(center=self.character_rect.center)

            self.character_velocity_y += self.GRAVITY
            self.character_rect.y += self.character_velocity_y

            solid_tiles = get_solid_tiles(self.tmx_data, self.TILE_SIZE, self.scale_factor)
            self.on_ground = False
            for tile_rect in solid_tiles:
                if self.character_rect.colliderect(tile_rect):
                    if self.character_velocity_y > 0:
                        self.character_rect.bottom = tile_rect.top
                        self.character_velocity_y = 0
                        self.on_ground = True
                    elif self.character_velocity_y < 0:
                        self.character_rect.top = tile_rect.bottom
                        self.character_velocity_y = 0

            if self.character_rect.left < 0:
                self.character_rect.left = 0
            if self.character_rect.right > self.DISPLAY_W:
                self.character_rect.right = self.DISPLAY_W
            if self.character_rect.top < 0:
                self.character_rect.top = 0
                self.character_velocity_y = 0
            if self.character_rect.bottom > self.DISPLAY_H:
                self.character_rect.bottom = self.DISPLAY_H
                self.character_velocity_y = 0
                self.on_ground = True

            self.screen.fill((0, 0, 0))
            draw_tile_map(self.screen, self.tmx_data, self.scale_factor, self.TILE_SIZE)
            self.screen.blit(self.character_sprite, self.character_rect.topleft)
            pygame.display.flip()
            self.clock.tick(self.FPS)

            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)