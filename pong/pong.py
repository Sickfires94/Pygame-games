import pygame 
from pygame.locals import *
import time
import os
import math
import random

pygame.font.init()

FPS = 60

WW = 800
WH = 600
wn = pygame.display.set_mode((WW,WH))
pygame.display.set_caption("Pong")

BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255,0,0)

PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
PADDLE_VEL = 5
PADDLE_IMAGE = pygame.image.load(os.path.join("assets", "paddle.png"))

BALL_RADIUS = 5
BALL_START_X = WW/2
BALL_START_Y = WH/2
BALL_X_VEL = 5
BALL_Y_VEL = 5
MAX_BALL_VEL = 10

RIGHT_SCORE = pygame.USEREVENT + 1
LEFT_SCORE = pygame.USEREVENT + 2
WAIT_3 = pygame.USEREVENT + 3
STOP = pygame.USEREVENT +4

SCORE_FONT = pygame.font.SysFont('comicsans', 40)



def draw_window(left, right, left_score, right_score, ball_rect, stop_text):
    wn.fill(BLACK)

    left_score_text = SCORE_FONT.render("Player 1: " + str(left_score), 1, WHITE)
    right_score_text = SCORE_FONT.render("Player 2: "+ str(right_score), 1, WHITE)
    Score_text = SCORE_FONT.render(stop_text, 1, WHITE)
   

    wn.blit(left_score_text, (10,10))
    wn.blit(right_score_text, (WW - right_score_text.get_width() - 10, 10))
    wn.blit(Score_text, (WW/2 - Score_text.get_width()/2, WH/4 - Score_text.get_height()/2))

    paddle_img = pygame.transform.scale(PADDLE_IMAGE, (right.width, right.height))

    wn.blit(paddle_img, (left.x, left.y))
    wn.blit(paddle_img, (right.x, right.y))
    pygame.draw.circle(wn, WHITE, (ball_rect.x, ball_rect.y), BALL_RADIUS)
    pygame.display.update()


def left_movement(left, keys_pressed, paddle_vel):
    if keys_pressed[pygame.K_w] and left.y > 0:
        left.y -= paddle_vel
       # print("left moved up")
    if keys_pressed[pygame.K_s] and left.y < WH - left.height:
        left.y += paddle_vel
        #print("left moved down")
    

def right_movement(right, keys_pressed, paddle_vel):
    if keys_pressed[pygame.K_UP] and right.y > 0:
        right.y -= paddle_vel
        #print("right moved up")
    if keys_pressed[pygame.K_DOWN] and right.y < WH - right.height:
        right.y += paddle_vel
        #print("Right moved down")


def ball_movement(ball_vel, left, right, ball_rect, ball_collision):
    if left.colliderect(ball_rect) and not ball_collision:
        ball_vel[0] *= -1
        ball_collision = True
        if ball_rect.y - left.y < PADDLE_HEIGHT/4 and ball_vel[1] > 0:            
            ball_vel[1] *= -1
        elif ball_rect.y - left.y > 3*(PADDLE_HEIGHT/4) and ball_vel[1] < 0:
            ball_vel[1] *= -1
        #print("x reversed") 
    else:
        ball_collision = False
    if right.colliderect(ball_rect) and not ball_collision:
        ball_vel[0] *= -1
        ball_collision = True

        if ball_rect.y - right.y < PADDLE_HEIGHT/4 and ball_vel[1] > 0:            
            ball_vel[1] *= -1
        elif ball_rect.y - right.y > 3*(PADDLE_HEIGHT/4) and ball_vel[1] < 0:
            ball_vel[1] *= -1

        #print("x reversed") 
    else:
        ball_collision = False
    
    

    if ball_rect.y <= 0 and ball_vel[1] < 0:
        ball_vel[1] *= -1
        #print("y reversed") 
    if ball_rect.y >= WH - ball_rect.height and ball_vel[1] > 0:
        ball_vel[1] *= -1
        #print("y reversed") 
    if ball_rect.x < 0:
        pygame.event.post(pygame.event.Event(RIGHT_SCORE))
    if ball_rect.x > WW:
        pygame.event.post(pygame.event.Event(LEFT_SCORE))

    ball_rect.x += ball_vel[0]
    ball_rect.y += ball_vel[1]

