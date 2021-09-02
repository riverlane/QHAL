from numpy import uint64
from ..quantum_simulators import IQuantumSimulator


class HardwareAbstractionLayer:
    """Encapsulates a process which receives HAL commands and uses them to
    perform operations on a quantum device.

    Parameters
    ----------
    quantum_simulator : IQuantumSimulator
        Object with the IQuantumSimulator interface that accepts commands
        and returns measurement results.
    """

    def __init__(
        self,
        quantum_simulator: IQuantumSimulator
    ):
        self._quantum_simulator = quantum_simulator

    def accept_command(self, hal_command: uint64) -> uint64:
        """Interface for ``quantum_simulator.accept_command``.

        Parameters
        ----------
        command : uint64
            The HAL command to deconstruct and use to perform actions.

        Returns
        -------
        uint64
            Result of a measurement command.
        """
        return self._quantum_simulator.accept_command(hal_command)
