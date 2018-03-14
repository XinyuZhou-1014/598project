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
    def __init__(self, keypoint_list, idx):
        # args: x, y, confidence
        self.x, self.y, self.conf = keypoint_list[3*idx : 3*idx+3]
        self.z = 0
        self.idx = idx
        self.part = idx_body[idx]


class Skeleton():
    def __init__(self, keypoint_list):
        self.points = []
        for i in range(len(keypoint_list) // 3):
            point_3d = Point(keypoint_list, i)
            self.points.append(point_3d)

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

