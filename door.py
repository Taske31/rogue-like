import pygame
import sys
import os
import hero

door_group = pygame.sprite.Group()


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


class Door(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(door_group)
        name = 'door'
        self.frames = []
        self.sheet = load_image(f'{name}.png')
        self.x = pos[0]
        self.y = pos[1]

    def cut_sheet(self, sheet, columns, rows, frame):
        self.rect = pygame.Rect(500, 500, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def spawn_door(self):
        self.cut_sheet(self.sheet, 1, 1, self.frames)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def new_level(self):
        if pygame.sprite.spritecollideany(self, hero.hero_group):
            return True
