import pygame
import random
from PIL import Image

alien_projectiles = pygame.image.load("projectiles_16x16px.png")
backgrounds = pygame.image.load("planet_and_space_tilesets_16x16px.png")
dead_moon_monster = pygame.image.load("moon_monster_explode_80x80px.png")
background = pygame.image.load("star_background_320x240px.png")
blue_alien = pygame.image.load("blue_alien_black_outline_36x36px.png")
green_alien = pygame.image.load("green_alien_black_outline_36x36px.png")
explosion = pygame.image.load("player_ship_32x32px.png")
bgimg = pygame.image.load("star_background_320x240px.png")
bgimg = pygame.transform.scale(bgimg, (960,720))





# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Sounds
bg_music = pygame.mixer.Sound("space-beat-263970.mp3")
player_shoot = pygame.mixer.Sound("laser-104024.mp3")
# Screen dimensions
screen_width = 960
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load(f"Ship{i}.png") for i in range(4)] 
        self.images = [pygame.transform.scale(img, (75, 75)) for img in self.images]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed_x = 0
        self.speed_y = 0
        self.score = 0
        self.shoot_delay = 250 # Cooldown period in milliseconds 
        self.last_shot = pygame.time.get_ticks()
        self.image = pygame.transform.scale(self.image,(75,75))

    def update(self): 
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]: 
            self.speed_x = -5 
            self.index = (self.index + 1) % 4 
            self.image = pygame.transform.scale(self.images[self.index], (75,75))
        elif keys[pygame.K_RIGHT]: 
            self.speed_x = 5 
            self.index = (self.index + 1) % 4 
            self.image = pygame.transform.scale(self.images[self.index], (75,75))
        else: 
            self.speed_x = 0 
        if keys[pygame.K_UP]: 
            self.speed_y = -5 
            self.index = (self.index + 1) % 4 
            self.image = pygame.transform.scale(self.images[self.index], (75,75))
        elif keys[pygame.K_DOWN]: 
            self.speed_y = 5
            self.index = (self.index - 1) % 4 
            self.image = pygame.transform.scale(self.images[self.index], (75,75))
        else: 
            self.speed_y = 0 
        self.rect.x += self.speed_x 
        self.rect.y += self.speed_y 
        if self.rect.left < 0: 
            self.rect.left = 0 
        if self.rect.right > screen_width: 
            self.rect.right = screen_width 
        if self.rect.top < 0: 
            self.rect.top = 0 
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height 
        if keys[pygame.K_SPACE]: 
            self.shoot()


    def shoot(self):
        now = pygame.time.get_ticks() 
        if now - self.last_shot > self.shoot_delay: 
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, crab_enemies)
            all_sprites.add(bullet)
            bullets.add(bullet)
            player_shoot.play()
    def draw(self):
        pass

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, enemies):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = -10
        self.enemies = enemies

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
        hits = pygame.sprite.spritecollide(self, self.enemies, True) 
        # Use enemies group for collision detection 
        if hits: 
            self.kill()

# Squid invader class
class SquidEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"blue{i}.png") for i in range(23)] 
        self.images = [pygame.transform.scale(img, (40, 40)) for img in self.images]
        self.index = 0 
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.velocity = velocity
        self.move_delay = 1000 # Initial delay in milliseconds 
        self.last_move = pygame.time.get_ticks() 
        self.speedup_interval = 1000 # Time interval in milliseconds to speed up

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_move >= self.move_delay:
            self.rect.x += self.velocity * self.move_direction

            # Change direction and move down if at edge 
            if self.rect.right >= screen_width or self.rect.left <= 0: 
                self.move_direction *= -1 
                self.rect.y += 20 
            # Animate the invader 
            self.index = (self.index + 1) % len(self.images) 
            self.image = self.images[self.index]
            self.last_move = now # Update last move time
        # Gradually increase speed over time 
        if now % self.speedup_interval < self.move_delay: 
            self.move_delay = max(0, self.move_delay - 10) # Ensure a minimum delay
        hits = pygame.sprite.spritecollide(self, bullets, True) 
        if hits: 
            self.kill()
            player.score += 30
            print(player.score)

