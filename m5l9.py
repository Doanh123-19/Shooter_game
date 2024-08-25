from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win_text = font1.render('YOU WIN!!', True, (255, 253, 85))
lose_text = font1.render('YOU LOSE!!', True, (255, 0, 0))
life_text = font2.render('Health:',True,(0, 255, 0))
score = 0
lost = 0
life_color = (0, 255, 0)

mixer.init()
mixer.music.load('fire.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.png'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_ast = 'asteroid.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost, number_of_enemies
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
            number_of_enemies += 1
            add_enemies()


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()


healths = 6
win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
number_of_enemies = 6
number_of_enemies_2 = 4
for i in range(1, number_of_enemies):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

for i in range(1, number_of_enemies_2):
    asteroid = Enemy(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

def add_enemies():
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


goal = 100

finish = False
run = True
reload_time = False
reload_second = 2
number_fire = 6
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                if number_fire > 0 and reload_time == False:
                    number_fire -= 1
                    ship.fire()
                    fire_sound.play()
            if number_fire <= 0 and reload_time == False:
                last_time = timer()
                reload_time = True

    if not finish:
        window.blit(background, (0, 0))
        text = font2.render('Score:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Missed:' + str(lost), 1, (255, 255, 255))
        if healths <= 4 and healths > 2 :
            life_color = (255, 255, 0)
        if healths <= 2:
            life_color = (255, 0, 0)
        life_text = font2.render(str(healths),True,life_color)
        window.blit(life_text,(610,10))
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        window.blit(text_lose, (10, 50))
        if reload_time == True:
            now_time = timer()

            if now_time - last_time <= reload_second:
                reload = font2.render('Out of bullets!!!', 1, (255, 0, 0))
                window.blit(reload, (260, 460))
            else:
                number_fire = 5
                reload_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for is_collides in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            healths -= 1

        collides_2 = sprite.groupcollide(asteroids, bullets, True, True)
        for is_collides in collides_2:
            score += 1
            asteroid = Enemy(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)

        if sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, asteroids, True)
            healths -= 1

        if score >= goal:
            finish = True
            window.blit(win_text, (200, 200))

        if healths == 0:
            finish = True
            window.blit(lose_text, (200, 200))

        if lost >= 7:
            finish = True
            window.blit(lose_text, (200, 200))

        display.update()
    else:
        finish = False
        lost = 0
        healths = 6

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)

        for i in range(1, number_of_enemies):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(1, number_of_enemies_2):
            asteroid = Enemy(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)

    time.delay(50)