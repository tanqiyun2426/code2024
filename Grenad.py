import pygame


class Grenade(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, grenade_img, SCREEN_WIDTH, GRAVITY, TILE_SIZE):
		pygame.sprite.Sprite.__init__(self)
		self.timer = 100
		self.vel_y = -11
		self.speed = 7
		self.image = grenade_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction
		self.SCREEN_WIDTH = SCREEN_WIDTH
		self.GRAVITY = GRAVITY
		self.TILE_SIZE = TILE_SIZE

	def update(self, player, enemy_group, grenade_group, explosion_group):
		self.vel_y += self.GRAVITY
		dx = self.direction * self.speed
		dy = self.vel_y

		#check collision with floor
		if self.rect.bottom + dy > 300:
			dy = 300 - self.rect.bottom
			self.speed = 0

		#check collision with walls
		if self.rect.left + dx < 0 or self.rect.right + dx > self.SCREEN_WIDTH:
			self.direction *= -1
			dx = self.direction * self.speed

		#update grenade position
		self.rect.x += dx
		self.rect.y += dy

		# countdown timer
		self.timer -= 1
		if self.timer <= 0:
			self.kill()
			explosion = Explosion(self.rect.x, self.rect.y, 0.5)
			explosion_group.add(explosion)
			# do damage to anyone that is nearby
			if (abs(self.rect.centerx - player.rect.centerx) < self.TILE_SIZE * 2 and
						abs(self.rect.centery - player.rect.centery) < self.TILE_SIZE * 2):
				player.health -= 50
			for enemy in enemy_group:
				if abs(self.rect.centerx - enemy.rect.centerx) < self.TILE_SIZE * 2 and	\
						abs(self.rect.centery - enemy.rect.centery) < self.TILE_SIZE * 2:
					enemy.health -= 50




class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, scale):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
			self.images.append(img)
		self.frame_index = 0
		self.image = self.images[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0


	def update(self,player,enemy):
		EXPLOSION_SPEED = 4
		#update explosion amimation
		self.counter += 1

		if self.counter >= EXPLOSION_SPEED:
			self.counter = 0
			self.frame_index += 1
			#if the animation is complete then delete the explosion
			if self.frame_index >= len(self.images):
				self.kill()
			else:
				self.image = self.images[self.frame_index]

