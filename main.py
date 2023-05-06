from pygame import *
from random import randint

import os

init()
font.init()
mixer.init()

# розміри вікна
WIDTH, HEIGHT = 900, 600

# картинка фону
bg_image = image.load("img/Ground_01.png")
#картинки для спрайтів
player_image = image.load("img/soldier/survivor-move_shotgun_0.png")
zombie_image = image.load("img/zombie/skeleton-attack_0.png")

# фонова музика
mixer.music.load('ente_evil.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

#окремі звуки
# fire_sound = mixer.Sound(".wav")
# fire_sound.set_volume(0.2)

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y, speed = 3):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.mask = mask.from_surface(self.image)  

    def draw(self): #відрисовуємо спрайт у вікні
        window.blit(self.image, self.rect)

class Player(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__()
        self.width = 100
        self.height = 100
        self.image_orig = transform.scale(player_image, (self.width, self.height))
        self.image = self.image_orig
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > -1000:
            self.rect.x -= self.speed
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > -1000:
            self.rect.x -= self.speed
            self.image = transform.rotate(self.image_orig, 180)
        if keys_pressed[K_d] and self.rect.x > -1000:
            self.rect.x += self.speed
            self.image = self.image_orig
        if keys_pressed[K_w] and self.rect.y > -1000:
            self.rect.y -= self.speed
            self.image = transform.rotate(self.image_orig, 90)
        if keys_pressed[K_s] and self.rect.y > -1000:
            self.rect.y += self.speed
            self.image = transform.rotate(self.image_orig, -90)

    def fire(self):
            print(self.rect.right)
            bullets.add(Bullet(self.rect.x + self.width - 10, self.rect.y + self.height * 0.75))

class Enemy(sprite.Sprite):
    def __init__(self, enem_image, enem_speed, enem_x, enem_y):
        super().__init__()
        self.width = 100
        self.height = 100
        self.image = transform.scale(enem_image, (self.width, self.height))
        self.speed = enem_speed
        self.rect = self.image.get_rect()
        self.rect.x = enem_x
        self.rect.y = enem_y
    def update(self):
        # if self.rect.x > 0:
        #      self.rect.x -= self.speed

        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        # Movement along y direction
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Text(sprite.Sprite):
    def __init__(self, text, x, y, font_size=22, font_name="Impact", color=(255,255,255)):
        self.font = font.SysFont(font_name, font_size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        
    def draw(self): #відрисовуємо спрайт у вікні
        window.blit(self.image, self.rect)
    
    def set_text(self, new_text): #змінюємо текст напису
        self.image = self.font.render(new_text, True, self.color)


# створення вікна
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Zombie Hunting")

# написи для лічильників очок
score_text = Text("Score: 0", 20, 50)
# напис з результатом гри
result_text = Text("YOU WIN!", 350, 250, font_size = 50)

#додавання фону
bg = transform.scale(bg_image, (WIDTH, HEIGHT))

# створення спрайтів
player = Player(player_image, player_speed=4, player_x=250, player_y=300)
zombies = sprite.Group()
zombies.add(Enemy(zombie_image, 3, 500, 500))


# основні змінні для гри
run = True
finish = False
clock = time.Clock()
FPS = 60
score = 0
lost = 0

# ігровий цикл
while run:
    # перевірка подій
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:  #якщо натиснуто ESCAPE
                menu.enable()
                menu.mainloop(window)
    if not finish: # поки гра триває
        # рух спрайтів
        player.update() #рух гравця
        zombies.update()

         #зіткнення гравця і ворогів
        spritelist = sprite.spritecollide(player, zombies, False)
        for collide in spritelist:
            finish = True
            result_text.set_text("YOU LOSE!")
        # перевірка зіткнення 2 груп спрайтів
        # spritelist = sprite.groupcollide(ufos, bullets, True, True)
        # for collide in spritelist:
        #     explosions.add(Explosion(collide.rect.x, collide.rect.y, images_list))
        #     score += 1
        #     score_text.set_text("Рахунок:" + str(score))
       
        if score >= 10:
            finish = True
         #відрисовуємо фон
        window.blit(bg, (0, 0)) 
        #відрисовуємо спрайти
        player.draw() 
        zombies.draw(window)
    else:
        result_text.draw() # текст вкінці гри
    score_text.draw()
    # оновлення екрану і FPS
    display.update()
    clock.tick(FPS)