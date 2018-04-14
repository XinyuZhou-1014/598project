import pygame
from pygame.locals import *
import sys
import math
import smooth
import argparse


WIDTH = 800
HEIGHT = 800
FPS = 30  # seems useless
BACKGROUND_COLOR = (255, 255, 255)
POINT_COLOR = (0, 150, 200)
POINT_SIZE = 8
LINE_COLOR = (0, 150, 200)
LINE_WIDTH = 4

parser = argparse.ArgumentParser()
parser.add_argument('filepath', type=str,
                    help='the dir of the json files')
parser.add_argument('-s', '--smooth', type=int, default=1,
                    help="smooth factor")
parser.add_argument('--skip', type=int, default=1,
                    help="skip factor")
parser.add_argument('--scale', type=float, default=1.0,
                    help="scale factor")
parser.add_argument('-z', "--z_axis", default=False, action="store_true",
                    help="if true, to z axis")


args = parser.parse_args()
path = args.filepath
smooth_factor = args.smooth
skip_factor = args.skip
scale_factor = args.scale
to_z_axis = args.z_axis

def draw_animate(skeleton, screen, scale_factor=1.0):
    for point in skeleton.animate_points:
        x, y = point.pos
        x = int(x * scale_factor)
        y = int(y * scale_factor)
        pygame.draw.circle(screen, POINT_COLOR, (x, y), POINT_SIZE)

    for line in skeleton.animate_lines:
        x1, y1 = line[0].pos
        x2, y2 = line[1].pos
        x1 = int(x1 * scale_factor)
        x2 = int(x2 * scale_factor)
        y1 = int(y1 * scale_factor)
        y2 = int(y2 * scale_factor)
        pygame.draw.line(screen, LINE_COLOR, (x1, y1), (x2, y2), LINE_WIDTH)


def draw_animate_3d(skeleton, standard_skeleton, screen, scale_factor=1.0):
    skeleton.points_to_3d(standard_skeleton)
    #print(skeleton.animate_points)
    for point in skeleton.animate_points:
        x, y = point.pos
        z = point.z
        print(z)
        if to_z_axis:
            z, x = x, z
            x += 200
        x = int(x * scale_factor)
        y = int(y * scale_factor)
        #adjust_point_size = int(POINT_SIZE * (1 + z / 400))
        adjust_point_size = POINT_SIZE
        color_change = 0
        adjust_point_color = list(POINT_COLOR)
        adjust_point_color[1] = int(POINT_COLOR[1] + color_change)
        pygame.draw.circle(screen, adjust_point_color, (x, y), adjust_point_size)

    for line in skeleton.animate_lines:
        x1, y1 = line[0].x, line[0].y
        x2, y2 = line[1].x, line[1].y
        if to_z_axis:
            x1 = line[0].z + 200
            x2 = line[1].z + 200

        x1 = int(x1 * scale_factor)
        x2 = int(x2 * scale_factor)
        y1 = int(y1 * scale_factor)
        y2 = int(y2 * scale_factor)
        pygame.draw.line(screen, LINE_COLOR, (x1, y1), (x2, y2), LINE_WIDTH)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)


skeleton_list = smooth.construct_skeleton_list(path, smooth_factor, skip_factor)
y_axis = WIDTH  # set by video resolution



idx = 0
while True:
    pygame.display.update()
    screen.fill(BACKGROUND_COLOR)
    skeleton = skeleton_list[idx]
    idx += 1
    idx %= len(skeleton_list)
    # draw_animate(skeleton, screen, scale_factor)

    draw_animate_3d(skeleton, skeleton_list[0], screen, scale_factor)

    event = pygame.event.poll()
    if event.type == QUIT:
        sys.exit()