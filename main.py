import pygame
import sys
import os
import settings
import hero
import map
import mobs
import chest


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


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    size = width, height = window.get_size()
    window.fill((255, 255, 255))
    font = pygame.font.Font(None, 40)
    fon = pygame.transform.scale(load_image('floor.png'), (width, height))
    hero_group = hero.hero_group
    mobs_group = mobs.mobs_group
    chest_group = chest.chest_group
    clock = pygame.time.Clock()
    FPS = 24


    def death_screen():
        window.blit(fon, (0, 0))
        text_coord = 300
        death_screen_text = ["Экран смерти.", "",
                      "НР вашего персонажа опустилось до 0.",
                      "Старайтесь так не делать.",
                      "*Нажмите на любую клавишу что бы начать новый забег*"]
        for line in death_screen_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            death_screen_rect = string_rendered.get_rect()
            text_coord += 10
            death_screen_rect.top = text_coord
            death_screen_rect.x = 500
            text_coord += death_screen_rect.height
            window.blit(string_rendered, death_screen_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  terminate()
            pygame.display.flip()
            clock.tick(FPS)

    def intro():
        window.blit(fon, (0, 0))
        text_coord = 300
        intro_text = ["Начальный экран.", "",
                      "Убивайте противников, проходите в следующие комнаты.",
                      "Получайте сундуки с новым оружием, веселитесь.",
                      "*Нажмите на любую клавишу что бы выйти*"]
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 500
            text_coord += intro_rect.height
            window.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(FPS)


    def terminate():
        pygame.quit()
        sys.exit()

    def health_bar(health):
        text = font.render("HP", True, (255, 255, 255))
        window.blit(text, (width - 400, 50))
        pygame.draw.rect(window, (255, 0, 0), (width - 340, 50, health * 2, 30))


    def attack(receiver, attacker):
        receiver.get_damage(attacker.attack())


    hero_object = hero.Hero(4, 1)
    hero_health = 100
    boar = mobs.Mob('boar', 20, 30, (500, 200))
    boar2 = mobs.Mob('boar', 20, 30, (700, 800))
    chest = chest.Chest((500, 500))
    run = True
    DEATHTIMER = pygame.USEREVENT + 1
    BOARTIMER = pygame.USEREVENT
    intro()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings.open_settings()
            if event.type == pygame.MOUSEBUTTONDOWN:
                attack(boar, hero_object)
                attack(boar2, hero_object)
                if pygame.sprite.spritecollide(boar, hero_group, False):
                    pygame.time.set_timer(BOARTIMER, 2000)
            if event.type == BOARTIMER:
                attack(hero_object, boar)
                attack(hero_object, boar2)
            if hero_health <= 0:
                pygame.time.set_timer(DEATHTIMER, 500)
            if event.type == DEATHTIMER:
                death_screen()

        game_map = map.game_map

        map.tiles_group.draw(window)

        hero_health = hero_object.health
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        hero_object.move(keys)
        hero_object.animation(keys, mouse)

        boar.animation(hero_object.rect)
        boar2.animation(hero_object.rect)

        hero_group.draw(window)
        mobs_group.draw(window)
        chest_group.draw(window)

        health_bar(hero_health)
        pygame.display.flip()
        clock.tick(FPS)
        window.fill((255, 255, 255))

    pygame.quit()
