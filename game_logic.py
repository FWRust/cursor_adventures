from entity_data import *
import pickle
import sys


class MenuHandler:
    def __init__(self):
        pass

    @staticmethod
    def handle():
        for object in world_data.objects:
            if type(object) is PlayButton:
                if object.pressed:
                    level_manager.next_level()
            if type(object) is OptionsButton:
                if object.pressed:
                    pass
            if type(object) is ExitButton:
                if object.pressed:
                    level_manager.exit_game()

        # elif world_data.objects[2].pressed:  # options button (wip)
        #     level_manager.load_level(99)


class PlayerHandler:

    @staticmethod
    def death():
        sound_system.death_sound.play()
        level_manager.restart_level()

    @staticmethod
    def update():
        player_movement_handler.update_pos()
        for text in world_data.text_list:
            if isinstance(text, TimedText):
                timed_text_handler.handle(text)

        colliding_object = collision_handler.check_player_collision()
        player_ghost_handler.update_body_ghost(colliding_object)


class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.native_cursor_level = False

    def load_level(self, level_num):
        self.current_level = level_num
        world_data.text_list = []
        with open(f'levels/level{level_num}_data.pkl', 'rb') as f:
            world_data.level_data = pickle.load(f)

        world_data.level_start_pos = world_data.level_data[0]
        pygame.mouse.set_pos(world_data.level_start_pos)

        world_data.objects = world_data.level_data[1]

        if world_data.level_data[2]:
            for text in world_data.level_data[2]:
                text.render()
                world_data.text_list.append(text)

        if self.current_level in native_cursor_levels:
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)
            self.native_cursor_level = True
        else:
            self.native_cursor_level = False
            pygame.event.set_grab(True)
            pygame.mouse.set_visible(False)

    def restart_level(self):
        player_data.ghosted = False
        self.load_level(self.current_level)

    def next_level(self):
        self.current_level += 1
        self.load_level(self.current_level)
        sound_system.play_music(self.current_level)

    @staticmethod
    def exit_game():
        sys.exit()


class ObjectInteractionHandler:
    def __init__(self):
        pass

    @staticmethod
    def handle(object):
        death_conditions = (type(object) is VoidObject,
                            (type(object) is GhostKillerObject) and player_data.ghosted,
                            (type(object) is BodyKillerObject) and not player_data.ghosted)
        if isinstance(object, TriggerObject):
            object.on_activate()
            if type(object) is LevelEndTrigger and not player_data.ghosted:
                level_manager.next_level()
                sound_system.level_end_sound.play()
            elif type(object) is LevelEndFadeOutTrigger and not player_data.ghosted:
                world_data.screen_fade_out = True
            elif any(death_conditions) and object.active:
                PlayerHandler.death()


class CollisionHandler:
    def __init__(self):
        pass

    @staticmethod
    def check_player_collision():
        for object in world_data.objects:
            player_x, player_y = player_data.rect.x, player_data.rect.y
            player_width, player_height = player_data.rect.width, player_data.rect.height
            if (player_x < object.rect.x + object.rect.width and
                    player_x + player_width > object.rect.x and
                    player_y < object.rect.y + object.rect.height and
                    player_y + player_height > object.rect.y):
                object_interaction_handler.handle(object)
                return object


class PlayerMovementHandler:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.velocity = 0

    def update_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        self.dx, self.dy = mouse_pos[0] - player_data.rect.x, mouse_pos[1] - player_data.rect.y
        self.velocity = ((player_data.rect.x - mouse_pos[0]) ** 2 + (player_data.rect.x - mouse_pos[0]) ** 2) ** 0.5
        player_data.rect.x, player_data.rect.y = mouse_pos


class PlayerBodyGhostHandler:
    def __init__(self):
        self.player_body = cursor_img.get_rect()
        self.player_body_enter_cooldown = 0

    def update_body_ghost(self, colliding_object):
        if colliding_object:
            if colliding_object.solid and not player_data.ghosted:
                self.enter_ghost()
            elif isinstance(colliding_object, PlayerBody) and player_data.ghosted:
                self.enter_body()

        if self.player_body_enter_cooldown > 0:
            self.player_body_enter_cooldown -= 1

    def enter_ghost(self):
        sound_system.body_left_sound.play()

        rect_x, rect_y = player_data.rect.x, player_data.rect.y
        dx, dy = player_movement_handler.dx, player_movement_handler.dy
        player_body.rect.topleft = (rect_x - dx, rect_y - dy)
        world_data.objects.append(player_body)

        player_data.ghosted = True
        self.player_body_enter_cooldown = fps * 0.6

    def enter_body(self):
        if self.player_body_enter_cooldown == 0:
            sound_system.body_enter_sound.play()
            world_data.objects.remove(player_body)
            player_data.ghosted = False


class DebugMethods:
    def __init__(self):
        pass

    @staticmethod
    def debug_show_velocity():
        velocity_text = font.render(f'Velocity: {player_movement_handler.velocity}', True, color_red)
        velocity_text_rect = velocity_text.get_rect()
        screen.blit(velocity_text, velocity_text_rect)


class TimedTextHandler:
    def __init__(self):
        self.timer = 0

    @staticmethod
    def handle(timed_text):
        if not timed_text.timer == 0:
            timed_text.timer -= 1
            if timed_text.timer == 0:
                voice_over_system.voice_over()


player_movement_handler = PlayerMovementHandler()
player_ghost_handler = PlayerBodyGhostHandler()
collision_handler = CollisionHandler()
object_interaction_handler = ObjectInteractionHandler()
level_manager = LevelManager()
timed_text_handler = TimedTextHandler()
