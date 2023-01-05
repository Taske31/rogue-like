import pygame
import sys
import os

pygame.init()
window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
size = width, height = window.get_size()
settings_sprites = pygame.sprite.Group()
window.fill((255, 255, 255))
font = pygame.font.Font(None, 75)
settings_screen_size = settings_screen_width, settings_screen_height = width // 2, height // 1.5
settings_run = False


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def open_settings():
    global settings_run
    settings_screen = pygame.Surface((settings_screen_width, settings_screen_height))
    settings_screen.fill((67, 67, 69))
    text = font.render("Настройки", True, (255, 255, 255))
    settings_run = True
    exit_btn = Exit()
    continue_btn = Continue()
    while settings_run:
        window.blit(settings_screen, (width // 4, height // 4))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings_run = False
            settings_screen.blit(text, [settings_screen_width // 3, 20])
            settings_sprites.draw(settings_screen)
            settings_sprites.update(event)
            pygame.display.flip()


class Exit(pygame.sprite.Sprite):
    image = load_image('exit.png', -1)

    def __init__(self):
        super().__init__(settings_sprites)
        self.image = Exit.image
        self.rect = self.image.get_rect()
        self.rect.x = settings_screen_width // 5 - 40
        self.rect.y = settings_screen_height // 2

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            scaled_pos = (args[0].pos[0] - width // 4, args[0].pos[1] - height // 4)
            if self.rect.collidepoint(scaled_pos):
                terminate()


class Continue(pygame.sprite.Sprite):
    image = load_image('continue.png', -1)

    def __init__(self):
        super().__init__(settings_sprites)
        self.image = Continue.image
        self.rect = self.image.get_rect()
        self.rect.x = settings_screen_width // 5 - 40
        self.rect.y = settings_screen_height // 10

    def update(self, *args):
        global settings_run 
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            scaled_pos = (args[0].pos[0] - width // 4, args[0].pos[1] - height // 4)
            if self.rect.collidepoint(scaled_pos):
                settings_run = False


