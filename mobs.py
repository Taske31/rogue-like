import pygame
import sys
import os
import hero
import main

pygame.init()
window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
size = width, height = window.get_size()
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
mobs_group = pygame.sprite.Group()
count_of_mobs = 2


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


class Mob(pygame.sprite.Sprite):
    def __init__(self, name, damage, health, pos):
        super().__init__(mobs_group)
        self.name = name
        self.health = damage
        self.damage = health
        self.condition = 'calm'

        self.cur_frame = 0
        self.frames_stay = []
        self.sheet = load_image(f'{name}.png')
        self.cut_sheet(self.sheet, 4, 1, self.frames_stay)

        self.frames_run = []
        self.sheet_run = load_image(f'{name}-run.png')
        self.cut_sheet(self.sheet_run, 6, 1, self.frames_run)

        #self.frames_attack = []
        #self.sheet_attack = load_image(f'{name}-attack.png')
        #self.cut_sheet(self.sheet_attack, 6, 1, self.frames_attack)

        self.image = self.frames_stay[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def cut_sheet(self, sheet, columns, rows, frame):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def animation(self, hero_pos):
        if self.condition == 'calm':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_stay)
            self.image = self.frames_stay[self.cur_frame]
        if self.condition == 'angry':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_run)
            self.image = self.frames_run[self.cur_frame]
            self.chase(hero_pos)
        # if self.condition == 'attack':
        #     self.cur_frame = (self.cur_frame + 1) % len(self.frames_attack)
        #     self.image = self.frames_attack[self.cur_frame]

    def get_damage(self, damage):
        if pygame.sprite.spritecollideany(self, hero.hero_group):
            self.health -= damage
            self.image.fill((255, 255, 255))
            self.condition = 'angry'
        if self.health <= 0:
            self.death()

    def death(self):
        pass

    def chase(self, hero_pos):
        pass
       # while not pygame.sprite.spritecollideany(self, main.hero_group):
       #     if self.rect.x < main.hero.rect[0]