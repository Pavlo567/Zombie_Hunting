from pygame import *
from random import *
import math
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
bullet_image = image.load("img/ghfhjgkg.png")

# фонова музика
mixer.music.load('img/khp.mp3')
mixer.music.set_volume(0.4)
mixer.music.play(-1)

#окремі звуки
fire_sound = mixer.Sound('img/gun_fire.wav')
fire_sound.set_volume(0.4)
dead_sound = mixer.Sound('img/Death.wav')
dead_sound.set_volume(0.2)

def random_position():
    side = choice(["top", "bottom", "left", "right"])
    if side == "top":
        return (randint(0, WIDTH), -150)
    elif side == "bottom":
        return (randint(0, WIDTH), HEIGHT + 150)
    elif side == "left":
        return (-150, randint(0, HEIGHT))
    elif side == "right":
        return (HEIGHT, randint(0, HEIGHT))

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
        fire_sound.play()

class Enemy(sprite.Sprite):
    def __init__(self, enem_x, enem_y):
        super().__init__()
        self.width = 100
        self.height = 100
        self.image = transform.scale(zombie_image, (self.width, self.height))
        self.orig_image = self.image
        self.speed = 3
        self.rect = self.image.get_rect()
        self.rect.x = enem_x
        self.rect.y = enem_y
    def update(self):
        
        angle = math.degrees(math.atan2(self.rect.y-player.rect.y,player.rect.x - self.rect.x))
        self.image = transform.rotate(self.orig_image, angle) # поворот кулі в напрямку пострілу
        
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
    

class Bullet(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = (x, y)
        mx, my = mouse.get_pos() # координати мишки
        self.dir = (mx - x, my - y)
        lenght = math.hypot(*self.dir)
        if lenght == 0.0:
            self.dir = (0, -1) #напрямок пострілу
        else:
            self.dir = (self.dir[0]/lenght, self.dir[1]/lenght)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.image = Surface((9, 4)).convert_alpha() #зображення кулі
        self.image.fill((156, 91, 0)) # колір кулі в RGB
        self.image = transform.rotate(self.image, angle) # поворот кулі в напрямку пострілу
        self.speed = 13
        self.rect = Rect(x, y, 9, 4)

    def update(self): # рух кулі
        self.rect.x += self.dir[0]*self.speed
        self.rect.y += self.dir[1]*self.speed
        # видалення кулі при виході за межі екрану
        if not window.get_rect().collidepoint(self.pos):
            self.kill()

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
score_text = Text("KILLED: 0", 20, 50, color = (255, 140, 0))
# напис з результатом гри
result_text = Text("YOU WIN!", 350, 250, font_size = 50, color = (0, 255,0))
restart_btn = Text("RESTART", 370, 350, font_size = 40, color = (0, 255, 0))
#додавання фону
bg = transform.scale(bg_image, (WIDTH, HEIGHT))

# створення спрайтів
player = Player(player_image, player_speed=4, player_x=250, player_y=300)
bullets = sprite.Group()
zombies = sprite.Group()


# основні змінні для гри
run = True
finish = False
clock = time.Clock()
FPS = 60
score = 0
lost = 0

# Змінні для генерації ворогів
last_enemy_time = time.get_ticks()
enemy_interval = randint(1000, 3000)

# ігровий цикл
while run:
    # перевірка подій
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            player.fire()
        if e.type == MOUSEBUTTONDOWN and finish:
            x, y = mouse.get_pos()
            if restart_btn.rect.collidepoint(x,y):
                finish = False
                lost = 0
                score = 0
                score_text.set_text("KILLED:" + str(score))
                zombies = sprite.Group()

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:  #якщо натиснуто ESCAPE
                menu.enable()
                menu.mainloop(window)
    if not finish: # поки гра триває
        # Отримання часу, що пройшов з моменту запуску гри
        current_time = time.get_ticks()
        # Перевірка часу, що пройшов з моменту появи останнього ворога
        if current_time - last_enemy_time > enemy_interval:
            # Генерація нового ворога на випадковій стороні екрану
            x,y = random_position()
            zombies.add(Enemy(x,y))
            # Оновлення часу останнього ворога та інтервалу часу між появами ворогів
            last_enemy_time = current_time
            enemy_interval = randint(1000, 3000)
        player.update()
        zombies.update()
        bullets.update()

        spritelist = sprite.groupcollide(zombies, bullets, True, True, sprite.collide_mask)
        for collide in spritelist:
            score += 1
            score_text.set_text("KILLED:" + str(score))
            dead_sound.play()
        spritelist = sprite.spritecollide(player, zombies,False, sprite.collide_mask)
        for collide in spritelist:
            finish = True
            result_text.color = (255,0,0)
            result_text.set_text("YOU LOSE!")

        if score >= 50:
            finish = True
         #відрисовуємо фон
        window.blit(bg, (0, 0)) 
        #відрисовуємо спрайти
        player.draw() 
        zombies.draw(window)
        bullets.draw(window)
    else:
        result_text.draw() # текст вкінці гри
        restart_btn.draw()
    
    score_text.draw()
    # оновлення екрану і FPS
    display.update()
    clock.tick(FPS)