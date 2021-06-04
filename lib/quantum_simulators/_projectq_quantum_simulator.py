import atexit
import logging

import numpy as np
from numpy import uint64
from typing import Tuple
from numpy.random import RandomState

from projectq import MainEngine
from projectq.backends import CircuitDrawer, Simulator
from projectq.ops import (All, C, DaggeredGate, H, Measure, R,
                          Rx, Ry, Rz, S, SqrtX, T, X, Y, Z)
from projectq.ops._basics import BasicGate, BasicRotationGate

from . import IQuantumSimulator
from ..hal import command_unpacker, string_to_command


class SxGate(BasicGate):
    """Gate that consists of consecutive S and X gate
    (pi-rotation with axis in x-y-plane).
    """

    @property
    def matrix(self):
        return np.array([[0, 1], [1j, 0]])

    def __str__(self):
        return "SX"


#: Shortcut (instance of) :class:`projectq.ops.SxGate`
Sx = SxGate()


class SyGate(BasicGate):
    """Gate that consists of consecutive S and Y gate
    (pi-rotation with axis in x-y-plane).
    """

    @property
    def matrix(self):
        return np.array([[0, 1j], [1, 0]])

    def __str__(self):
        return "SY"


#: Shortcut (instance of) :class:`projectq.ops.SyGate`
Sy = SyGate()


class PiXY(BasicRotationGate):
    """Pi-rotation with axis in x-y-plane gate class."""

    @property
    def matrix(self):
        return np.array([[0, -np.sin(self.angle) - 1j * np.cos(self.angle)],
                         [np.sin(self.angle) - 1j * np.cos(self.angle), 0]])


class PiYZ(BasicRotationGate):
    """Pi-rotation with axis in y-z-plane gate class."""

    @property
    def matrix(self):
        return np.array([[np.cos(self.angle), -1j * np.sin(self.angle)],
                         [1j * np.sin(self.angle), -1 * np.cos(self.angle)]])


class PiZX(BasicRotationGate):
    """Pi-rotation with axis in z-x-plane gate class."""

    @property
    def matrix(self):
        return np.array([[np.cos(self.angle), np.sin(self.angle)],
                         [np.sin(self.angle), -1 * np.cos(self.angle)]])


