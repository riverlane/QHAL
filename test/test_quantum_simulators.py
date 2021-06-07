import unittest

import numpy as np
from projectq.backends import Simulator

from lib.quantum_simulators import ProjectqQuantumSimulator
from lib.hal import command_creator, measurement_unpacker


class TestQuantumSimulators(unittest.TestCase):
    """
    Test that checks the projQ output by running a simple test circuit and
    checking that the final wavefunction is as expected.
    """

    def test_circuit_equivalence(self):

        # set the size of the register
        n_qubits = 3

        projQ_backend = ProjectqQuantumSimulator(
            register_size=n_qubits,
            seed=234,
            backend=Simulator
        )

        circuit = [
            ["STATE_PREPARATION", 0, 0],
            ['X', 0, 0],
            ['H', 0, 2],
            ["CONTROL", 0, 2],
            ["Y", 0, 1],
            ["T", 0, 0],
            ["SX", 0, 1],
            ["T", 0, 2],
            ["S", 0, 2],
            ["CONTROL", 0, 1],
            ["Z", 0, 2],
            ["T", 0, 2],
            ["INVS", 0, 2],
            ['RZ', 672, 1],
            ['SQRT_X', 0, 0],
            ["CONTROL", 0, 2],
            ["X", 0, 0],
            ["H", 0, 2],
            ["PIXY", 458, 1],
        ]

        for commands in circuit:

            hal_cmd = command_creator(*commands)
            projQ_backend.accept_command(hal_cmd)

        # extract wavefunction at the end of the circuit (before measuring)
        psi_projq = np.array(projQ_backend._engine.backend.cheat()[1])

        # send measure command to projQ backend (will complain if not flushed)
        projQ_backend.accept_command(command_creator(*['QUBIT_MEASURE', 0, 0]))

        self.assertEqual(
            list(psi_projq), [
                (0.25903240188259363-0.2406287904115682j),
                (0.2406287904115682+0.25903240188259363j),
                (-0.2590324018825938-0.2406287904115681j),
                (-0.2406287904115681+0.2590324018825938j),
                (0.25903240188259363-0.2406287904115682j),
                (0.2406287904115682+0.25903240188259363j),
                (0.2590324018825938+0.2406287904115681j),
                (0.2406287904115681-0.2590324018825938j)]
        )

    def test_individual_qubit_measurements(self):

        projQ_backend = ProjectqQuantumSimulator(
            register_size=2,
            seed=234,
            backend=Simulator
        )

        circuit = [
            ["STATE_PREPARATION", 0, 0],
            ['X', 0, 0]
        ]

        for commands in circuit:

            hal_cmd = command_creator(*commands)
            projQ_backend.accept_command(hal_cmd)

        hal_res_0 = projQ_backend.accept_command(
            command_creator("QUBIT_MEASURE", 0, 0)
        )
        hal_res_1 = projQ_backend.accept_command(
            command_creator("QUBIT_MEASURE", 0, 1)
        )

        decoded_hal_result_0 = measurement_unpacker(hal_res_0)
        decoded_hal_result_1 = measurement_unpacker(hal_res_1)

        self.assertEqual(decoded_hal_result_0[0], 0)
        self.assertEqual(decoded_hal_result_0[2], 1)
        self.assertEqual(decoded_hal_result_1[0], 1)
        self.assertEqual(decoded_hal_result_1[2], 0)

    def test_double_measurement_fails(self):
        """Tests thats you can't measure the same qubit twice.
        """

        # single qubit
        projQ_backend = ProjectqQuantumSimulator(
            register_size=1,
            seed=234,
            backend=Simulator
        )

        circuit = [
            ["STATE_PREPARATION", 0, 0],
            ['X', 0, 0],
            ['QUBIT_MEASURE', 0, 0]
        ]

        for commands in circuit:

            hal_cmd = command_creator(*commands)
            projQ_backend.accept_command(hal_cmd)

        with self.assertRaises(ValueError):
            projQ_backend.accept_command(
                command_creator(*['QUBIT_MEASURE', 0, 0])
            )

        # multi qubit
        projQ_backend = ProjectqQuantumSimulator(
            register_size=2,
            seed=234,
            backend=Simulator
        )

        circuit = [
            ["STATE_PREPARATION", 0, 0],
            ['X', 0, 0],
            ['QUBIT_MEASURE', 0, 0],
            ['QUBIT_MEASURE', 0, 1]
        ]

        for commands in circuit:

            hal_cmd = command_creator(*commands)
            projQ_backend.accept_command(hal_cmd)

        with self.assertRaises(ValueError):
            projQ_backend.accept_command(
                command_creator(*['QUBIT_MEASURE', 0, 0])
            )


if __name__ == "__main__":
    unittest.main()
