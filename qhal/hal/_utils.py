import numpy as np


def angle_binary_representation(angle: float) -> int:
    """Converts an angle in radians to a 16-bit representation.

    Parameters
    ----------
    angle : float
        The angle (in radians) to be converted.

    Returns
    -------
    int
        16-bit representation of angle.
    """
    return int(np.rint(angle / (2 * np.pi / 2**16)))
