from game_constants import *
from sound import *


class PlayerData:
    def __init__(self):
        self.rect = pygame.Rect((1, 1, 12, 20))
        self.ghosted = False


class WorldData:
    def __init__(self):
        self.level_data = []
        self.text_list = []
        self.objects = []
        self.screen_fade_out = False


class Object:
    def __init__(self, x=0, y=0, width=100, height=100, color=color_gray, solid=True):
        self.color = color
        self.solid = solid
        self.rect = pygame.Rect((x, y, width, height))
        self.rect_core = pygame.Rect((x + 3, y + 3, width - 6, height - 6))

    def draw(self):
        pygame.draw.rect(screen, color_black, self.rect)
        pygame.draw.rect(screen, self.color, self.rect_core)


class ButtonObject(Object):
    def __init__(self, x=0, y=0, width=100, height=100,
                 activates_once=True, subject=None, ghost_button=False):
        self.ghost_button = ghost_button
        self.activates_once = activates_once
        self.activated = False
        self.subject = subject
        if ghost_button:
            self.color = color_light_blue
            self.active_color = color_blue
        else:
            self.color = color_green
            self.active_color = color_red
        super().__init__(x, y, width, height, self.color, False)

    def activate(self):
        sound_system.button_click_sound.play()
        if self.subject:
            if type(self.subject) in (tuple, list):
                for subject in self.subject:
                    self.activate_subject(subject)
            else:
                self.activate_subject(self.subject)

    def on_press(self):
        if player_data.ghosted == self.ghost_button:
            if self.activates_once and not self.activated:
                self.activated = True
                self.activate()
            else:
                self.activated = not self.activated
                self.activate()

    def activate_subject(self, subject):
        if type(subject) is ButtonSubject:
            subject.solidity_switch()
        elif isinstance(subject, TriggerObject):
            subject.activate()

    def draw(self):
        pygame.draw.rect(screen, color_black, self.rect)
        if not self.activated:
            pygame.draw.rect(screen, self.color, self.rect_core)
        else:
            pygame.draw.rect(screen, self.active_color, self.rect_core)


class PlayButton(ButtonObject):
    def __init__(self, x=0, y=0, width=100, height=100):
        super().__init__(x, y, width, height, False, None, False)
        self.color = color_gray
        self.pressed = False

    def on_press(self):
        self.pressed = True


class OptionsButton(ButtonObject):
    def __init__(self, x=0, y=0, width=100, height=100):
        super().__init__(x, y, width, height, False, None, False)
        self.color = color_gray
        self.pressed = False

    def on_press(self):
        self.pressed = True


class ExitButton(ButtonObject):
    def __init__(self, x=0, y=0, width=100, height=100):
        super().__init__(x, y, width, height, False, None, False)
        self.color = color_gray
        self.pressed = False

    def on_press(self):
        self.pressed = True


class ButtonSubject(Object):
    def __init__(self, x=0, y=0, width=100, height=100, color=color_light_gray, unsolid_color=color_subject_gray,
                 solid=True):
        super().__init__(x, y, width, height, color, solid)
        self.unsolid_color = unsolid_color

    def solidity_switch(self):
        self.solid = not self.solid

    def draw(self):
        pygame.draw.rect(screen, color_black, self.rect)
        if self.solid:
            pygame.draw.rect(screen, self.color, self.rect_core)
        else:
            pygame.draw.rect(screen, self.unsolid_color, self.rect_core)



class ObjectTextured(Object):
    def __init__(self, image, x=0, y=0, width=100, height=100, solid=True):
        super().__init__(x, y, width, height, solid)
        self.image = image
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, self.rect)


class PlayerBody(ObjectTextured):
    def __init__(self):
        super().__init__(cursor_img_body, width=10, height=14, solid=False)


