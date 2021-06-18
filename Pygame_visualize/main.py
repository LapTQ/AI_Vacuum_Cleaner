import pygame
import numpy as np
import time
from constant import *
from Function import *


def draw_inital_state():
    global board

    for i in range(n):
        for j in range(m):
            x_, y_ = i * size_box, j * size_box
            if board[j, i] == 0:
                SCREEN.blit(floor, (x_, y_))
            elif board[j, i] == 1:
                SCREEN.blit(floor, (x_, y_))
                SCREEN.blit(dust, (x_, y_))
            elif board[j, i] == 2:
                SCREEN.blit(floor, (x_, y_))
                SCREEN.blit(jewel, (x_, y_))
            elif board[j, i] == 3:
                SCREEN.blit(floor, (x_, y_))
                SCREEN.blit(dust, (x_, y_))
                SCREEN.blit(jewel, (x_, y_))
            else:
                SCREEN.blit(floor, (x_, y_))
                SCREEN.blit(obstacle, (x_, y_))
    SCREEN.blit(chest, (0, 0))
    rect = pygame.Rect(y * size_box, x * size_box, size_box - 1, size_box - 1)
    pygame.draw.rect(SCREEN, RED, rect, 2)
    text = fnt.render('Planning..... ', 1, BLACK)
    SCREEN.blit(text, (0, m * size_box))
    pygame.display.update()


