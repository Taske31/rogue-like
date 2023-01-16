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

# название всех мобов
mob_list = {
    'boar_brown': [20, 100],
    'boar_black': [30, 100],
    'boar_white': [15, 100],
    'bee': [25, 50]

}
mob_list_keys = ['boar_brown', 'boar_black', 'boar_white', 'bee']
amount_of_mobs = 0


# загрузка картинок
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


# возваращаем результаты
def return_score():
    return str(amount_of_mobs)


# прибавляем очки
def plus_score():
    global amount_of_mobs
    amount_of_mobs += 1
    print(amount_of_mobs)


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
    door_group = door.door_group
    clock = pygame.time.Clock()
    FPS = 24


    def death_screen():
        window.blit(fon, (0, 0))
        text_coord = 300
        death_screen_text = ["Экран смерти.", "",
                             "НР вашего персонажа опустилось до 0.",
                             "Старайтесь так не делать.",
                             f"Вы набрали {return_score()} очка(о)",
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
                    return terminate()
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
        # цикл пока не нажата кнопка
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            clock.tick(FPS)

    # закрытие программмы
    def terminate():
        pygame.quit()
        sys.exit()

    # полоска здоровья
    def health_bar(health):
        text = font.render("HP", True, (255, 255, 255))
        window.blit(text, (width - 400, 50))
        pygame.draw.rect(window, (255, 0, 0), (width - 340, 50, health * 2, 30))

    # атака объектов
    def attack(receiver, attacker):
        receiver.get_damage(attacker.attack())

    # новый уровень
    def new_level():
        global mob1, mob2, mob3
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

    # спавним дверь, если все мобы умерли
    def mobs_count(m1, m2, m3):
        import chest
        import hero
        if m1 and m2 and m3:
            chest = chest.Chest((500, 500))
            if chest.open():
                color = ['black', 'red', 'nothing']
                win = random.choice(color)
                hero_object.swap_weapon(win)
            door.spawn_door()
            return True


    hero_object = hero.Hero(4, 1)
    hero_health = 100
    door = door.Door((width // 2, 0))
    mob1, mob2, mob3 = new_level()
    run = True
    # таймеры
    DEATHTIMER = pygame.USEREVENT
    ENEMYTIMER1 = pygame.USEREVENT + 1
    ENEMYTIMER2 = pygame.USEREVENT + 2
    ENEMYTIMER3 = pygame.USEREVENT + 3
    mob1_attack = False
    mob2_attack = False
    mob3_attack = False

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
                    mob1_attack = True
                else:
                    pygame.time.set_timer(ENEMYTIMER1, 0)
                if pygame.sprite.spritecollide(mob2, hero_group, False):
                    pygame.time.set_timer(ENEMYTIMER2, 2000)
                    mob2_attack = True
                else:
                    pygame.time.set_timer(ENEMYTIMER2, 0)
                if pygame.sprite.spritecollide(mob3, hero_group, False):
                    pygame.time.set_timer(ENEMYTIMER3, 2000)
                    mob3_attack = True
                else:
                    pygame.time.set_timer(ENEMYTIMER3, 0)
            if event.type == ENEMYTIMER1:
                attack(hero_object, mob1)
                mob1_attack = False
            if event.type == ENEMYTIMER2:
                attack(hero_object, mob2)
                mob2_attack = False
            if event.type == ENEMYTIMER3:
                attack(hero_object, mob3)
                mob3_attack = False
            if hero_health <= 0:
                pygame.time.set_timer(DEATHTIMER, 500)
            if event.type == DEATHTIMER:
                death_screen()

        game_map = map.game_map

        map.tiles_group.draw(window)
        # доп функции
        hero_health = hero_object.health
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        hero_object.move(keys)
        hero_object.animation(keys, mouse)
        # анимация спрайтов
        mob1.animation(hero_object.rect)
        mob2.animation(hero_object.rect)
        mob3.animation(hero_object.rect)
        # отрисовка объектов
        hero_group.draw(window)
        mobs_group.draw(window)
        chest_group.draw(window)
        # условие появления двери
        if mobs_count(mob1.alive(), mob2.alive(), mob3.alive()):
            door_group.draw(window)
            chest_group.draw(window)
            if door.new_level():
                new_level()
        health_bar(hero_health)
        pygame.display.flip()
        clock.tick(FPS)
        window.fill((255, 255, 255))

    pygame.quit()
