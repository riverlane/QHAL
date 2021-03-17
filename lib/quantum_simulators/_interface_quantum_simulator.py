from abc import ABC, abstractclassmethod

from numpy import uint32


class IQuantumSimulator(ABC):
    """Abstract class for interfacing with a quantum simulators that interacts
    with the HAL.
    """

    @abstractclassmethod
    def accept_command(
        cls,
        command: uint32
    ) -> uint32:
        """Performs required logic based on received commands, and returns
        results if command is a measurement.

        Parameters
        ----------
        command : DUInt(DSize(32))
            The HAL command to deconstruct and use to perform actions.

        Returns
        -------
        DUInt(DSize(32))
            Result of a measurement command.
        """
        pass
