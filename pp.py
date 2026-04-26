from pygame import *
from time import sleep

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (100, 100))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Left(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 500 - 80:
            self.rect.y += self.speed

class Right(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 500 - 80:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction_x = player_speed
        self.direction_y = player_speed
    
    def update(self):
        self.rect.x += self.direction_x
        self.rect.y += self.direction_y
        
        if self.rect.y <= 0 or self.rect.y >= 500 - 80:
            self.direction_y = -self.direction_y
        
        if sprite.collide_rect(self, left_racket) or sprite.collide_rect(self, right_racket):
            self.direction_x = -self.direction_x

window = display.set_mode((700, 500))
display.set_caption('ping pong')
background = transform.scale(image.load('background.jpg'), (700, 500))

left_racket = Left('pplracket.png', 40, 200, 5)
right_racket = Right('pprracket.png', 560, 200, 5)

ball = Ball('ppball.png', 300, 200, 5)

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('xtt.mp3')
mixer.music.play()

font.init()
font1 = font.SysFont('Arial', 70)
font_counter = font.SysFont('Arial', 50)

font_counter.set_bold(True)

counter_blue = 0
counter_red = 0

game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        
        clock.tick(FPS)
        window.blit(background, (0, 0))

        if ball.rect.x < -100:
            counter_red += 1
            FPS += 4
            ball.rect.x = 300
            ball.rect.y = 200
        if ball.rect.x > 700:
            counter_blue += 1
            FPS += 4
            ball.rect.x = 300
            ball.rect.y = 200

        blues_score = font_counter.render(str(counter_blue), True, (0, 0, 200))
        reds_score = font_counter.render(str(counter_red), True, (200, 0, 0))
        window.blit(blues_score, (30, 30))
        window.blit(reds_score, (650, 30))

        if counter_blue == 10:
            window.blit(font1.render('Player1 wins', True, (0, 0, 200)), (250, 200))
            ball.rect.x = -4444
            finish = True
        if counter_red == 10:
            window.blit(font1.render('Player2 wins', True, (200, 0, 0)), (250, 200))
            ball.rect.x = -4444
            finish = True
            

        left_racket.update()
        left_racket.reset()
        right_racket.update()
        right_racket.reset()
        ball.update()
        ball.reset()

        display.update()

    if finish:
        for i in range(4):
            sleep(1)
            print(4 - i)
        game = False