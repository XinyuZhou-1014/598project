import numpy as np
import math
import math_functions
import json
import argparse
import os


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


def read(path):
    file_list = []
    res = []
    for filename in os.listdir(path):
        if filename.endswith("keypoints.json"):
            file_list.append(filename)
    file_list.sort()

    for filename in file_list:
        with open(os.path.join(path, filename), 'r') as f:
            res.append(json.load(f))
    return res


def get_keypoints(dct):
    try:
        l = dct['people'][0]  # assume only one person here
        l = l['pose_keypoints_2d']
    except:
        print("warning: no person")
        l = [0] * 54
    assert len(l) % 3 == 0
    res = []
    for i in range(len(l) // 3):
        res.append(tuple(l[3*i:3*i+3]))
    return np.array(res)


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


def smooth(matrix_3d, smooth_factor):
    res = np.zeros((len(matrix_3d) - smooth_factor + 1, 18, 3))
    for frame_idx in range(len(matrix_3d) - smooth_factor + 1):
        for point_idx in range(18):
            x_s = matrix_3d[frame_idx:frame_idx+smooth_factor, point_idx, 0]
            y_s = matrix_3d[frame_idx:frame_idx+smooth_factor, point_idx, 1]
            conf_s = matrix_3d[frame_idx:frame_idx+smooth_factor, point_idx, 2]
            conf_all = sum(conf_s)
            x_new = sum(x_s * conf_s) / conf_all
            y_new = sum(y_s * conf_s) / conf_all
            res[frame_idx, point_idx] = [x_new, y_new, conf_all / smooth_factor]
            #print(res[frame_idx, point_idx])
    return res


def create_skeleton_list(path, smooth_factor, skip_factor):
    list_of_json = read(path)
    matrix_3d = np.array(list(map(get_keypoints, list_of_json)))
    smoothed_matrix_3d = smooth(matrix_3d, smooth_factor)[::skip_factor]
    assert len(smoothed_matrix_3d.shape) == 3
    assert smoothed_matrix_3d.shape[1] == 18
    assert smoothed_matrix_3d.shape[2] == 3
    skeleton_list = [Skeleton(points) for points in smoothed_matrix_3d]
    return skeleton_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str,
                        help='the dir of the json files')
    parser.add_argument('-s', '--smooth', type=int, default=1,
                        help="smooth factor")
    parser.add_argument('--skip', type=int, default=1,
                        help="skip factor")
    parser.add_argument("--height", type=int, default=1000,
                        help="height of video")
    parser.add_argument("--width", type=int, default=1000,
                        help="width of video")

    args = parser.parse_args()
    path = args.filepath
    smooth_factor = args.smooth
    height, width = args.height, args.width
    skip_factor = args.skip

    print(create_skeleton_list(path, smooth_factor, skip_factor))