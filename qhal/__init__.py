from .__about__ import (
    __license__,
    __copyright__,
    __url__,
    __contributors__,
    __version__,
    __doc__
)

from .hal import (HardwareAbstractionLayer,
                  string_to_opcode,
                  command_creator)
from .quantum_simulators import (IQuantumSimulator,
                                 ProjectqQuantumSimulator)
