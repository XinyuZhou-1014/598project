import unittest

from skeleton import Point
from util import approx_equal, get_foot_len, get_part, HEIGHT_FOOT_RATIO


class TestUtil(unittest.TestCase):
    def setUp(self):
        self.points = [
            # x, y, conf, idx, z
            Point(50, 50, 1, 0, 0),     #     0: 'Nose',
            Point(50, 55, 1, 0, 0),     #     1: 'Neck',
            Point(40, 55, 1, 0, 0),     #     2: 'RShoulder',
            Point(35, 75, 1, 0, 0),     #     3: 'RElbow',
            Point(30, 95, 1, 0, 0),     #     4: 'RWrist',
            Point(60, 55, 1, 0, 0),     #     5: 'LShoulder',
            Point(65, 75, 1, 0, 0),     #     6: 'LElbow',
            Point(70, 95, 1, 0, 0),     #     7: 'LWrist',
            Point(43, 95, 1, 0, 0),     #     8: 'RHip',
            Point(42, 125, 1, 0, 0),    #     9: 'RKnee',
            Point(40, 155, 1, 0, 0),    #     10: 'RAnkle',
            Point(57, 95, 1, 0, 0),     #     11: 'LHip',
            Point(58, 125, 1, 0, 0),    #     12: 'LKnee',
            Point(60, 155, 1, 0, 0),    #     13: 'LAnkle',
            Point(48, 47, 1, 0, 0),     #     14: 'REye',
            Point(52, 47, 1, 0, 0),     #     15: 'LEye',
            Point(45, 48, 1, 0, 0),     #     16: 'REar',
            Point(55, 48, 1, 0, 0)      #     17: 'LEar'
        ]

    def test_approx_equal_true(self):
        self.assertTrue(approx_equal(200, 200.5))

    def test_approx_equal_false(self):
        self.assertFalse(approx_equal(200, 200.6))

    def test_get_foot_len(self):
        expect_len = (155 - (47 + 47 - 50)) / HEIGHT_FOOT_RATIO
        result = get_foot_len(self.points)
        self.assertEqual(expect_len, result)

    def test_get_part(self):
        result = get_part(self.points, 'LAnkle')
        l_ankle = Point(60, 155, 1, 0, 0)
        self.assertEqual(l_ankle, result)
