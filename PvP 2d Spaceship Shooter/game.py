import pygame 
from pygame.locals import *
import time
import os
import math
pygame.font.init()
pygame.mixer.init()
SPACE_IMAGE = pygame.image.load(os.path.join('game 1', 'assets', 'space.png'))
WH = 450
WW = 900
wn = pygame.display.set_mode((WW,WH))
pygame.display.set_caption("game")
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,255,0)
SPACESHIP_HEIGHT = 80
SPACESHIP_WIDTH = 110
ship_vel = 5
bullet_vel = 10
max_bullets = 3
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
STOP_SHOOTING = pygame.USEREVENT + 3
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
SPACESHIP_SIZE = (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
FPS = 60
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('game 1', 'assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,SPACESHIP_SIZE),90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('game 1', 'assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,SPACESHIP_SIZE),270)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('game 1', 'assets', 'Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('game 1', 'assets', 'Assets_Gun+Silencer.mp3'))

#SPACE = pygame.transform.scale(SPACE_IMAGE,(WW, WH))
border = pygame.Rect( WW/2 - 30, 0, 30, WH)


def draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health, winner_text):
    #wn.fill(WHITE)
    wn.blit(SPACE_IMAGE,(0,0))
    pygame.draw.rect(wn, BLACK, border)
    red_health_text = HEALTH_FONT.render("HEALTH: "+ str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("HEALTH: "+ str(yellow_health), 1, WHITE)
    win_text = HEALTH_FONT.render(str(winner_text),1,WHITE)
    wn.blit(red_health_text, (WW - red_health_text.get_width() - 10, 10))
    wn.blit(yellow_health_text, (10,10))
    wn.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))
    wn.blit(RED_SPACESHIP,(red.x, red.y))
    wn.blit(win_text, (WW/2  - win_text.get_width()/2, WH/2 - win_text.get_height()/2))
    for bullet in red_bullets:
        pygame.draw.rect(wn, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(wn, YELLOW, bullet)
    pygame.display.update()

def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= ship_vel
    if keys_pressed[pygame.K_DOWN] and red.y < WH - SPACESHIP_HEIGHT - 30:
        red.y += ship_vel
    if keys_pressed[pygame.K_LEFT] and red.x > WW/2:
        red.x -= ship_vel
    if keys_pressed[pygame.K_RIGHT] and red.x < WW - SPACESHIP_WIDTH:
        red.x += ship_vel

def yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= ship_vel
    if keys_pressed[pygame.K_s] and yellow.y < WH - SPACESHIP_HEIGHT - 30:
        yellow.y += ship_vel
    if keys_pressed[pygame.K_a] and yellow.x > 0:
        yellow.x -= ship_vel
    if keys_pressed[pygame.K_d]  and  yellow.x < WW/2 - SPACESHIP_WIDTH:
        yellow.x += ship_vel
    
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WW:
            yellow_bullets.remove(bullet)
        


 

def main():
    yellow = pygame.Rect(0,290, SPACESHIP_WIDTH - 40, SPACESHIP_HEIGHT)
    red = pygame.Rect(690, 290, SPACESHIP_WIDTH - 40, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    game_running = True
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    yellow_release = True
    red_release = True
    end = False
    while game_running:
        while not end:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    quit()

            if (math.sqrt((yellow.x-red.x)**2+(yellow.y-red.y)**2)) < 80:
                game_running = False
        
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_ESCAPE]:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and yellow_release and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow.x + SPACESHIP_WIDTH, yellow.y + SPACESHIP_WIDTH/2 - 10, 40,20)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    yellow_release = False
                if event.key == pygame.K_RCTRL and red_release and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x - 40, red.y + SPACESHIP_WIDTH/2 - 10, 40,20)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    red_release = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    yellow_release = True
                if event.key == pygame.K_RCTRL:
                    red_release = True

            if event.type == RED_HIT: 
                red_health -= 1
                BULLET_HIT_SOUND.play()
                pygame.event.post(pygame.event.Event(STOP_SHOOTING))
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
                pygame.event.post(pygame.event.Event(STOP_SHOOTING))
            winner_text = ""
            if red_health <= 0:
                winner_text = "Yellow Wins!"
                end = True
            elif yellow_health <= 0:
                winner_text = "Red Wins!"
                end = True
            #if winner_text != "":
                
            red_movement(keys_pressed,red)
            yellow_movement(keys_pressed,yellow)
            draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health, winner_text)
            handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health, winner_text)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            quit()
if __name__ == "__main__":
    main()