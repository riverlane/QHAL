import unittest

from qhal.hal._commands import (command_creator,
                               command_unpacker,
                               measurement_creator,
                               measurement_unpacker,
                               _OPCODES)


class HALTest(unittest.TestCase):
    """Basic tests for HAL command creation and result validation.
    """

    def test_roundtrip_hal_commands(self):
        """Test roundtripping of the command packer/unpackers."""
        for opcode in _OPCODES:
            if opcode.cmd_type == "SINGLE":
                for qubit0 in range(8):
                    for arg0 in range(32):
                        self.assertEqual(
                            command_unpacker(command_creator(
                                opcode.name, arg0, qubit0
                            )), (opcode.name, opcode.cmd_type, [arg0], [qubit0])
                        )
            else:
                for qubit0 in range(8):
                    for qubit1 in range(8):
                        for arg0 in range(32):
                            for arg1 in range(32):
                                self.assertEqual(
                                    command_unpacker(
                                        command_creator(
                                            opcode.name,
                                            arg0,
                                            qubit0,
                                            arg1,
                                            qubit1
                                        )
                                    ),
                                    (
                                        opcode.name,
                                        opcode.cmd_type,
                                        [arg0, arg1],
                                        [qubit0, qubit1]
                                    )
                                )

    def test_measurement_creator_unpacker(self):
        """Tests measurement encoding is consistent between measurement creator
        and unpacker functions.
        """

        for idx in range(8):
            for offset in range(8):
                for status in range(8):
                    for res in range(2):
                        args = (idx, offset, status, res)
                        self.assertEqual(
                            args, 
                            measurement_unpacker(measurement_creator(*args))
                        )


if __name__ == "__main__":
    unittest.main()
