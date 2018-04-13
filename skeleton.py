import numpy as np
import math
import math_functions


idx_body = {
    0: 'Nose',
    1: 'Neck',
    2: 'RShoulder',
    3: 'RElbow',
    4: 'RWrist',
    5: 'LShoulder',
    6: 'LElbow',
    7: 'LWrist',
    8: 'RHip',
    9: 'RKnee',
    10: 'RAnkle',
    11: 'LHip',
    12: 'LKnee',
    13: 'LAnkle',
    14: 'REye',
    15: 'LEye',
    16: 'REar',
    17: 'LEar'
}

body_idx = {val: key for key, val in idx_body.items()}


class Point():
    def __init__(self, x, y, conf, idx, z=0):
        # args: x, y, confidence
        self.x, self.y, self.conf = x, y, conf
        self.z = z
        self.idx = idx
        self.part = idx_body[idx]

    def __str__(self):
        return "({}, {}, {}, {}, {})".format(
            self.idx, self.x, self.y, self.z, self.conf)

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x == other.x and
                    self.y == other.y and
                    self.conf == other.conf and
                    self.idx == other.idx and
                    self.z == other.z)
        return False

    @property
    def pos(self):
        return self.x, self.y

    def distance_2d(self, other):
        return math.sqrt((self.x - other.x) ** 2 +
                         (self.y - other.y) ** 2)

    def distance_3d(self, other):
        return math.sqrt((self.x - other.x) ** 2 +
                         (self.y - other.y) ** 2 +
                         (self.z - other.z) ** 2)


class Skeleton():
    def __init__(self, keypoint_list):
        self.points = []
        assert len(keypoint_list) in [54, 18], "Wrong length on keypoint list"
        for idx in range(18):
            if len(keypoint_list) == 54:
                x, y, conf = keypoint_list[idx*3:idx*3+3]
            elif len(keypoint_list) == 18:
                x, y, conf = keypoint_list[idx]
            point_3d = Point(x, y, conf, idx)
            self.points.append(point_3d)
        self.points = np.array(self.points)

    def __str__(self):
        return "\n".join([str(x) for x in self.points])

    @property
    def plot_points(self, dim=2):
        mask = [0, 1, 2, 3, 4,
                3, 2, 1,
                5, 6, 7,
                6, 5, 1,
                8, 9, 10,
                9, 8, 1,
                11, 12, 13]
        mask = self.mask_filter(mask, dim=1)
        points = self.points[mask]
        return [p.x for p in points], [p.y for p in points]

    @property
    def animate_points(self):
        mask = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        mask = self.mask_filter(mask, dim=1)
        return self.points[mask]

    @property
    def animate_lines(self):
        mask = [(0, 1), (1, 2), (2, 3), (3, 4),
                (1, 5), (5, 6), (6, 7),
                (1, 8), (8, 9), (9, 10),
                (1, 11), (11, 12), (12, 13)]
        mask = self.mask_filter(mask, dim=2)
        lines = [(self.points[i], self.points[j]) for i, j in mask]
        return lines

    def mask_filter(self, mask, dim):
        return mask  # TODO

    def distance_2d(self, idx_1, idx_2):
        return self.points[idx_1].distance_2d(self.points[idx_2])

    def distance_3d(self, idx_1, idx_2):
        return self.points[idx_1].distance_3d(self.points[idx_2])

    # func 3d
    def points_to_3d(self, standard_skeleton):
        derivation_order = [(10, 9, 1),
                            (13, 12, 1),
                            (9, 8, -1),
                            (12, 11, -1),
                            (11, 1, 1),
                            (8, 1, 1, "re_calc"),
                            (1, 2, 0),
                            (1, 5, 0),
                            (2, 3, -1),
                            (5, 6, -1),
                            (3, 4, 1),
                            (6, 7, 1),
                            (1, 0, 1)]
        for items in derivation_order:
            re_calc = (len(items) == 4)
            idx_start, idx_end, sign = items[:3]
            standard_distance = standard_skeleton.distance_2d(idx_start, idx_end)
            try:
                math_functions.z_axis_calc(self.points[idx_start],
                                       self.points[idx_end],
                                       standard_distance,
                                       sign,
                                       re_calc)
            except AssertionError:
                print(self.points[idx_start], self.points[idx_end])
                print(self.points[idx_start].distance_2d(self.points[idx_end]))
                print(standard_distance)
                raise

def create_skeleton_list(matrix_3d):
    assert len(matrix_3d.shape) == 3
    assert matrix_3d.shape[1] == 18
    assert matrix_3d.shape[2] == 3
    skeleton_list = [Skeleton(points) for points in matrix_3d]
    return skeleton_list


if __name__ == "__main__":
    sk = Skeleton(list(range(54)))
    print(sk.plot_points)
    print(sk.animate_lines)
