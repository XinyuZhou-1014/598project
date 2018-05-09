import pygame
from pygame.locals import *
import sys
import skeleton as sk
import argparse
from numpy import array
from math_functions import rotation_matrix


WIDTH = 800
HEIGHT = 800
FPS = 60
BLACK = (0, 0, 0)
RED = (255, 128, 128)
BLUE = (128, 128, 255)
GREY = (127, 127, 127)

# animate factors
BACKGROUND_COLOR = BLACK
POINT_COLOR = RED
POINT_SIZE = 6
LINE_COLOR = BLUE
LINE_WIDTH = 4
FONT = "arial"
FONT_SIZE = 24
FONT_COLOR = GREY

# fit coordinate to screen
FIT_FUNC = lambda coordinate, frame: 4 * coordinate + frame / 2 - 200


parser = argparse.ArgumentParser()
parser.add_argument('filepath', type=str,
                    help='the dir of the json files')
parser.add_argument('-s', '--smooth', type=int, default=1,
                    help="smooth factor")
parser.add_argument('--skip', type=int, default=1,
                    help="skip factor")
parser.add_argument('--scale', type=float, default=0.1,
                    help="scale factor")


args = parser.parse_args()
path = args.filepath
smooth_factor = args.smooth
skip_factor = args.skip
scale_factor = args.scale


class Physical:
    __rotation = [0, 0, 0]  # radians around each axis

    def __init__(self, vertices, edges):
        """
        a 3D object that can rotate around the three axes
        :param vertices: a tuple of points (each has 3 coordinates)
        :param edges: a tuple of pairs (each pair is a set containing
                      2 vertices' indexes)
        """
        self.__vertices = array(vertices)
        self.__edges = tuple(edges)

    @classmethod
    def rotate(cls, axis, theta):
        axis_idx = {"X": 0, "Y": 1, "Z": 2}
        cls.__rotation[axis_idx[axis]] += theta

    @property
    def lines(self):
        location = self.__vertices.dot(rotation_matrix(*self.__rotation))
        # an index->location mapping
        return ((location[v1], location[v2]) for v1, v2 in self.__edges)

    @classmethod
    def get_rotation(cls):
        return tuple(cls.__rotation)

    @classmethod
    def reset_rotation(cls):
        cls.__rotation = [0, 0, 0]


