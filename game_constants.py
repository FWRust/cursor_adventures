import pygame

pygame.init()

fps = 60
size = (1600, 900)
debug_mode = False

font = pygame.font.Font(None, 32)
font_pixel_big = pygame.font.Font('fonts/prstart.ttf', 60)
font_pixel = pygame.font.Font(None, 70)

pygame.display.set_caption("Mouse game")

color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_light_blue = (173, 216, 230)
color_blue = (0, 0, 255)
color_dark_blue = (0, 0, 139)
color_cyan = (64, 224, 208)
color_gray = (128, 128, 128)
color_light_gray = (83, 83, 83)
color_very_light_gray = (200, 200, 200)
color_black = (0, 0, 0)
color_yellow = (255, 255, 0)
color_dark_green = (0, 100, 0)
color_bg = (220, 220, 220)
color_subject_gray = (230, 231, 232)
color_light_pink = (255, 182, 193)

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("Mouse game")
pygame.display.set_icon(pygame.image.load('sprites/cursor_icon.png'))

screen = pygame.display.set_mode(size)
invisible_surface = pygame.Surface(size)
invisible_surface.set_alpha(128)

fade_out_surface = pygame.Surface(size, pygame.SRCALPHA)
fade_out_surface.set_alpha(0)

cursor_ghost_img = pygame.image.load('sprites/cursor_ghost.png')
cursor_ghost_img_rect = cursor_ghost_img.get_rect()
cursor_img = pygame.image.load('sprites/cursor.png')
cursor_img_body = pygame.image.load('sprites/cursor.png')
cursor_img_rect = cursor_img.get_rect()

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

native_cursor_levels = (0, 8, 9)