def draw_new_state(point0, point1):
    global handsfree, cost
    action = 'Moving'
    if isinstance(point1, str):
        if point1 == 'SuckDust':
            SCREEN.blit(floor, (point0[1] * size_box, point0[0] * size_box))
            rect_vaccum = pygame.Rect(point0[1] * size_box + size_box // 4, point0[0] * size_box + size_box // 4,
                                      size_box // 2, size_box // 2)
            pygame.draw.rect(SCREEN, RED, rect_vaccum, 2)
            action = 'SuckDust'
        elif point1 == 'PickUp':
            if board[point0[0], point0[1]] == 0:
                SCREEN.blit(floor, (point0[1] * size_box, point0[0] * size_box))
            elif board[point0[0], point0[1]] == 1:
                SCREEN.blit(floor, (point0[1] * size_box, point0[0] * size_box))
                SCREEN.blit(dust, (point0[1] * size_box, point0[0] * size_box))
            pygame.draw.circle(SCREEN, RED,
                               (point0[1] * size_box + size_box // 2, point0[0] * size_box + size_box // 2),
                               size_box // 3, 2)
            handsfree = False
            action = 'PickUp'
        elif point1 == 'PutDown':
            SCREEN.blit(floor, (point0[1] * size_box, point0[0] * size_box))
            SCREEN.blit(chest, (point0[1] * size_box, point0[0] * size_box))

            rect_vaccum = pygame.Rect(point0[1] * size_box + size_box // 4, point0[0] * size_box + size_box // 4,
                                      size_box // 2, size_box // 2)
            pygame.draw.rect(SCREEN, RED, rect_vaccum, 2)
            handsfree = True
            action = 'PutDown'
    else:
        if board[point0[0], point0[1]] == 0:
            SCREEN.blit(floor, (point0[1] * size_box, point0[0] * size_box))
        elif board[point0[0], point0[1]] == 1:
            SCREEN.blit(floor, (point0[1] * size_box, point0[0] * size_box))
            SCREEN.blit(dust, (point0[1] * size_box, point0[0] * size_box))
        elif board[point0[0], point0[1]] == 2:
            SCREEN.blit(floor, (point0[1] * size_box, point0[0] * size_box))
            SCREEN.blit(jewel, (point0[1] * size_box, point0[0] * size_box))
        elif board[point0[0], point0[1]] == 3:
            SCREEN.blit(floor, (point0[1] * size_box, point0[0] * size_box))
            SCREEN.blit(dust, (point0[1] * size_box, point0[0] * size_box))
            SCREEN.blit(jewel, (point0[1] * size_box, point0[0] * size_box))
        if handsfree:
            rect_vaccum = pygame.Rect(point1[1] * size_box, point1[0] * size_box, size_box - 1, size_box - 1)
            pygame.draw.rect(SCREEN, RED, rect_vaccum, 2)
        else:
            pygame.draw.circle(SCREEN, RED,
                               (point1[1] * size_box + size_box // 2, point1[0] * size_box + size_box // 2),
                               size_box // 2 - 1, 2)
    if point0 == [0, 0]:
        SCREEN.blit(chest, (0, 0))
    rect = pygame.Rect(0, m * size_box, WINDOW_WIDTH - text_time.get_width() - 15, 80)
    pygame.draw.rect(SCREEN, WHITE, rect)
    text_action = fnt.render(f'Action: {action}', 1, BLACK)
    SCREEN.blit(text_action, (0, m * size_box))
    if handsfree:
        text_hand = fnt.render('Hold a jewel?: No', 1, BLACK)
        SCREEN.blit(text_hand, (0, m * size_box + text_action.get_height()))
    else:
        text_hand = fnt.render('Hold a jewel?: Yes', 1, BLACK)
        SCREEN.blit(text_hand, (0, m * size_box + text_action.get_height()))
    if point0 != point1:
        cost += 1
    text_cost = fnt.render(f'Cost: {cost}', 1, BLACK)
    SCREEN.blit(text_cost, (0, m * size_box + text_action.get_height() + text_hand.get_height()))
    pygame.display.update()


def animation():
    rect = pygame.Rect(0, m * size_box, WINDOW_WIDTH, 80)
    pygame.draw.rect(SCREEN, WHITE, rect)
    text_time = fnt.render(f'Planning time:{round(end_planning, 2)} s', 1, BLACK)
    SCREEN.blit(text_time, (0, m * size_box))
    current = 0
    speed = 0

    while current < WINDOW_WIDTH - text_time.get_width():
        rect = pygame.Rect(0, m * size_box, WINDOW_WIDTH, 80)
        pygame.draw.rect(SCREEN, WHITE, rect)
        SCREEN.blit(text_time, (current, m * size_box))
        CLOCK.tick(90)
        speed += 0.5
        current += speed
        pygame.display.update()

    text_action = fnt.render(f'Action: ... ', 1, BLACK)
    SCREEN.blit(text_action, (0, m * size_box))

    text_hand = fnt.render('Hold a jewel?: ...', 1, BLACK)
    SCREEN.blit(text_hand, (0, m * size_box + text_action.get_height()))

    text_cost = fnt.render(f'Cost: ...', 1, BLACK)
    SCREEN.blit(text_cost, (0, m * size_box + text_action.get_height() + text_hand.get_height()))
    pygame.display.update()
    CLOCK.tick(1)


pygame.font.init()
pygame.init()

# get and prepare data
icon = pygame.image.load('Image/icon.png')
floor = pygame.transform.scale(pygame.image.load('Image/floor.png'), (size_box, size_box))
dust = pygame.transform.scale(pygame.image.load('Image/dust.png'), (size_box, size_box))
jewel = pygame.transform.scale(pygame.image.load('Image/jewel.png'), (size_box, size_box))
obstacle = pygame.transform.scale(pygame.image.load('Image/ostacle.png'), (size_box, size_box))
chest = pygame.transform.scale(pygame.image.load('Image/chest.png'), (size_box, size_box))
fnt = pygame.font.SysFont("consolas", 20)

# create client object
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Intelligent Vacuum Cleaner')
pygame.display.set_icon(icon)
SCREEN.fill(WHITE)

# create instance
start = time.time()
board, x, y = create_data(m, n)

draw_inital_state()

# Planning
matrix, path = floyd_warshall(board)
pygame.display.set_caption('Intelligent Vacuum Cleaner (Ready to run)')
end_planning = time.time() - start
rect = pygame.Rect(0, m * size_box, WINDOW_WIDTH, 80)
pygame.draw.rect(SCREEN, WHITE, rect)
text_time = fnt.render(f'Planning time:{round(end_planning, 2)} s', 1, BLACK)
SCREEN.blit(text_time, (0, m * size_box))
text_guide = fnt.render(f'Press Space to run the cleaner', 1, BLACK)
SCREEN.blit(text_guide, (0, m * size_box + text_time.get_height()))
pygame.display.update()

# Run the cleaner
q = False
while not q:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            q = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.display.set_caption('Intelligent Vacuum Cleaner (Running)')
                animation()
                cost = 0
                status = True
                handsfree = True
                while status:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            q = True

                    old_point = [x, y]
                    x, y, route = f(board, path, x, y, [])
                    route = simplify_route(route)

                    for point in route:
                        CLOCK.tick(FPS)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()

                        draw_new_state(old_point, point)
                        if not isinstance(point, str):
                            old_point = point

                    if check(board):
                        fnt = pygame.font.SysFont("consolas", 60)
                        text = fnt.render('MISSION COMPLETED', 5, BLUE, WHITE)
                        SCREEN.blit(text,
                                    (20, m * size_box // 2 - text.get_height() // 2))
                        pygame.display.update()
                        status = False

                pygame.display.set_caption('Intelligent Vacuum Cleaner (Finished)')
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            q = True
