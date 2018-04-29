from math import atan, degrees

from util import approx_equal, get_foot_len, get_part

# place here easy to see
# idx_body = {
#     0: 'Nose',
#     1: 'Neck',
#     2: 'RShoulder',
#     3: 'RElbow',
#     4: 'RWrist',
#     5: 'LShoulder',
#     6: 'LElbow',
#     7: 'LWrist',
#     8: 'RHip',
#     9: 'RKnee',
#     10: 'RAnkle',
#     11: 'LHip',
#     12: 'LKnee',
#     13: 'LAnkle',
#     14: 'REye',
#     15: 'LEye',
#     16: 'REar',
#     17: 'LEar'
# }


class Violation:
    SHOULDER_HEIGHT = "Left and right shoulder height are different"
    HIP_HEIGHT = "Left and right hip height are different"
    LEFT_KNEE_BUCKLE = "Left knee buckle"
    RIGHT_KNEE_BUCKLE = "Right knee buckle"
    LEFT_KNEE_EXCEED_TOE = "Left knee exceed toe"
    RIGHT_KNEE_EXCEED_TOE = "Right knee exceed toe"
    ANKLE_WIDTH = "Left and right ankle width different"

    def __init__(self, idx, message):
        self.idx = idx
        self.message = message

    def __eq__(self, other):
        if isinstance(other, Violation):
            return (self.idx == other.idx and self.message == other.message)
        return False

    def __repr__(self):
        return "Frame: {0} Violation type: {1}\n".format(self.idx, self.message)


class Standard:
    STANDARD_CONDITION = "Hip lower than knee"

    def __init__(self):
        self.reached = False
        self.record = []

    def is_reached(self):
        return self.reached

    def set_reached(self, idx):
        self.reached = True
        self.record.append(idx)

    def reset_reached(self):
        self.reached = False

    def get_record(self):
        return self.record


class Rule:
    """
    violations to check
        The knees shouldn’t buckle
        The knee should not exceed toe in the vertical direction
        Left and right shoulder at same height
        Left and right hip should at same height
        The lifter shouldn’t lean over too much
        The lifter shouldn’t come down too fast
        Left and right ankle same stand width  # assume foot not moving
    standard squat goal
        hip lower than knee
    """

    def __init__(self, points_list):
        self.points_list = points_list
        self.violation_list = []
        self.standard = Standard()
        self.foot_len = get_foot_len(self.points_list[0])

    def check_once(self, idx, points):
        # assign point to part
        neck = get_part(points, 'Neck')
        l_shoulder = get_part(points, 'LShoulder')
        r_shoulder = get_part(points, 'RShoulder')
        l_hip = get_part(points, 'LHip')
        r_hip = get_part(points, 'RHip')
        l_knee = get_part(points, 'LKnee')
        r_knee = get_part(points, 'RKnee')
        l_ankle = get_part(points, 'LAnkle')
        r_ankle = get_part(points, 'RAnkle')

        if self.shoulder_different_height(l_shoulder, r_shoulder):
            self.violation_list.append(Violation(idx, Violation.SHOULDER_HEIGHT))
        if self.hip_different_height(l_hip, r_hip):
            self.violation_list.append(Violation(idx, Violation.HIP_HEIGHT))
        if self.knee_buckle(l_hip, l_knee, l_ankle, 'left'):
            self.violation_list.append(Violation(idx, Violation.LEFT_KNEE_BUCKLE))
        if self.knee_buckle(r_hip, r_knee, r_ankle, 'right'):
            self.violation_list.append(Violation(idx, Violation.RIGHT_KNEE_BUCKLE))
        if self.knee_exceed_toe(l_knee, l_ankle):
            self.violation_list.append(Violation(idx, Violation.LEFT_KNEE_EXCEED_TOE))
        if self.knee_exceed_toe(r_knee, r_ankle):
            self.violation_list.append(Violation(idx, Violation.RIGHT_KNEE_EXCEED_TOE))
        if self.ankle_different_width(neck, l_ankle, r_ankle):
            self.violation_list.append(Violation(idx, Violation.ANKLE_WIDTH))

        if self.standard.is_reached() != self.check_standard(l_hip, r_hip, l_knee, r_knee):
            if self.standard.is_reached():
                self.standard.reset_reached()
            else:
                self.standard.set_reached(idx)

    def check_all_frame(self):
        for idx, points in enumerate(self.points_list):
            self.check_once(idx, points)

    def shoulder_different_height(self, l_shoulder, r_shoulder):
        return not approx_equal(l_shoulder.y, r_shoulder.y)

    def body_lean_over(self):
        ## TODO: define what is body lean over
        return False

    def check_standard(self, l_hip, r_hip, l_knee, r_knee):
        return (self.hip_lower_than_knee(l_hip, l_knee) and
               self.hip_lower_than_knee(r_hip, r_knee))

    def hip_lower_than_knee(self, hip, knee):
        return hip.y >= knee.y

    def hip_different_height(self, l_hip, r_hip):
        return not approx_equal(l_hip.y, r_hip.y)

    def knee_exceed_toe(self, knee, ankle):
        foot_z = ankle.z + self.foot_len
        return knee.z > foot_z

    def knee_buckle(self, hip, knee, ankle, side, buck_angle=145.0):
        if side == 'left' and knee.x >= hip.x:
            return False
        elif side == 'right' and knee.x <= hip.x:
            return False
        hip_knee_angle = atan(abs(hip.y - knee.y) / abs(hip.x - knee.x))
        knee_ankle_angle = atan(abs(knee.y - ankle.y) / abs(knee.x - ankle.x))
        total_angle = degrees(hip_knee_angle + knee_ankle_angle)
        return total_angle <= buck_angle

    def ankle_different_width(self, neck, l_ankle, r_ankle):
        l_width = abs(neck.x - l_ankle.x)
        r_width = abs(neck.x - r_ankle.x)
        return not approx_equal(l_width, r_width)

    def move_too_fast(self):
        ## TODO: define what is too fast
        return False
