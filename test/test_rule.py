import unittest

from skeleton import Point
from rule import *


class TestRule(unittest.TestCase):

    def setUp(self):
        points_1 = [
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
        self.rule = Rule([points_1])

    def test_shoulder_different_height(self):
        l_shoulder = Point(60, 55, 1, 0, 0)
        r_shoulder = Point(40, 53, 1, 0, 0)
        result = self.rule.shoulder_different_height(l_shoulder, r_shoulder)
        self.assertTrue(result)

    def test_shoulder_same_height(self):
        l_shoulder = Point(60, 55, 1, 0, 0)
        r_shoulder = Point(40, 55, 1, 0, 0)
        result = self.rule.shoulder_different_height(l_shoulder, r_shoulder)
        self.assertFalse(result)

    def test_hip_lower_than_knee(self):
        hip = Point(57, 125, 1, 0, 0)
        knee = Point(58, 125, 1, 0, 0)
        result = self.rule.hip_lower_than_knee(hip, knee)
        self.assertTrue(result)

    def test_hip_higher_than_knee(self):
        hip = Point(57, 120, 1, 0, 0)
        knee = Point(58, 125, 1, 0, 0)
        result = self.rule.hip_lower_than_knee(hip, knee)
        self.assertFalse(result)

    def test_hip_different_height(self):
        l_hip = Point(57, 120, 1, 0, 0)
        r_hip = Point(47, 119, 1, 0, 0)
        result = self.rule.hip_different_height(l_hip, r_hip)
        self.assertTrue(result)

    def test_hip_same_height(self):
        l_hip = Point(57, 120, 1, 0, 0)
        r_hip = Point(47, 119.5, 1, 0, 0)
        result = self.rule.hip_different_height(l_hip, r_hip)
        self.assertFalse(result)

    def test_knee_exceed_toe(self):
        # foot len is 17.12
        knee = Point(58, 125, 1, 0, 18)
        ankle = Point(60, 155, 1, 0, 0)
        result = self.rule.knee_exceed_toe(knee, ankle)
        self.assertTrue(result)

    def test_knee_not_exceed_toe(self):
        # foot len is 17.12
        knee = Point(58, 125, 1, 0, 17)
        ankle = Point(60, 155, 1, 0, 0)
        result = self.rule.knee_exceed_toe(knee, ankle)
        self.assertFalse(result)

    def test_left_knee_buckle(self):
        hip = Point(60, 95, 1, 0, 0)
        knee = Point(50, 125, 1, 0, 0)
        ankle = Point(60, 155, 1, 0, 0)
        result = self.rule.knee_buckle(hip, knee, ankle, 'left')
        self.assertTrue(result)

    def test_left_knee_not_buckle(self):
        hip = Point(60, 95, 1, 0, 0)
        knee = Point(58, 125, 1, 0, 0)
        ankle = Point(60, 155, 1, 0, 0)
        result = self.rule.knee_buckle(hip, knee, ankle, 'left')
        self.assertFalse(result)

    def test_right_knee_buckle(self):
        hip = Point(60, 95, 1, 0, 0)
        knee = Point(70, 125, 1, 0, 0)
        ankle = Point(60, 155, 1, 0, 0)
        result = self.rule.knee_buckle(hip, knee, ankle, 'right')
        self.assertTrue(result)

    def test_right_knee_not_buckle(self):
        hip = Point(60, 95, 1, 0, 0)
        knee = Point(62, 125, 1, 0, 0)
        ankle = Point(60, 155, 1, 0, 0)
        result = self.rule.knee_buckle(hip, knee, ankle, 'right')
        self.assertFalse(result)


    def test_ankle_different_width(self):
        neck = Point(50, 55, 1, 0, 0)
        l_ankle = Point(60, 155, 1, 0, 0)
        r_ankle = Point(41, 155, 1, 0, 0)
        result = self.rule.ankle_different_width(neck, l_ankle, r_ankle)
        self.assertTrue(result)

    def test_ankle_same_width(self):
        neck = Point(50, 55, 1, 0, 0)
        l_ankle = Point(60, 155, 1, 0, 0)
        r_ankle = Point(40.5, 155, 1, 0, 0)
        result = self.rule.ankle_different_width(neck, l_ankle, r_ankle)
        self.assertFalse(result)

    def test_check_standard_both_hips_exceed(self):
        l_hip = Point(60, 126, 1, 0, 0)
        l_knee = Point(62, 125, 1, 0, 0)
        r_hip = Point(40, 126, 1, 0, 0)
        r_knee = Point(42, 125, 1, 0, 0)
        result = self.rule.check_standard(l_hip, r_hip, l_knee, r_knee)
        self.assertTrue(result)

    def test_check_standard_only_one_hip_exceed(self):
        l_hip = Point(60, 120, 1, 0, 0)
        l_knee = Point(62, 125, 1, 0, 0)
        r_hip = Point(40, 126, 1, 0, 0)
        r_knee = Point(42, 125, 1, 0, 0)
        result = self.rule.check_standard(l_hip, r_hip, l_knee, r_knee)
        self.assertFalse(result)

    def test_check_standard_no_hip_exceed(self):
        l_hip = Point(60, 120, 1, 0, 0)
        l_knee = Point(62, 125, 1, 0, 0)
        r_hip = Point(40, 10, 1, 0, 0)
        r_knee = Point(42, 125, 1, 0, 0)
        result = self.rule.check_standard(l_hip, r_hip, l_knee, r_knee)
        self.assertFalse(result)

    def test_check_once_no_violation_no_standard(self):
        points = self.rule.points_list[0]
        self.rule.check_once(0, points)
        self.assertEqual([], self.rule.violation_list)
        self.assertEqual([], self.rule.standard.get_record())


    def test_check_once_shoulder_height_violation(self):
        points = self.rule.points_list[0]
        # change one shoulder height to different value
        points[2].y = 100
        self.rule.check_once(0, points)
        expect_violation = Violation(0, Violation.SHOULDER_HEIGHT)
        self.assertEqual(expect_violation, self.rule.violation_list[0])

    def test_check_once_standard_reached_once(self):
        points = self.rule.points_list[0]
        # change two hips height to over knee
        points[8].y = 126
        points[11].y = 126
        self.rule.check_once(0, points)
        result = self.rule.standard.get_record()
        expect_record = [0]
        self.assertEqual(expect_record, result)

    def fun(self):
        pass
