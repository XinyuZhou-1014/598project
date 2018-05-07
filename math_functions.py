import math
from math import cos, sin


ignore_scale = 1.0
ignore_distance = 80

def z_axis_change_calc(point_start, point_end, standard_length):
    """
    calculate the relative z axis value by triangle formula, have tolerance
    """
    length = point_start.distance_2d(point_end)
    if length > standard_length:
        if abs(length - standard_length) / standard_length < ignore_scale:
            return 0
        raise ValueError("Current projected length larger than standard length")
    abs_z_axis_diff = math.sqrt(standard_length ** 2 - length ** 2)
    return abs_z_axis_diff


def z_axis_calc(point_start, point_end, standard_length, sign, re_calculate=False):
    """
    calculate the absolute z axis value by 
    relative z axis value, start z axis value, sign and some adjustment

    """
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


def rotation_matrix(α, β, γ):
    """
    rotation matrix of α, β, γ radians around x, y, z axes (respectively)
    """
    sα, cα = sin(α), cos(α)
    sβ, cβ = sin(β), cos(β)
    sγ, cγ = sin(γ), cos(γ)
    return (
        (cβ * cγ, -cβ * sγ, sβ),
        (cα * sγ + sα * sβ * cγ, cα * cγ - sγ * sα * sβ, -cβ * sα),
        (sγ * sα - cα * sβ * cγ, cα * sγ * sβ + sα * cγ, cα * cβ)
    )
