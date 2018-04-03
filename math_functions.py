import math

ignore_scale = 1.0
ignore_distance = 80

def z_axis_change_calc(point_start, point_end, standard_length):
    length = point_start.distance_2d(point_end)
    if length > standard_length:
        if (length - standard_length) / standard_length < ignore_scale:
            return 0
    abs_z_axis_diff = math.sqrt(standard_length ** 2 - length ** 2)
    return abs_z_axis_diff


def z_axis_calc(point_start, point_end, standard_length, sign, re_calculate=False):
    diff = z_axis_change_calc(point_start, point_end, standard_length)
    assert sign in ["+", "-", "=", 1, -1, 0, 1.0, -1.0, 0.0], "Sign not valid"
    sign = {"+": 1.0, "-": -1.0, "=": 0.0}.get(sign, sign)  # convert char to float
    if sign == 0.0:
        assert diff < ignore_scale * standard_length, "z diff can't ignore: {}, {}".format(diff, standard_length)
    if not re_calculate:
        point_end.z = point_start.z + sign * diff
        return
    else:
        temp = point_start.z + sign * diff
        assert (temp - point_end.z) < ignore_distance, "two estimate have too large differece: {}, {}".format(temp, point_end.z)
        point_end.z = (point_end.z + temp) / 2
        return