def main():

    clock = pygame.time.Clock()
    stop_text = ""
    score_txt = ""
    scored = False
    kickoff = True #true = right

    ball_collision = False
    max_speed = False

    paddle_vel = PADDLE_VEL
    
    ball_vel = [BALL_X_VEL, BALL_Y_VEL]
    ball_rect = pygame.Rect(BALL_START_X, BALL_START_Y, BALL_RADIUS*2, BALL_RADIUS*2)
    left = pygame.Rect(0, WH/2 - PADDLE_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right = pygame.Rect(WW - PADDLE_WIDTH, WH/2 - PADDLE_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)

    right_score = 0
    left_score = 0

    game_stop_timer = -1

    game_running = True
    while game_running:
        clock.tick(FPS)

    
    
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                quit()
            if game_stop_timer < 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    stop_text = "Paused"
                    game_stop_timer = 99999
            elif event.type == pygame.MOUSEBUTTONDOWN:
                stop_text = ""
                game_stop_timer = -1
            if event.type == RIGHT_SCORE:
                right_score += 1
                ball_rect.x = BALL_START_X
                ball_rect.y = BALL_START_Y
                ball_vel[0] *= -1
                score_txt = "Right Scored!!!"
                scored = True
                pygame.event.post(pygame.event.Event(WAIT_3))
                kickoff = True
            if event.type == LEFT_SCORE:
                left_score += 1
                ball_vel[0] *= -1
                ball_rect.x = BALL_START_X
                ball_rect.y = BALL_START_Y
                score_txt = "Left Scored!!!"
                scored = True
                kickoff = False
                pygame.event.post(pygame.event.Event(WAIT_3))  
            if event.type == WAIT_3:
                game_stop_timer = 5*FPS
                ball_vel[1] = BALL_Y_VEL
                if random.randint(0,1) == 0:
                    ball_vel[1] *= -1
                if kickoff:
                    ball_vel[0] = BALL_X_VEL
                else:
                    ball_vel[0] = -BALL_X_VEL
                left.height = PADDLE_HEIGHT
                right.height = PADDLE_HEIGHT
                paddle_vel = PADDLE_VEL
                scored = False
                pygame.event.post(pygame.event.Event(STOP))
                


        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[K_ESCAPE]:
            game_running = False
        
        

        right_movement(right, keys_pressed, paddle_vel)
        left_movement(left, keys_pressed, paddle_vel)
        
        if game_stop_timer < 0:
            ball_movement(ball_vel, left, right, ball_rect, ball_collision)
        
        draw_window(left,right, left_score, right_score, ball_rect, stop_text)


       
        if game_stop_timer == -5*FPS:
            if not max_speed:
                paddle_vel += 1

                if ball_vel[0] < 0:
                    ball_vel[0] -= 1
                else:
                    ball_vel[0] += 1
                
                if ball_vel[1] < 0:
                    ball_vel[1] -= 1
                else:
                    ball_vel[1] += 1
                
                print("speed increase = " + str(ball_vel))
                

                if ball_vel[0] >= MAX_BALL_VEL:
                    max_speed = True
            elif right.height > PADDLE_HEIGHT/2:
                right.height -= 10
                left.height -= 10
                paddle_vel += 1
                print("paddle size decreased = ", right.height, PADDLE_HEIGHT/2)
            game_stop_timer = -1

        if game_stop_timer < 0:
            stop_text = ""
        elif game_stop_timer < FPS:
            stop_text = "1"
        elif game_stop_timer < 2*FPS:
            stop_text = "2"
        elif game_stop_timer < 3*FPS:
            stop_text = "3"
            score_txt = ""
        elif game_stop_timer < 5*FPS:
            stop_text = score_txt
        
            
        game_stop_timer -= 1
        
    quit()
if __name__ == "__main__":
    main()