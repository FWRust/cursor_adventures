from game_constants import *
from entity_data import player_body, TimedText
from game_logic import world_data, DebugMethods, player_data, level_manager
import pygame.draw
import pygame.display


class GraphicsSystem:
    def __init__(self):
        self.fade_out_timer = 5 * fps

    @staticmethod
    def draw_game():
        screen.fill(color_bg)

        for object in world_data.objects:
            object.draw()
        for text in world_data.text_list:
            if isinstance(text, TimedText):
                if text.timer == 0:
                    text.draw()
            else:
                text.draw()

        if debug_mode:
            pygame.draw.rect(screen, color_red, player_data.rect)
            DebugMethods.debug_show_velocity()

        if player_data.ghosted:
            cursor_ghost_img_rect.topleft = pygame.mouse.get_pos()
            player_body.draw()
            if not level_manager.native_cursor_level:
                screen.blit(cursor_ghost_img, cursor_ghost_img_rect)
        else:
            cursor_img_rect.topleft = pygame.mouse.get_pos()
            if not level_manager.native_cursor_level:
                screen.blit(cursor_img, cursor_img_rect)

        if world_data.screen_fade_out:
            pygame.mixer.music.stop()
            graphics_system.fade_out()
            fade_out_surface.fill(color_white)
            screen.blit(fade_out_surface, (0, 0))

        pygame.display.flip()

    def fade_out(self):
        fade_out_surface.set_alpha(fade_out_surface.get_alpha() + 1)
        fade_out_surface.convert_alpha()
        if self.fade_out_timer > 0:
            self.fade_out_timer -= 1
        elif self.fade_out_timer == 0:
            self.fade_out_timer = 5 * fps
            level_manager.next_level()
            world_data.screen_fade_out = False


graphics_system = GraphicsSystem()
