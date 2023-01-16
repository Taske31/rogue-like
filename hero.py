import pygame
import sys
import os

pygame.init()
window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
size = width, height = window.get_size()
hero_group = pygame.sprite.Group()
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


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


class Hero(pygame.sprite.Sprite):

    def __init__(self, columns, rows):
        super().__init__(hero_group)
        self.frames_stay = []
        self.sheet = load_image('hero.png')
        self.cut_sheet(self.sheet, columns, rows, self.frames_stay)
        self.cur_frame = 0
        self.image = self.frames_stay[self.cur_frame]

        self.frames_run = []
        self.sheet_run = load_image('Run-Sheet.png')
        self.cut_sheet(self.sheet_run, 8, 1, self.frames_run)

        self.frames_attack_red = []
        self.sheet_attack = load_image(f'Attack_red.png', -1)
        self.cut_sheet(self.sheet_attack, 8, 1, self.frames_attack_red)

        self.frames_attack = []
        self.sheet_attack = load_image(f'Attack.png')
        self.cut_sheet(self.sheet_attack, 8, 1, self.frames_attack)

        self.frames_attack_black = []
        self.sheet_attack = load_image(f'Attack_black.png', -1)
        self.cut_sheet(self.sheet_attack, 8, 1, self.frames_attack_black)

        self.frames_death = []
        self.sheet_death = load_image('Death.png')
        self.cut_sheet(self.sheet_death, 8, 1, self.frames_death)

        self.rect = self.image.get_rect()
        self.rect.x = 120
        self.rect.y = 385
        self.right = True
        self.speed = 30
        self.damage = 10
        self.health = 100
        self.condition = ''
        self.count_to_death = 0

    def swap_weapon(self, name):
        if name == 'black':
            self.damage = 30
        if name == 'red':
            self.damage = 20
        if name == 'nothing':
            pass
    def cut_sheet(self, sheet, columns, rows, frame):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def animation(self, keys, button):
        if self.condition == 'death':
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_death)
            self.image = self.frames_death[self.cur_frame]
            if self.cur_frame >= 7:
                self.cur_frame = 7
                self.frames_death = [self.frames_death[self.cur_frame]]

        else:
            if keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s]:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_run)
                self.image = self.frames_run[self.cur_frame]
            elif button[0]:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_attack)
                self.image = self.frames_attack[self.cur_frame]
            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_stay)
                self.image = self.frames_stay[self.cur_frame]
            if not self.right:
                self.image = pygame.transform.flip(self.image, True, False)

    def move(self, keys):
        self.speed = 10
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.speed += 5
        if keys[pygame.K_d]:
            if self.rect.x < width - 180:
                if not self.right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = True
                self.rect.x += self.speed
        if keys[pygame.K_a]:
            if self.rect.x > 120:
                if self.right:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.right = False
                self.rect.x -= self.speed
        if keys[pygame.K_w]:
            if self.rect.y > 120:
                self.rect.y -= self.speed
        if keys[pygame.K_s]:
            if self.rect.y < height - 230:
                self.rect.y += self.speed

    def get_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.condition = 'death'

    def attack(self):
        return self.damage

    def death(self):
        terminate()
