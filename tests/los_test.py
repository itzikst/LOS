import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from los import isVisible

class TestIsVisible(unittest.TestCase):
    def test_visibility(self):
        # Case where line of sight is clear (all elevations < heights)
        elevations_pass = [10, 10, 10, 10, 10]
        heights_pass = [20, 20, 20, 20, 20]
        self.assertTrue(isVisible(elevations_pass, heights_pass), "Should be visible")

        # Case where line of sight is blocked (one elevation >= height)
        elevations_fail = [10, 10, 30, 10, 10]
        heights_fail = [20, 20, 20, 20, 20]
        self.assertFalse(isVisible(elevations_fail, heights_fail), "Should not be visible")

if __name__ == '__main__':
    unittest.main()
