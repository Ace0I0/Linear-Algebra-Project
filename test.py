import pygame
import pytmx

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 16
MAP_WIDTH = 25
MAP_HEIGHT = 18
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576
GRAVITY = 0.2
JUMP_STRENGTH = -5
CHARACTER_SPEED = 3
FPS = 60

# Calculate the scale factor
scale_factor_x = SCREEN_WIDTH / (MAP_WIDTH * TILE_SIZE)
scale_factor_y = SCREEN_HEIGHT / (MAP_HEIGHT * TILE_SIZE)
scale_factor = min(scale_factor_x, scale_factor_y)

# Character size constants
DEFAULT_CHARACTER_SIZE = (int(16 * scale_factor), int(16 * scale_factor))
MAX_CHARACTER_SIZE = (int(64 * scale_factor), int(64 * scale_factor))
MIN_CHARACTER_SIZE = (int(8 * scale_factor), int(8 * scale_factor))

# Create a window to display the scaled tile map
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Load the tile map
tmx_data = pytmx.load_pygame('C:\\Users\\rafae\\PyGame\\Tile_Maps\\Test_Environment.tmx') # set to where ever you save this

# Load the character sprite
character_sprite = pygame.image.load('C:\\Users\\rafae\\PyGame\\Sprites\\Slime_1.png') # same with this thing
character_sprite = pygame.transform.scale(character_sprite, DEFAULT_CHARACTER_SIZE)

# Character properties
character_rect = character_sprite.get_rect()
character_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
character_velocity_y = 0
on_ground = False

# Function to draw the tile map
def draw_tile_map(screen, tmx_data, scale_factor):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    tile = pygame.transform.scale(tile, (int(TILE_SIZE * scale_factor), int(TILE_SIZE * scale_factor)))
                    screen.blit(tile, (x * TILE_SIZE * scale_factor, y * TILE_SIZE * scale_factor))

# Function to get solid tiles
def get_solid_tiles(tmx_data):
    solid_tiles = []
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    tile_properties = tmx_data.get_tile_properties_by_gid(gid)
                    if tile_properties and tile_properties.get('solid'):
                        tile_rect = pygame.Rect(x * TILE_SIZE * scale_factor, y * TILE_SIZE * scale_factor, TILE_SIZE * scale_factor, TILE_SIZE * scale_factor)
                        solid_tiles.append(tile_rect)
    return solid_tiles

# Create a clock object to manage the frame rate
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Move the character left or right
    if keys[pygame.K_a]:
        character_rect.x -= CHARACTER_SPEED
    if keys[pygame.K_d]:
        character_rect.x += CHARACTER_SPEED

    # Make the character jump
    if keys[pygame.K_SPACE] and on_ground:
        character_velocity_y = JUMP_STRENGTH
        on_ground = False

    # Increase character size
    if keys[pygame.K_w]:
        new_width = min(character_rect.width * 2, MAX_CHARACTER_SIZE[0])
        new_height = min(character_rect.height * 2, MAX_CHARACTER_SIZE[1])
        character_sprite = pygame.transform.scale(character_sprite, (new_width, new_height))
        character_rect = character_sprite.get_rect(center=character_rect.center)

    # Decrease character size
    if keys[pygame.K_s]:
        new_width = max(character_rect.width // 2, MIN_CHARACTER_SIZE[0])
        new_height = max(character_rect.height // 2, MIN_CHARACTER_SIZE[1])
        character_sprite = pygame.transform.scale(character_sprite, (new_width, new_height))
        character_rect = character_sprite.get_rect(center=character_rect.center)

    # Reset character size to default
    if keys[pygame.K_r]:
        character_sprite = pygame.transform.scale(character_sprite, DEFAULT_CHARACTER_SIZE)
        character_rect = character_sprite.get_rect(center=character_rect.center)

    # apply gravity
    character_velocity_y += GRAVITY
    character_rect.y += character_velocity_y

    # get solid tiles
    solid_tiles = get_solid_tiles(tmx_data)

    # check for collisions with solid tiles
    on_ground = False
    for tile_rect in solid_tiles:
        if character_rect.colliderect(tile_rect):
            if character_velocity_y > 0:  # Falling
                character_rect.bottom = tile_rect.top
                character_velocity_y = 0
                on_ground = True
            elif character_velocity_y < 0:  # Jumping
                character_rect.top = tile_rect.bottom
                character_velocity_y = 0

    # prevent the character from leaving the screen borders
    if character_rect.left < 0:
        character_rect.left = 0
    if character_rect.right > SCREEN_WIDTH:
        character_rect.right = SCREEN_WIDTH
    if character_rect.top < 0:
        character_rect.top = 0
        character_velocity_y = 0
    if character_rect.bottom > SCREEN_HEIGHT:
        character_rect.bottom = SCREEN_HEIGHT
        character_velocity_y = 0
        on_ground = True

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the scaled tile map
    draw_tile_map(screen, tmx_data, scale_factor)

    # Draw the character
    screen.blit(character_sprite, character_rect.topleft)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()