# Squid invader class
class CrabEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"green{i}.png") for i in range(7)] 
        self.images = [pygame.transform.scale(img, (40, 40)) for img in self.images]
        self.index = 0 
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.velocity = velocity
        self.move_delay = 1000 # Initial delay in milliseconds 
        self.last_move = pygame.time.get_ticks() 
        self.speedup_interval = 1000 # Time interval in milliseconds to speed up

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_move >= self.move_delay:
            self.rect.x += self.velocity * self.move_direction

            # Change direction and move down if at edge 
            if self.rect.right >= screen_width or self.rect.left <= 0: 
                self.move_direction *= -1 
                self.rect.y += 20 
            # Animate the invader 
            self.index = (self.index + 1) % len(self.images) 
            self.image = self.images[self.index]
            self.last_move = now # Update last move time
        # Gradually increase speed over time 
        if now % self.speedup_interval < self.move_delay: 
            self.move_delay = max(0, self.move_delay - 10) # Ensure a minimum delay
        hits = pygame.sprite.spritecollide(self, bullets, True) 
        if hits: 
            self.kill()
            player.score += 20
            print(player.score)


# Squid invader class
class OctopusEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"purple{i}.png") for i in range(7)] 
        self.images = [pygame.transform.scale(img, (40, 40)) for img in self.images]
        self.dead_images = self.image = [pygame.image.load(f"dead_purple{i}.png") for i in range(7)]
        self.dead_images = [pygame.transform.scale(img, (40, 40)) for img in self.images]
        self.index = 0 
        self.dead_index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.velocity = velocity
        self.move_delay = 1000 # Initial delay in milliseconds 
        self.last_move = pygame.time.get_ticks() 
        self.speedup_interval = 1000 # Time interval in milliseconds to speed up

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_move >= self.move_delay:
            self.rect.x += self.velocity * self.move_direction

            # Change direction and move down if at edge 
            if self.rect.right >= screen_width or self.rect.left <= 0: 
                self.move_direction *= -1 
                self.rect.y += 20 
            # Animate the invader 
            self.index = (self.index + 1) % len(self.images) 
            self.image = self.images[self.index]
            self.last_move = now # Update last move time
        # Gradually increase speed over time 
        if now % self.speedup_interval < self.move_delay: 
            self.move_delay = max(0, self.move_delay - 10) # Ensure a minimum delay
        hits = pygame.sprite.spritecollide(self, bullets, True) 
        if hits: 
            self.kill()
            player.score += 10
            print(player.score)






# Game loop
running = True
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
squid_enemy = pygame.sprite.Group()
octopus_enemy = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

squid_enemies = pygame.sprite.Group() 
for row in range(2): 
    for col in range(11): 
        squid = SquidEnemy(col * 60 + 50, row * 60 + 50, velocity=3) 
        squid_enemies.add(squid) 
        all_sprites.add(squid)
            

crab_enemies = pygame.sprite.Group() 
for row in range(2): 
    for col in range(11): 
        crab = CrabEnemy(col * 60 + 50, row * 60 + 150, velocity=3) 
        crab_enemies.add(crab) 
        all_sprites.add(crab)

octupus_enemies = pygame.sprite.Group() 
for row in range(2): 
    for col in range(11): 
        octopus = OctopusEnemy(col * 60 + 50, row * 50 + 250, velocity=3) 
        octupus_enemies.add(octopus) 
        all_sprites.add(octopus)

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            bg_music.play(-1)

    # Update
    all_sprites.update()
    squid_enemy.update()

    # Draw/render
    screen.blit(bgimg, (0,0) )
    all_sprites.draw(screen)
    pygame.display.flip()
    squid_enemy.draw(screen)

    # Frame rate
    clock.tick(60)

pygame.quit()
