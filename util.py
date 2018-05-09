from math import isclose

from skeleton import body_idx



AVG_US_MALE_HEIGHT = 177.0
AVG_US_MALE_FOOT = 27.3
AVG_US_MALE_HIP = 10
HEIGHT_FOOT_RATIO = AVG_US_MALE_HEIGHT / AVG_US_MALE_FOOT
HEIGHT_HIP_RATIO = AVG_US_MALE_HEIGHT / AVG_US_MALE_HIP

ABS_TOLERENCE = 3
def approx_equal(a, b):
    return isclose(a, b, abs_tol = ABS_TOLERENCE)

def get_height(points):
    nose = get_part(points, 'Nose')
    l_eye = get_part(points, 'LEye')
    r_eye = get_part(points, 'REye')

    # head height = nose - avg(nose - eye) * 2
    head_height = l_eye.y + r_eye.y - nose.y
    l_ankle = get_part(points, 'LAnkle')
    r_ankle = get_part(points, 'RAnkle')
    foot_height = (l_ankle.y + r_ankle.y) / 2
    return foot_height - head_height

def get_foot_len(points):
    return get_height(points) / HEIGHT_FOOT_RATIO

def get_part(points, idx_name):
    return points[body_idx[idx_name]]

def get_hip_height(points):
    return get_height(points) / HEIGHT_HIP_RATIO
