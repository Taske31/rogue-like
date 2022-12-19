import pygame
import sys
import os

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    #size = width, height = 500, 500
    #screen = pygame.display.set_mode(size)
    size = width, height = window.get_size()
    walls = pygame.sprite.Group()
    heroes = pygame.sprite.Group()
    settings = pygame.sprite.Group()
    window.fill((255, 255, 255))
    font = pygame.font.Font(None, 75)

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


    class Settings(pygame.sprite.Sprite):
        image = load_image("settings.png")

        def __init__(self):
            super().__init__(settings)
            self.image = Settings.image
            self.image_size = self.image.get_size()
            self.rect = self.image.get_rect()
            self.rect.x = width - 60
            self.rect.y = 30

        def update(self, *args):
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                    self.rect.collidepoint(args[0].pos):
                self.open_settings()

        def open_settings(self):
            global run

            settings_screen_size = settings_screen_width, settings_screen_height = width // 2, height // 2
            settings_screen = pygame.Surface((settings_screen_width, settings_screen_height))
            text = font.render("Настройки", True, (255, 255, 255))
            cross = font.render('X', True, (255, 255, 255))
            cross_rect = cross.get_rect()
            settings_sprites = pygame.sprite.Group()
            settings_run = True
            while settings_run:
                window.blit(settings_screen, (width // 4, height // 4))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        settings_run = False
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(event.pos)
                        print(cross_rect)
                        if cross_rect.collidepoint(event.pos):
                            print(1)
                            settings_run = False

                settings_screen.blit(cross, [settings_screen_width - 60, 20])
                settings_screen.blit(text, [settings_screen_width // 3, 20])
                pygame.display.flip()


    s = Settings()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            settings.draw(window)
            settings.update(event)
            pygame.display.flip()
        window.fill((255, 255, 255))

    pygame.quit()
