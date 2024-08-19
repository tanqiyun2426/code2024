import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, bullet_img, SCREEN_WIDTH):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.SCREEN_WIDTH = SCREEN_WIDTH

    def update(self, player, enemy, bullet_group):
        self.rect.x += (self.direction * self.speed)
        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > self.SCREEN_WIDTH:
            self.kill()

        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()

        if type(enemy) == pygame.sprite.Group:
            for enemy_single in enemy:
                if pygame.sprite.spritecollide(enemy_single, bullet_group, False):
                    if enemy_single.alive:
                        enemy_single.health -= 25
                        self.kill()
        else:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()


def shot(place, Player, enemy, bullet_group, bullet_img, SCREEN_WIDTH):
    #传入值：place:一个字典，包含x,y轴位置信息，direction方向
    #       Player：攻击者，单个精灵
    #       enemy：被攻击目标，单个精灵或者精灵组
    #       buttle_group：子弹，精灵组
    #       buttle_img：子弹图片
    #       SCREEN_WIDTH：屏幕宽度

    # 未传入位置时 返回
    if place == 'empty':
        return

    #解析位置信息
    x = place['x']
    y = place['y']
    direction = place['direction']

    #创建子弹bullet，并将其添加至bullet_group，然后运行bullet的update函数
    bullet = Bullet(x, y, direction, bullet_img, SCREEN_WIDTH)
    bullet_group.add(bullet)
    bullet.update(Player, enemy, bullet_group)