class Paint:
    def __init__(self, skeleton_list, font):
        self.__font = font
        s_list = skeleton_list
        self._shapelist = []

        s_list[0].points_to_3d(s_list[0])
        init_head_pos = s_list[0].animate_points[0]
        x = init_head_pos.x * scale_factor - 110
        y = init_head_pos.y * scale_factor - 25
        z = init_head_pos.z * scale_factor
        self.ax_val_adjust = [x, y, z]
        self.user_ax_adjust = [0, 0]

        for skeleton in s_list:
            skeleton.points_to_3d(s_list[0])
            v_list = []
            for point in skeleton.animate_points:
                # multiply by scale_factor to fit the obejct into screen
                v_list.append((point.x * scale_factor - 65,  
                               # mystery value for rotate axis adjust 
                               point.y * scale_factor,
                               point.z * scale_factor))

            self._shapelist.append(Physical(
                vertices=v_list,
                edges=({0, 1}, {1, 2}, {2, 3}, {3, 4},
                       {1, 5}, {5, 6}, {6, 7}, {1, 8},
                       {8, 9}, {9, 10}, {1, 11}, {11, 12}, {12, 13})))

        self.__size = WIDTH, HEIGHT
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode(self.__size)
        self._idx = 0
        self.__mainloop()

    def __fit(self, vec):
        """
        ignore the z-element (creating a very cheap projection),
        and scale x, y to the coordinates of the screen
        """
        # change the coordinate to be fit into screen
        return [int(FIT_FUNC(coordinate, frame))
                for coordinate, frame in zip(vec, self.__size)]

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        self._keys_handler(pygame.key.get_pressed())

    def _keys_handler(self, keys):
        counter_clockwise = 0.05  # radians
        clockwise = -counter_clockwise
        rotate_handle_params = {
            K_q: ("X", counter_clockwise),
            K_w: ("X", clockwise),
            K_a: ("Y", counter_clockwise),
            K_s: ("Y", clockwise),
            K_z: ("Z", clockwise),
            K_x: ("Z", counter_clockwise),
        }
        for key in rotate_handle_params:
            if keys[key]:
                Physical.rotate(*rotate_handle_params[key])
            if keys[K_r]:
                Physical.reset_rotation()
                self.user_ax_adjust = [0, 0]
            if keys[K_SPACE]:
                Physical.reset_rotation()
                self._idx = -1
                self._updateshape()
                self.user_ax_adjust = [0, 0]
        
        MOVE = 5
        display_adjust_params = {
            K_UP: [0, -MOVE], 
            K_DOWN: [0, MOVE], 
            K_LEFT: [-MOVE, 0], 
            K_RIGHT: [MOVE, 0] 
        }
        for key in display_adjust_params:
            if keys[key]:
                x, y = display_adjust_params[key]
                self.user_ax_adjust = [self.user_ax_adjust[0] + x, 
                                       self.user_ax_adjust[1] + y]

    def __draw_shape(self, point_size=POINT_SIZE, line_width=LINE_WIDTH):
        for start, end in self.__shape.lines:
            # number to fit into the screen
            # hardcode for display position adjust
            new_start = [0, 0, 0]
            new_end = [0, 0, 0]
            new_start[0] = start[0] - self.ax_val_adjust[0] + self.user_ax_adjust[0]
            new_start[1] = start[1] - self.ax_val_adjust[1] + self.user_ax_adjust[1]
            new_start[2] = start[2] - self.ax_val_adjust[2]
            new_end[0] = end[0] - self.ax_val_adjust[0] + self.user_ax_adjust[0]
            new_end[1] = end[1] - self.ax_val_adjust[1] + self.user_ax_adjust[1]
            new_end[2] = end[2] - self.ax_val_adjust[2] 

            pygame.draw.line(self.__screen,
                             LINE_COLOR,
                             self.__fit(new_start),
                             self.__fit(new_end),
                             line_width)
            pygame.draw.circle(self.__screen,
                               POINT_COLOR,
                               self.__fit(new_start),
                               point_size)
            pygame.draw.circle(self.__screen,
                               POINT_COLOR,
                               self.__fit(new_end),
                               point_size)
            # TODO: some repeated points

    def _updateshape(self):
        self._idx += 1
        self._idx %= len(self._shapelist)
        self.__shape = self._shapelist[self._idx]

    def __draw_text(self):
        rotation_text = "X:{:6.2f}, Y:{:6.2f}, Z:{:6.2f}".format(
            *Physical.get_rotation())
        rotation_text_surface = self.__font.render(
            rotation_text, True, FONT_COLOR)
        self.__screen.blit(rotation_text_surface, (0, 0))
        frame_text = "{}/{}".format(self._idx, len(self._shapelist))
        frame_text_surface = self.__font.render(
            frame_text, True, FONT_COLOR)
        self.__screen.blit(frame_text_surface, (0, FONT_SIZE))

    def __mainloop(self):
        while True:
            self._updateshape()
            self.__handle_events()
            self.__screen.fill(BACKGROUND_COLOR)
            self.__draw_shape()
            self.__draw_text()
            pygame.display.update()
            self.__clock.tick(FPS)


def main():
    skeleton_list = sk.create_skeleton_list(
        path, smooth_factor, skip_factor)
    pygame.init()
    caption = "Control - q, w: X; a, s: Y; z, x: Z, r: Reset, space: Restart"
    pygame.display.set_caption(caption)
    my_font = pygame.font.SysFont(FONT, FONT_SIZE)
    Paint(skeleton_list, my_font)


if __name__ == '__main__':
    main()