class TriggerObject(Object):
    def __init__(self, x=0, y=0, width=100, height=100, color=color_gray, cooldown=1,
                 activates_once=True, active=True, subject=None):
        self.cooldown = cooldown
        self.cooldown_timer = pygame.time.get_ticks()
        self.activates_once = activates_once
        self.activated = False
        self.active = active
        self.subject = subject
        super().__init__(x, y, width, height, color, False)

    def activate(self):
        self.active = not self.active

    def on_activate(self):
        if self.activates_once and not self.activated:
            self.activated = True
            self.activate_subject(self.subject)
        elif not self.activates_once:
            now = pygame.time.get_ticks()
            if now - self.cooldown_timer >= self.cooldown * fps * 20:
                self.activate_subject(self.subject)
                self.cooldown_timer = now

    def activate_subject(self, subjects):
        if subjects:
            if type(subjects) in (tuple, list):
                for subject in subjects:
                    if type(subject) is ButtonSubject:
                        subject.solidity_switch()
                    elif isinstance(subject, TriggerObject):
                        subject.activate()
            else:
                if type(subjects) is ButtonSubject:
                    subjects.solidity_switch()
                elif isinstance(subjects, TriggerObject):
                    subjects.activate()


class VoidObject(TriggerObject):
    def __init__(self, x=0, y=0, width=100, height=100, active=True, color=color_black, inactive_color=color_gray):
        self.inactive_color = inactive_color
        super().__init__(x, y, width, height, color, active=active)

    def draw(self):
        pygame.draw.rect(screen, color_black, self.rect)
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect_core)
        else:
            pygame.draw.rect(screen, self.inactive_color, self.rect_core)


class LevelEndTrigger(TriggerObject):
    def __init__(self, x=0, y=0, width=100, height=100, color=color_dark_green, solid=False):
        super().__init__(x, y, width, height, color, solid)


class LevelEndFadeOutTrigger(LevelEndTrigger):
    def __init__(self, x=0, y=0, width=100, height=100, color=color_dark_green, solid=False):
        super().__init__(x, y, width, height, color, solid)


class GhostKillerObject(VoidObject):
    def __init__(self, x=0, y=0, width=100, height=100, active=True, color=color_dark_blue, inactive_color=color_cyan):
        self.color = color_dark_blue
        self.inactive_color = color_cyan
        super().__init__(x, y, width, height, active, color, inactive_color)


class BodyKillerObject(VoidObject):
    def __init__(self, x=0, y=0, width=100, height=100, active=True, color=color_red, inactive_color=color_light_pink):
        self.color = color_red
        self.inactive_color = color_light_pink
        super().__init__(x, y, width, height, active, color, inactive_color)


class TutorialText:
    def __init__(self, x, y, text='Test', color=color_black):
        self.rendered_text = None
        self.rendered_text_rect = None
        self.text = text
        self.x, self.y = x, y
        self.color = color

    def draw(self):
        screen.blit(self.rendered_text, self.rendered_text_rect)

    def render(self):
        self.rendered_text = font.render(self.text, True, self.color)
        self.rendered_text_rect = self.rendered_text.get_rect()
        self.rendered_text_rect.x, self.rendered_text_rect.y = self.x, self.y


class BigPixelText(TutorialText):
    def __init__(self, x, y, text='Test', color=color_black):
        super().__init__(x, y, text, color)

    def render(self):
        self.rendered_text = font_pixel_big.render(self.text, True, self.color)
        self.rendered_text_rect = self.rendered_text.get_rect()
        self.rendered_text_rect.x, self.rendered_text_rect.y = self.x, self.y


class PixelText(TutorialText):
    def __init__(self, x, y, text='Test', color=color_black):
        super().__init__(x, y, text, color)

    def render(self):
        self.rendered_text = font_pixel.render(self.text, True, self.color)
        self.rendered_text_rect = self.rendered_text.get_rect()
        self.rendered_text_rect.x, self.rendered_text_rect.y = self.x, self.y


class TimedText(TutorialText):
    def __init__(self, x, y, text='Test', color=color_light_blue, timer=420):
        self.timer = timer
        super().__init__(x, y, text, color)


player_body = PlayerBody()
world_data = WorldData()
player_data = PlayerData()
