import pygame
import pytmx

def draw_tile_map(screen, tmx_data, scale_factor, TILE_SIZE):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    tile = pygame.transform.scale(tile, (int(TILE_SIZE * scale_factor), int(TILE_SIZE * scale_factor)))
                    screen.blit(tile, (x * TILE_SIZE * scale_factor, y * TILE_SIZE * scale_factor))

def get_solid_tiles(tmx_data, TILE_SIZE, scale_factor):
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