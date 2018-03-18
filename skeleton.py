import numpy as np

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
    def __init__(self, x, y, conf, idx):
        # args: x, y, confidence
        self.x, self.y, self.conf = x, y, conf
        self.z = 0
        self.idx = idx
        self.part = idx_body[idx]

    def __str__(self):
        return "({}, {}, {})".format(self.idx, self.x, self.y)

    @property
    def pos(self):
        return (int(self.x), int(self.y))

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
        points = self.points[mask]
        if dim == 2:
            return [p.x for p in points], [p.y for p in points]
        elif dim == 3:
            return ([p.x for p in points],
                    [p.y for p in points],
                    [p.z for p in points])

    @property
    def animate_lines(self):
        mask = [(0, 1), (1, 2), (2, 3), (3, 4),
                (1, 5), (5, 6), (6, 7),
                (1, 8), (8, 9), (9, 10),
                (1, 11), (11, 12), (12, 13)]

        lines = [(self.points[i], self.points[j]) for i, j in mask]
        return lines


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
