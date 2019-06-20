from django.test import TestCase


class SmokeTest(TestCase):
    """Some silly test"""

    def test_bad_maths(self):
        """Some bad math"""
        self.assertEqual(1 + 1, 3)