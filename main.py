from game_logic import *
from graphics import *

# with open('levels/level8_data.pkl', 'wb') as f:
#      pickle.dump(level, f)

level_manager.load_level(0)
while True:
    for event in pygame.event.get():
        if event.type == pygame.ACTIVEEVENT:
            if level_manager.current_level == 8 and event.state == 2:
                sound_system.play_portal(event.gain)

        if event.type == pygame.QUIT:
            level_manager.exit_game()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                level_manager.exit_game()
            if debug_mode:
                if event.key == pygame.K_e:
                    player_data.ghosted = not player_data.ghosted
        if event.type == pygame.MOUSEBUTTONUP:
            collision_object = collision_handler.check_player_collision()
            if isinstance(collision_object, ButtonObject):
                collision_object.on_press()

    if level_manager.current_level in (0, 9):
        MenuHandler.handle()
    PlayerHandler.update()

    graphics_system.draw_game()

    clock.tick(fps)
