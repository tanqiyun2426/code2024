import pygame
import os
from Soldier import Soldier
from Shot import shot
from Grenad import Grenade
from Grenad import Explosion
from Box import ItemBox
from Box import HealthBar

def main():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Shooter')

    # set framerate
    clock = pygame.time.Clock()
    FPS = 60

    # define game variables
    GRAVITY = 0.75
    TILE_SIZE = 40

    # define player action variables
    moving_left = False
    moving_right = False
    shoot = False
    grenade = False
    grenade_thrown = False
    scale = 3


    # load bullet images
    bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
    #load grenade image
    grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
    # pick up boxes
    health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
    ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
    grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
    item_boxes = {
        'Health': health_box_img,
        'Ammo': ammo_box_img,
        'Grenade': grenade_box_img
    }


    # define colours
    BG = (144, 201, 120)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)

    #define  font
    font = pygame.font.SysFont('Futura', 30)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def draw_bg():
        screen.fill(BG)
        pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

    # create sprite groups
    enemy_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    grenade_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    item_box_group = pygame.sprite.Group()

    item_box = ItemBox('Health', 100, 260, TILE_SIZE, item_boxes)
    item_box_group.add(item_box)
    item_box = ItemBox('Ammo', 400, 260, TILE_SIZE, item_boxes)
    item_box_group.add(item_box)
    item_box = ItemBox('Grenade', 500, 260, TILE_SIZE, item_boxes)
    item_box_group.add(item_box)

    player = Soldier('player', 200, 200, 1.5, 5, 20, screen,
                     SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, 5, TILE_SIZE)
    health_bar = HealthBar(10, 10, player.health, player.health)


    enemy = Soldier('enemy', 400, 200, 1.5, 5, 20, screen,
                    SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, 0, TILE_SIZE)
    enemy2 = Soldier('enemy', 300, 300, 1.5, 5, 20, screen,
                     SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, 0, TILE_SIZE)
    enemy_group.add(enemy)
    enemy_group.add(enemy2)

    run = True
    while run:

        clock.tick(FPS)

        draw_bg()
        #show player health
        health_bar.draw(player.health,  screen)
        #show ammo
        draw_text('AMMO: ', font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(bullet_img, (90 + (x * 10), 40))
        # show grenades
        draw_text('GRENADES: ', font, WHITE, 10, 60)
        for x in range(player.grenades):
            screen.blit(grenade_img, (135 + (x * 15), 60))

        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.ai(player, enemy, bullet_group, bullet_img, SCREEN_WIDTH)
            enemy.update()
            enemy.draw()

        # update and draw groups
        bullet_group.update(player, enemy_group, bullet_group)  #Exchange
        grenade_group.update(player, enemy_group, grenade_group, explosion_group)
        explosion_group.update(player, enemy_group)
        item_box_group.update(player)
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)

        # update player actions
        if player.alive:
            # shoot bullets
            if shoot:
                shot(player.place(), player, enemy_group, bullet_group, bullet_img, SCREEN_WIDTH)
            elif grenade and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                                  player.rect.top, player.direction, grenade_img, SCREEN_WIDTH, GRAVITY,
                                  TILE_SIZE)
                grenade_group.add(grenade)
                player.grenades -= 1
                grenade_thrown = True

            if player.in_air:
                player.update_action(2)  # 2: jump
            elif moving_left or moving_right:
                player.update_action(1)  # 1: run
            else:
                player.update_action(0)  # 0: idle
            player.move(moving_left, moving_right)

        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                run = False
            # keyboard presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_SPACE:
                    shoot = True
                if event.key == pygame.K_q:
                    grenade = True
                if event.key == pygame.K_w and player.alive:
                    player.jump = True
                if event.key == pygame.K_ESCAPE:
                    run = False

            # keyboard button released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_SPACE:
                    shoot = False
                if event.key == pygame.K_q:
                    grenade = False
                    grenade_thrown = False

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
