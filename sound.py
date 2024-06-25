import pygame.mixer


class SoundSystem:
    def __init__(self):
        pygame.mixer.music.set_volume(0.2)
        self.in_out = False

        self.body_enter_sound = pygame.mixer.Sound('sounds/body_entered.ogg')
        self.body_left_sound = pygame.mixer.Sound('sounds/body_left.ogg')
        self.level_end_sound = pygame.mixer.Sound('sounds/level_end.ogg')
        self.death_sound = pygame.mixer.Sound('sounds/death.ogg')
        self.voice1 = pygame.mixer.Sound('sounds/voice1.ogg')
        self.voice2 = pygame.mixer.Sound('sounds/voice2.ogg')
        self.win_sound = pygame.mixer.Sound('sounds/win.ogg')
        self.in_sound = pygame.mixer.Sound('sounds/in.ogg')
        self.out_sound = pygame.mixer.Sound('sounds/out.ogg')
        self.button_click_sound = pygame.mixer.Sound('sounds/button_click.ogg')

        self.main_menu_music_path = 'sounds/main_menu_theme.ogg'
        self.music1_path = 'sounds/music1.ogg'
        self.sad_music_path = 'sounds/sad_music.wav'

        pygame.mixer.music.load(self.main_menu_music_path)
        pygame.mixer.music.play(-1)

    def play_music(self, level_num):
        music = None
        if level_num == 1:
            music = self.music1_path
        elif level_num == 8:
            pygame.mixer.music.set_volume(0.8)
            music = self.sad_music_path
        elif level_num == 9:
            pygame.mixer.music.stop()
            sound_system.win_sound.play()

        if music:
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)

    def play_portal(self, gain):
        if gain:
            sound_system.in_sound.play()
        else:
            sound_system.out_sound.play()


class VoiceOverSystem:
    def __init__(self):
        self.voice = 1

    def voice_over(self):
        if self.voice % 2 == 0:
            sound_system.voice1.play()
        else:
            sound_system.voice2.play()
        self.voice += 1


sound_system = SoundSystem()
voice_over_system = VoiceOverSystem()
