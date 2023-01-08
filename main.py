import pygame
import sys
import os
import settings
import hero
import time
import map
import mobs

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    size = width, height = window.get_size()
    window.fill((255, 255, 255))
    font = pygame.font.Font(None, 75)
    hero_group = hero.hero_group
    mobs_group = mobs.mobs_group
    clock = pygame.time.Clock()
    FPS = 30

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
    hero = hero.Hero(4, 1)
    boar = mobs.Mob('boar', 20, 30, (500, 200))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings.open_settings()
            if event.type == pygame.MOUSEBUTTONDOWN:
                boar.get_damage(hero.damage)

        game_map = map.game_map

        map.tiles_group.draw(window)

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        hero.move(keys)
        hero.animation(keys, mouse)

        boar.animation(hero.rect)

        hero_group.draw(window)
        mobs_group.draw(window)

        pygame.display.flip()
        clock.tick(FPS)
        window.fill((255, 255, 255))

    pygame.quit()