class ProjectqQuantumSimulator(IQuantumSimulator):
    """Concrete ProjectQ implementation of the IQuantumSimulator interface.

    Parameters
    ----------
    register_size: int
        Size of the qubit register.
    seed : int
        Random number generator seed for both the ProjectQ Simulator and
        circuit errors.
    backend
        ProjectQ backend, could use CircuitDrawer for debugging purposes.


    .. TODO::
        Add and example how to use it in a graph (without any simulator).
    """

    def __init__(self,
                 register_size: int = 16,
                 seed: int = None,
                 backend=Simulator):
        if backend == Simulator and seed is not None:
            self._engine = MainEngine(backend=Simulator(rnd_seed=seed))

        else:
            self._engine = MainEngine(backend=backend())
        self.backend = backend
        self.seed = seed

        # if random numbers are needed to simulate quantum noise use this
        # state in the following way self._random_state.rand()
        self._random_state = RandomState(seed)

        self._qubit_register = None

        # defaulted to 16 because the bitcode status return
        # has 16 bits assigned for measurement results.
        self._qubit_register_size = register_size

        # stores control qubits
        self._control_qubit_indices = []

        # assign projectq gate to each opcode
        self._parameterised_gate_dict = {
            'CONTROL': C,
            'R': R,
            'RX': Rx,
            'RY': Ry,
            'RZ': Rz,
            'PIXY': PiXY,
            'PIYZ': PiYZ,
            'PIZX': PiZX,
        }

        self._constant_gate_dict = {
            'H': H,
            'S': S,
            'SQRT_X': SqrtX,
            'T': T,
            'X': X,
            'Y': Y,
            'Z': Z,
            'INVS': DaggeredGate(S),
            'SX': Sx,  # consecutive S and X gate, needed for RC
            'SY': Sy,  # consecutive S and Y gate, needed for RC
        }
        atexit.register(self.cleanup)

    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the engine has it generally unpickable.
        del state['_engine']
        return state

    def __setstate__(self, state):
        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)
        # Restore the engine
        if self.backend == Simulator and self.seed is not None:
            self._engine = MainEngine(backend=Simulator(rnd_seed=self.seed))
        else:
            self._engine = MainEngine(backend=self.backend())

    def cleanup(self):
        """Release all the qubits that haven't been handled yet."""
        if self._qubit_register is not None:
            All(Measure) | self._qubit_register
        self._engine.flush()

    def apply_gate(self,
                   gate: BasicGate,
                   qubit_index: int,
                   parameter: float = None):
        """Receives command information and implements the gate on the
        corresponding qubit.

        Parameters
        ----------
        gate : BasicGate
            ProjectQ gate to be applied.
        qubit_index : int
            Index of qubit for gate to be applied to.
        parameter : float
            Angle of gate if parametrised.
        """
        if self._qubit_register is not None:

            if gate is C:
                # add qubit index to self.control_qubit_indices, store
                # in memory until a gate is called, which is run controlled
                # on these qubits.

                if qubit_index in self._control_qubit_indices:
                    raise ValueError(
                        f"Qubit {qubit_index} already set-up as control qubit!"
                    )

                if len(self._control_qubit_indices) + 1 \
                        == self._qubit_register_size:

                    raise ValueError(
                        "Too many control qubits for register size of " +
                        "f{self._qubit_register_size}!"
                    )

                self._control_qubit_indices += [qubit_index]

            else:
                if len(self._control_qubit_indices) == 0:  # single qubit gate
                    if parameter is not None:
                        gate(parameter) | self._qubit_register[qubit_index]
                    else:
                        gate | self._qubit_register[qubit_index]

                else:  # controlled gate
                    if qubit_index in self._control_qubit_indices:
                        raise ValueError(
                            f"Target qubit {qubit_index} already set-up as " +
                            "control qubit!"
                        )

                    control_number = len(self._control_qubit_indices)
                    control_qubits = [
                        self._qubit_register[index] for
                        index in self._control_qubit_indices
                    ]

                    control_reg = tuple(
                        [control_qubits, self._qubit_register[qubit_index]]
                    )
                    if parameter is not None:
                        C(gate(parameter), n=control_number) | control_reg
                    else:
                        C(gate, n=control_number) | control_reg

                    # reset control indices
                    self._control_qubit_indices = []

                self._engine.flush()

    def accept_command(
        self,
        command: Tuple[uint64, uint64]
    ) -> uint64:

        op, args, qubit_indexes = command_unpacker(command)
        op_obj = string_to_command(op)

        for index in qubit_indexes:
            assert index <= self._qubit_register_size, \
                f"Qubit index {index} greater than register size ({self._qubit_register_size})!"

        if op == "STATE_PREPARATION":
            if not self._qubit_register:
                self._qubit_register = self._engine.allocate_qureg(
                    self._qubit_register_size
                )

        elif op == "STATE_MEASURE":
            # This measures a single qubit at the time.
            # TODO: this needs reviewing.

            All(Measure) | self._qubit_register
            self._engine.flush()
            # TODO: review this.
            meas = self._qubit_register[qubit_indexes[0]]
            print (f"meas - {meas}")
            self._qubit_register = None

            return (int(meas) << 32) + qubit_indexes[0]

        elif op == "ID":
            pass

        elif op_obj.param == "PARAM":
            if op_obj.type == "SINGLE":
                angle = args[0] * (2 * np.pi) / 1024
                gate = self._parameterised_gate_dict[op]
                print (f"gate: {gate} : qubit_indexes[0] - {qubit_indexes[0]}")
                self.apply_gate(gate, qubit_indexes[0], angle)
            else:
                logging.warning(f"{op} - Support yet to be added")

        elif op_obj.param == "CONST":
            gate = self._constant_gate_dict[op]
            if op_obj.type == "SINGLE":
                self.apply_gate(gate, qubit_indexes[0])
            else:
                logging.warning(f"{op} - Support yet to be added")
        else:
            raise TypeError(f"{op} is not a recognised opcode!")
