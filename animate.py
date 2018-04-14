import pygame
from pygame.locals import *
import sys
import math
import smooth
import argparse
import pygame
from numpy import array
from math import cos, sin
from pygame import K_q, K_w, K_a, K_s, K_z, K_x



WIDTH = 800
HEIGHT = 800
FPS = 30  # seems useless
BACKGROUND_COLOR = (255, 255, 255)
POINT_COLOR = (0, 150, 200)
POINT_SIZE = 8
LINE_COLOR = (0, 150, 200)
LINE_WIDTH = 4
BLACK, RED,BLUE = (0, 0, 0), (255, 128, 128), (128,255,128)
X, Y, Z = 0, 1, 2

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


def rotation_matrix(α, β, γ):
    """
    rotation matrix of α, β, γ radians around x, y, z axes (respectively)
    """
    sα, cα = sin(α), cos(α)
    sβ, cβ = sin(β), cos(β)
    sγ, cγ = sin(γ), cos(γ)
    return (
        (cβ*cγ, -cβ*sγ, sβ),
        (cα*sγ + sα*sβ*cγ, cα*cγ - sγ*sα*sβ, -cβ*sα),
        (sγ*sα - cα*sβ*cγ, cα*sγ*sβ + sα*cγ, cα*cβ)
    )


class Physical:
    def __init__(self, vertices, edges):
        """
        a 3D object that can rotate around the three axes
        :param vertices: a tuple of points (each has 3 coordinates)
        :param edges: a tuple of pairs (each pair is a set containing 2 vertices' indexes)
        """
        self.__vertices = array(vertices)
        self.__edges = tuple(edges)
        self.__rotation = [0, 0, 0]  # radians around each axis

    def rotate(self, axis, θ):
        self.__rotation[axis] += θ

    @property
    def lines(self):
        location = self.__vertices.dot(rotation_matrix(*self.__rotation))  # an index->location mapping
        return ((location[v1], location[v2]) for v1, v2 in self.__edges)

class Paint:
    def __init__(self,skeleton_list):
        self._s_list = skeleton_list
        self._shapelist = []
        #self.__shape = shape
        for skeleton in self._s_list:
            skeleton.points_to_3d(self._s_list[0])
            v_list = []
            for point in skeleton.animate_points:
                #divide by 10 to fit the obejct into screen
                v_list.append((point.pos[0] / 10, point.pos[1] / 10, point.z / 10))

            self._shapelist.append(Physical(
                vertices=v_list,
                edges=({0, 1}, {1, 2}, {2, 3}, {3, 4},
                       {1, 5}, {5, 6}, {6, 7}, {1, 8},
                       {8, 9}, {9, 10}, {1, 11}, {11, 12}, {12, 13})))

        self.__size = 1000, 1000
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode(self.__size)
        self._idx = 0
        self.__mainloop()

    def __fit(self, vec):
        """
        ignore the z-element (creating a very cheap projection), and scale x, y to the coordinates of the screen
        """
        # change the coordinate to be fit into screen
        return [round(5 * coordinate + frame/2 -200) for coordinate, frame in zip(vec, self.__size)]

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        self._keys_handler(pygame.key.get_pressed())

    def _keys_handler(self, keys):
        counter_clockwise = 0.05  # radians
        clockwise = -counter_clockwise
        params = {
            K_q: (X, clockwise),
            K_w: (X, counter_clockwise),
            K_a: (Y, clockwise),
            K_s: (Y, counter_clockwise),
            K_z: (Z, clockwise),
            K_x: (Z, counter_clockwise),
        }
        for key in params:
            if keys[key]:
                for i in range(self._idx, len(self._shapelist)):

                    self._shapelist[i].rotate(*params[key])

    def __draw_shape(self, thickness=4):
        for start, end in self.__shape.lines:
            #number to fit into the screen
            pygame.draw.circle(self.__screen, BLUE, (int(5 *start[0]+ 1000/2 -200), int(5 *start[1] + 1000/2)- 200), thickness+2)
        for start, end in self.__shape.lines:
            pygame.draw.line(self.__screen, RED, self.__fit(start), self.__fit(end), thickness)

    def _updateshape(self):

        self._idx += 1

        if self._idx >= len(self._s_list):
            sys.exit()

        self._idx %= len(self._s_list)
        self.__shape = self._shapelist[self._idx]

    def __mainloop(self):
        while True:
            self._updateshape()
            self.__handle_events()
            self.__screen.fill(BLACK)
            self.__draw_shape()
            pygame.display.flip()
            self.__clock.tick(40)



def main():

    skeleton_list = smooth.construct_skeleton_list(path, smooth_factor, skip_factor)
    pygame.init()
    pygame.display.set_caption('Control -   q,w : X    a,s : Y    z,x : Z')
    Paint(skeleton_list[1:])

if __name__ == '__main__':
    main()
