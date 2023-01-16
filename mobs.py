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


def load_image(name, colorkey=None):
    fullname = os.path.join('images/mobs', name)
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
        self.health = int(health)
        self.damage = int(damage)
        self.condition = 'calm'

        self.cur_frame = 0
        self.frames_stay = []
        self.sheet = load_image(f'{name}.png')
        self.cut_sheet(self.sheet, 4, 1, self.frames_stay)

        self.frames_run = []
        self.sheet_run = load_image(f'{name}-run.png')
        if self.name == 'bee':
            self.cut_sheet(self.sheet_run, 4, 1, self.frames_run)
        else:
            self.cut_sheet(self.sheet_run, 6, 1, self.frames_run)

        self.frames_die = []
        self.sheet_die = load_image(f'{name}-die.png')
        self.cut_sheet(self.sheet_die, 4, 1, self.frames_die)

        self.image = self.frames_stay[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 5
        self.count_to_death = 0
        self.call_of_death = False

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
        if self.condition == 'death':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_die)
            self.image = self.frames_die[self.cur_frame]
            self.count_to_death += 1
            if self.count_to_death >= 7:
                self.death()
        if self.condition == 'attack':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_stay)
            self.image = self.frames_stay[self.cur_frame]
            self.chase(hero_pos)

    def get_damage(self, damage):
        if pygame.sprite.spritecollideany(self, hero.hero_group):
            self.health -= damage
            self.condition = 'angry'
        if self.health <= 0:
            self.condition = 'death'

    def death(self):
        self.damage = 0
        if not self.call_of_death:
            main.plus_score()
            self.call_of_death = True
        self.kill()

    def alive(self):
        if self.health > 0:
            return False
        else:
            return True

    def chase(self, hero_pos):
        if not pygame.sprite.spritecollideany(self, hero.hero_group):
            self.condition = 'angry'
            if self.rect.x < hero_pos[0]:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rect.x += self.speed
            if self.rect.x > hero_pos[0]:
                self.rect.x -= self.speed
            if self.rect.y < hero_pos[1]:
                self.rect.y += self.speed
            if self.rect.y > hero_pos[1]:
                self.rect.y -= self.speed
        else:
            self.condition = 'attack'

    def attack(self):
        if pygame.sprite.spritecollideany(self, hero.hero_group):
            return self.damage
        return 0
