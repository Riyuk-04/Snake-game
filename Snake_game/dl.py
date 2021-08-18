import sys, pygame
import random
import numpy as np
from time import sleep
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
#from network import Net

alpha = 1
beta = 1500         #Cost Function = -Score*alpha + dist()/beta

pygame.init()

size = width, height = 1000, 900
white = 255, 255, 255

screen = pygame.display.set_mode(size)
pygame.display.set_caption("The Game Of Snakes")
font = pygame.font.Font("freesansbold.ttf", 30)
gameover = True
img = pygame.Surface((20,20))
snake_length = 1

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device
#net = Net()
#net.to(device)
#optimizer = optim.SGD(net.parameters(), lr=0.2, momentum=0.01)
#criterion = nn.CrossEntropyLoss()

def arr_to_direct(NN_Output):
    index = np.argmax(NN_Output)
    #index = random.randint(0, 4)
    if index == 0:
        return "Left"
    if index == 1:
        return "Right"
    if index == 2:
        return "Up"
    if index == 3:
        return "Down"
    if index == 4:
        return "None"

def update_rects(snakerect, snake, speed, NN_Output, snake_length):
    direction = arr_to_direct(NN_Output)
    #print(direction)

    if direction == "Left" and speed[0][0] != 20:
        if speed[0][1] == 20:
            snake = pygame.transform.rotate(snake, -90)
        elif speed[0][1] == -20:
            snake = pygame.transform.rotate(snake, 90)
        speed[0] = [0, 0]
        speed[0][0] = -20
    elif direction == "Right" and speed[0][0] != -20:
        if speed[0][1] == 20:
            snake = pygame.transform.rotate(snake, 90)
        elif speed[0][1] == -20:
            snake = pygame.transform.rotate(snake, -90)
        speed[0] = [0, 0]
        speed[0][0] = 20
    elif direction == "Up" and speed[0][1] != 20:
        if speed[0][0] == 20:
            snake = pygame.transform.rotate(snake, 90)
        elif speed[0][0] == -20:
            snake = pygame.transform.rotate(snake, -90)
        speed[0] = [0, 0]
        speed[0][1] = -20
    elif direction == "Down" and speed[0][1] != -20:
        if speed[0][0] == 20:
            snake = pygame.transform.rotate(snake, -90)
        elif speed[0][0] == -20:
            snake = pygame.transform.rotate(snake, 90)
        speed[0] = [0, 0]
        speed[0][1] = 20

    for i in range(1,snake_length):
        snakerect[-i] = snakerect[-i].move(speed[-i])
        speed[-i] = speed[-i-1]
    snakerect[0] = snakerect[0].move(speed[0])

    return snakerect, snake, speed 

def costfunc(score, applerect, headrect):
    dist = np.sqrt((headrect.center[0] - applerect.center[0])**2 + (headrect.center[1] - applerect.center[1])**2)
    return -alpha*score + dist/beta
    

while snake_length < 50:
    if gameover:
        apple = pygame.image.load("apple.png")
        snake = pygame.image.load("snake_head.png")
        snake = pygame.transform.rotate(snake, -90)
        temprect = snake.get_rect()
        snakerect = []
        snakerect.append(temprect)
        snake_length = 1
        speed = []
        speed.append([0, 0])
        score = 1
        applerect = apple.get_rect()
        apple_eaten = True
        gameover = False
        NN_Output = [0, 1, 0, 0, 0]

    screen.fill(white)

    if apple_eaten:
        x = random.randint(15,width - 15)
        y = random.randint(15,height - 15)
        applerect.center = x, y
        apple_eaten = False
    screen.blit(apple, applerect)

    snakerect, snake, speed = update_rects(snakerect, snake, speed, NN_Output, snake_length)

    a, b = snakerect[-1][0], snakerect[-1][1]
    av, bv = speed[-1]
    if snakerect[0].colliderect(applerect):
        apple_eaten = True
        snake_length += 1
        temp = pygame.draw.rect(screen, (0, 255, 0), [a, b, snakerect[-1][2], snakerect[-1][3]])
        snakerect.append(temp)
        speed.append([av, bv])
        score += 1

    snakerect_np = np.concatenate((snakerect, np.zeros([50-np.shape(snakerect)[0], 4])), axis = 0)
    speed_np = np.concatenate((speed, np.zeros([50-np.shape(speed)[0], 2])), axis = 0)
    speed_np = np.concatenate((speed_np, np.zeros([50, 2])), axis = 1)
    train_mat = np.concatenate((snakerect_np, speed_np, np.array(applerect).reshape(1,4), np.array(screen.get_rect()).reshape(1,4)), axis = 0)
    train_mat_tensor = torch.from_numpy(train_mat)

    max_cost = 0
    for i in range(5):
        arr = [0, 0, 0, 0, 0]
        arr[i] = 1
        snakerect_temp, snake_temp, speed_temp = update_rects(snakerect, snake, speed, arr, snake_length)
        cost = costfunc(score, applerect, snakerect_temp[0])

    if snakerect[0].right > width or snakerect[0].left < 0 or snakerect[0].top < 0 or snakerect[0].bottom > height or snakerect[0].collidelist(snakerect[1:]) != -1:
        gameover = True
    
    screen.blit(snake, snakerect[0])
    for i in range(1,snake_length):
        screen.blit(img, snakerect[i])
    score_text = font.render("Score: "+str(score), True, (0, 0, 0))
    screen.blit(score_text, [width - 200, 10])
    pygame.display.flip()
    pygame.time.Clock().tick(20)
