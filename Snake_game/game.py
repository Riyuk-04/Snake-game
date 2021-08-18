import sys, pygame
import random
import numpy as np
from time import sleep

pygame.init()

size = width, height = 1000, 900
speed = []
speed.append([0, 0])
snake_length = 1
score = 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)
pygame.display.set_caption("The Game Of Snakes")
font = pygame.font.Font("freesansbold.ttf", 30)

apple = pygame.image.load("apple.png")
snake = pygame.image.load("snake_head.png")
snake = pygame.transform.rotate(snake, -90)
temprect = snake.get_rect()
snakerect = []
snakerect.append(temprect)
applerect = apple.get_rect()
apple_eaten = True
gameover = False

img = pygame.Surface((20,20))

while 1:
    screen.fill(white)
    screen.blit(apple, applerect)
    if apple_eaten:
        x = random.randint(15,width - 15)
        y = random.randint(15,height - 15)
        applerect.center = x, y
        apple_eaten = False

    keys=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and speed[0][0] != 20:
                if speed[0][1] == 20:
                    snake = pygame.transform.rotate(snake, -90)
                elif speed[0][1] == -20:
                    snake = pygame.transform.rotate(snake, 90)
                speed[0] = [0, 0]
                speed[0][0] = -20
            elif event.key == pygame.K_RIGHT and speed[0][0] != -20:
                if speed[0][1] == 20:
                    snake = pygame.transform.rotate(snake, 90)
                elif speed[0][1] == -20:
                    snake = pygame.transform.rotate(snake, -90)
                speed[0] = [0, 0]
                speed[0][0] = 20
            elif event.key == pygame.K_UP and speed[0][1] != 20:
                if speed[0][0] == 20:
                    snake = pygame.transform.rotate(snake, 90)
                elif speed[0][0] == -20:
                    snake = pygame.transform.rotate(snake, -90)
                speed[0] = [0, 0]
                speed[0][1] = -20
            elif event.key == pygame.K_DOWN and speed[0][1] != -20:
                if speed[0][0] == 20:
                    snake = pygame.transform.rotate(snake, -90)
                elif speed[0][0] == -20:
                    snake = pygame.transform.rotate(snake, 90)
                speed[0] = [0, 0]
                speed[0][1] = 20

    a, b = snakerect[-1][0], snakerect[-1][1]
    av, bv = speed[-1] 
    for i in range(1,snake_length):
        snakerect[-i] = snakerect[-i].move(speed[-i])
        speed[-i] = speed[-i-1]
    snakerect[0] = snakerect[0].move(speed[0])

    if snakerect[0].colliderect(applerect):
        apple_eaten = True
        snake_length += 1
        temp = pygame.draw.rect(screen, (0, 255, 0), [a, b, snakerect[-1][2], snakerect[-1][3]])
        snakerect.append(temp)
        speed.append([av, bv])
        score += 1

    if snakerect[0].right > width or snakerect[0].left < 0 or snakerect[0].top < 0 or snakerect[0].bottom > height or snakerect[0].collidelist(snakerect[1:]) != -1:
        gameover = True
        snake_length = 1
        game_text = font.render("Game Over", True, (0, 0, 0))
        game_text_rect = game_text.get_rect()
        game_text_rect.center = (width/2, height/2)
        screen.blit(game_text, game_text_rect)
        score_text = font.render("Score: "+str(score), True, (0, 0, 0))
        screen.blit(score_text, [width - 200, 10])
        pygame.display.flip()
        sleep(10)
    
    screen.blit(snake, snakerect[0])
    for i in range(1,snake_length):
        screen.blit(img, snakerect[i])
    score_text = font.render("Score: "+str(score), True, (0, 0, 0))
    screen.blit(score_text, [width - 200, 10])
    pygame.display.flip()
    pygame.time.Clock().tick(20)
