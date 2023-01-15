import pygame
import sys
import os
import settings
import hero
import map
import mobs
import chest
import random
import door

mob_list ={
    'boar_brown': [20, 100],
    'boar_black': [30, 100],
    'boar_white': [15, 100],
    'bee': [25, 50]

}
mob_list_keys = ['boar_brown', 'boar_black', 'boar_white', 'bee']


def mobs_count():
    global amount_of_mobs
    amount_of_mobs -= 1
    if amount_of_mobs <= 0:
        door.spawn_door()


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
    amount_of_mobs = 3


    def death_screen():
        window.blit(fon, (0, 0))
        text_coord = 300
        death_screen_text = ["Экран смерти.", "",
                      "НР вашего персонажа опустилось до 0.",
                      "Старайтесь так не делать.",
                      "*Нажмите на любую клавишу что бы выйти*"]
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
                      "*Нажмите на любую клавишу что бы начать*"]
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

    def new_level():
        hero_object.rect.x = 120
        hero_object.rect.y = 385
        mob1_name = random.choice(mob_list_keys)
        mob1 = mobs.Mob(mob1_name, mob_list[mob1_name][0], mob_list[mob1_name][1], (random.randint(200, width - 200),
                                                                random.randint(200, height - 200)))
        mob2_name = random.choice(mob_list_keys)
        mob2 = mobs.Mob(mob2_name, mob_list[mob2_name][0], mob_list[mob2_name][1], (random.randint(200, width - 200),
                                                                random.randint(200, height - 200)))
        mob3_name = random.choice(mob_list_keys)
        mob3 = mobs.Mob(mob3_name, mob_list[mob3_name][0], mob_list[mob3_name][1], (random.randint(200, width - 200),
                                                                random.randint(200, height - 200)))
        return mob1, mob2, mob3

    hero_object = hero.Hero(4, 1)
    hero_health = 100
    door = door.Door((width // 2, 0))
    mob1, mob2, mob3 = new_level()
    run = True
    DEATHTIMER = pygame.USEREVENT + 1
    ENEMYTIMER1 = pygame.USEREVENT
    ENEMYTIMER2 = pygame.USEREVENT + 2
    ENEMYTIMER3 = pygame.USEREVENT + 3

    intro()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings.open_settings()
            if event.type == pygame.MOUSEBUTTONDOWN:
                attack(mob1, hero_object)
                attack(mob2, hero_object)
                attack(mob3, hero_object)
                if pygame.sprite.spritecollide(mob1, hero_group, False):
                    pygame.time.set_timer(ENEMYTIMER1, 2000)
                else:
                    pygame.time.set_timer(ENEMYTIMER1, 0)
                if pygame.sprite.spritecollide(mob2, hero_group, False):
                    pygame.time.set_timer(ENEMYTIMER2, 2000)
                else:
                    pygame.time.set_timer(ENEMYTIMER2, 0)
                if pygame.sprite.spritecollide(mob3, hero_group, False):
                    pygame.time.set_timer(ENEMYTIMER3, 2000)
                else:
                    pygame.time.set_timer(ENEMYTIMER3, 0)
            if event.type == ENEMYTIMER1:
                attack(hero_object, mob1)
            if event.type == ENEMYTIMER2:
                attack(hero_object, mob2)
            if event.type == ENEMYTIMER3:
                attack(hero_object, mob3)
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

        mob1.animation(hero_object.rect)
        mob2.animation(hero_object.rect)
        mob3.animation(hero_object.rect)

        hero_group.draw(window)
        mobs_group.draw(window)
        chest_group.draw(window)

        health_bar(hero_health)
        pygame.display.flip()
        clock.tick(FPS)
        window.fill((255, 255, 255))

    pygame.quit()
