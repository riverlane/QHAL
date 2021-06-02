import unittest

from lib.hal._commands import (command_creator,
                               command_unpacker,
                               #measurement_creator,
                               measurement_unpacker,
                               Opcode)


class HALTest(unittest.TestCase):
    """Basic tests for HAL command creation and result validation.
    """

    def test_roundtrip_hal_commands(self):
        """Test roundtripping of the command packer/unpackers."""
        for opcode in Opcode.__members__.keys():
            print (opcode)
            for qubit in range(8):
                for arg in range(128):
                    self.assertEqual(
                        command_unpacker(command_creator(opcode, arg, qubit)),
                        (opcode, [arg], [qubit])
                    )

    def test_roundtrip_measurements_4q(self):
        """Test roundtripping of the command packer/unpackers."""
        #test_list = [((Masks.VALIDS.value) | int("0000000000000110", base=2),
        #              [0, 1, 2, 3])]
        #for bitcode, qubits in test_list:
        #    rt_bitcode = measurement_creator(
        #        measurement_unpacker(bitcode, qubits), qubits)
        #    self.assertEqual(rt_bitcode, bitcode)


if __name__ == "__main__":
    unittest.main()
