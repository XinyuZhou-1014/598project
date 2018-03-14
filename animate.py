import pygame
from pygame.locals import *
import sys
import math
import smooth

WIDTH = 800
HEIGHT = 600
FPS = 30  # seems useless
BACKGROUND_COLOR = (255, 255, 255)
POINT_COLOR = (0, 0, 127)
POINT_SIZE = 10
LINE_COLOR = (0, 0, 127)
LINE_WIDTH = 2


def draw_animate(skeleton, screen):
    for point in skeleton.points:
        pygame.draw.circle(screen, POINT_COLOR, point.pos, POINT_SIZE)

    for line in skeleton.animate_lines:
        pygame.draw.line(screen, LINE_COLOR, line[0].pos, line[1].pos, LINE_WIDTH)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)


skeleton_list = smooth.construct_skeleton_list(1)
y_axis = WIDTH  # set by video resolution


idx = 0
while True:
    pygame.display.update()
    screen.fill(BACKGROUND_COLOR)
    skeleton = skeleton_list[idx]
    idx += 1
    idx %= len(skeleton_list)
    draw_animate(skeleton, screen)

    event = pygame.event.poll()
    if event.type == QUIT:
        sys.exit()

