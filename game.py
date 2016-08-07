__author__ = 'Raghava'
import pygame
from pygame.locals import *
from sys import exit
import random

data = open("data.bin", 'a')
data.close()
pygame.init()
SCREEN_SIZE = (800, 600)
Display_Size = (1000, 600)
font = pygame.font.SysFont("arial", 24)
font_height = font.get_linesize()
GameDisplay = pygame.display.set_mode(Display_Size, DOUBLEBUF, 32)
pygame.display.set_caption("Snake")
Play_color = (255, 0, 0)
background = 'bg.jpg'
bg = pygame.image.load(background).convert_alpha()
eat = pygame.mixer.Sound("eat.wav")
def get_apple(snake_rect):
    apple_x = random.randrange(4, SCREEN_SIZE[0]-4, 1)
    apple_y = random.randrange(4, SCREEN_SIZE[1]-4, 1)
    while pygame.Rect((apple_x - 5, apple_y - 5), (10, 10)).collidelist(snake_rect)!=-1:
        apple_x = random.randrange(4, SCREEN_SIZE[0]-4, 1)
        apple_y = random.randrange(4, SCREEN_SIZE[1]-4, 1)
    return (apple_x,apple_y)
def game_loop():
    data = open("data.bin", 'rb')
    strg = data.read().decode('base64','strict')
    data.close()
    high_score = 0
    if strg.isdigit():
        high_score = int(strg)
    (x, y) = (0, 0)
    coordinate = [(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)]
    snake_rect = [pygame.Rect((coordinate[0][0] - 5, coordinate[0][1] - 5), (10, 10))]
    score = 0
    for i in range(1, 30):
        coordinate += [(SCREEN_SIZE[0] / 2 - i * 5, SCREEN_SIZE[1] / 2)]
        snake_rect += [pygame.Rect((coordinate[i][0] - 5, coordinate[i][1] - 5), (10, 10))]
    flag = 0
    (apple_x,apple_y)=get_apple(snake_rect)
    apple_rect = pygame.Rect((apple_x - 5, apple_y - 5), (10, 10))
    prev_event_type=KEYUP
    while True:
        pygame.time.delay(10)
        for event in pygame.event.get():

            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                flag = 1
                if event.key == K_LEFT:
                    if x == 0:
                        x = -5
                        y = 0
                elif event.key == K_RIGHT:
                    if x == 0:
                        x = 5
                        y = 0
                elif event.key == K_UP:
                    if y == 0:
                        y = -5
                        x = 0
                elif event.key == K_DOWN:
                    if y == 0:
                        y = 5
                        x = 0
                else:
                    x = 0
                    y = 0
                    flag = 0

        if apple_rect.colliderect(snake_rect[0]):
            if eat.get_num_channels() != 0:
                eat.stop()
            eat.play(0, 1000)
            (apple_x,apple_y)=get_apple(snake_rect)
            score += 5
            for i in range(0, 6):
                coordinate += [coordinate[len(coordinate) - 1]]
                snake_rect += [snake_rect[len(snake_rect) - 1]]
        for i in snake_rect[7:]:
            if i.colliderect(snake_rect[0]):
                GameDisplay.blit(font.render("Gameover!!", True, (255, 255, 255)),
                                 (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))
                pygame.display.update()
                g = pygame.event.poll()
                while g.type != KEYDOWN:
                    if g.type==QUIT:
                        exit()
                    g = pygame.event.poll()
                data = open("data.bin", 'wb')
                data.write(str(high_score).encode('base64','strict'))
                data.close()
                return
        if flag != 0:
            for i in range(len(coordinate) - 1, 0, -1):
                coordinate[i] = coordinate[i - 1]
                snake_rect[i] = snake_rect[i - 1]

        coordinate[0] = (coordinate[0][0] + x, coordinate[0][1] + y)
        coordinate[0] = (coordinate[0][0] % SCREEN_SIZE[0], coordinate[0][1] % SCREEN_SIZE[1])
        GameDisplay.fill((47, 159, 39))
        pygame.draw.line(GameDisplay, (255, 255, 255), (SCREEN_SIZE[0] + 1, 0), (SCREEN_SIZE[0] + 1, Display_Size[1]), 10)
        GameDisplay.blit(font.render("Score:{0}".format(score), True, (255, 255, 255)), (SCREEN_SIZE[0] + 20, 50))
        GameDisplay.blit(font.render("Highest:{0}".format(high_score), True, (255, 255, 255)), (SCREEN_SIZE[0] + 20, 150))
        apple_rect = pygame.draw.circle(GameDisplay, (24, 16, 179), (apple_x, apple_y), 8, 0)
        snake_rect[0] = pygame.draw.circle(GameDisplay, (255, 0, 0), coordinate[0], 3, 0)
        for i in range(1, len(coordinate) - 1):
            if i == 3:
                snake_rect[i] = pygame.draw.circle(GameDisplay, (0,0,0),
                                                   coordinate[i], 10, 0)
            else:
                snake_rect[i] = pygame.draw.circle(GameDisplay, (abs(255 - 25 * i) % 255, 0, 0),
                                                   coordinate[i], 7, 0)

        pygame.display.flip()
        if score > high_score:
            high_score = score


def menu_loop():
    pos=0
    play_rect = pygame.Rect((SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2), (50, 50))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEMOTION:
                if play_rect.collidepoint(event.pos):

                    globals()["Play_color"] = (0, 255, 0)
                else:
                    globals()["Play_color"] = (255, 0, 0)
            elif event.type == MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    game_loop()
            elif event.type == KEYDOWN:
                if event.key ==K_DOWN or event.key==K_UP:
                    globals()["Play_color"] = (0, 255, 0)
                    pos=1
                if event.key==K_RETURN and pos==1:
                    game_loop()
        GameDisplay.fill((0,0,0))
        GameDisplay.blit(bg,(0,0))
        play_rect = pygame.draw.rect(GameDisplay, Play_color,
                                     (Display_Size[0] / 2 - 50, Display_Size[1] / 2 - 25, 100, 50), 0)
        GameDisplay.blit(font.render("PLAY", True, (0, 0, 0)),
                         ((Display_Size[0] - font.size("PLAY")[0]) / 2, (Display_Size[1] - font.size("PLAY")[1]) / 2))
        pygame.display.update()


menu_loop()