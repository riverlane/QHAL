import numpy as np
import unittest

from qhal.hal._utils import angle_binary_representation


class UtilsTest(unittest.TestCase):
    """basic tests for HAL util functions.
    """

    def test_angle_binary_conversion(self):
        """Thest the conversion of angles to 16-bit representation."""

        test_cases = {
            0: angle_binary_representation(0),
            8192: angle_binary_representation(np.pi/4),
            10923: angle_binary_representation(np.pi/3),
            16384: angle_binary_representation(np.pi/2),
            21845: angle_binary_representation(2 * np.pi/3),
            24576: angle_binary_representation(3 * np.pi/4),
            32768: angle_binary_representation(np.pi),
            40960: angle_binary_representation(5 * np.pi/4),
            43691: angle_binary_representation(4 * np.pi/3),
            49152: angle_binary_representation(3 * np.pi/2),
            54613: angle_binary_representation(5 * np.pi/3),
            57344: angle_binary_representation(7 * np.pi/4),
            65536: angle_binary_representation(2 * np.pi),
        }

        for expected, calculated in test_cases.items():
            self.assertEqual(expected, calculated)


if __name__ == "__main__":
    unittest.main()
