"""
All the commands respect the following structure:

+------------------+----------+-----------------+-----------------------------+
| Command type     | OPCODE   | ARGUMENT        | RELATIVE_QUBIT_IDX          |
|                  |          |                 |                             |
| Control, Single, | Command  | Argument for    | Relative index of the       |
| or Dual Qubit    | to       | the command     | QUBIT                       |
| command          | execute  |                 |                             |
+==================+==========+=================+=============================+
| CONTROL COMMANDS | [63-52]  | [51-36]         | [35-0] BASE_QUBIT0/1_IDX    |
+------------------+----------+-----------------+-----------------------------+
| SINGLE QUBIT     | [63-52]  | [51-36] padding | [19-10] padding             |
| COMMANDS         |          |                 |                             |
|                  |          | [35-20]         | [9-0] RELATIVE_QUBIT0_IDX   |
+------------------+----------+-----------------+-----------------------------+
| DUAL QUBIT       | [63-52]  | [51-36] arg1    | [19-10] RELATIVE_QUBIT1_IDX |
| COMMANDS         |          |                 |                             |
|                  |          | [35-20] arg0    | [9-0] RELATIVE_QUBIT0_IDX   |
+------------------+----------+-----------------+-----------------------------+

OPCODE is structured as:
SINGLE/DUAL | CONSTANT/PARAMETRIC   |   OPCODE
[11]        |   [10]                |   [9-0]

"""

from enum import Enum
from typing import List, Tuple

from numpy import uint64


class _Shifts(Enum):
    """
    Defines the position of the command subfields.
    """
    OPCODE_TYPE = 63

    OPCODE = 52
    ARG0 = 20
    IDX0 = 0
    ARG1 = 36
    IDX1 = 10


class _Masks(Enum):
    """ Masks used to decompose the commands """

    # Relative to entire 64-bit command
    QUBIT0_MASK = 0x3FF
    QUBIT1_MASK = 0xFFC00
    ARG0_MASK = 0xFFFF00000
    ARG1_MASK = 0xFFFF000000000

    # Relative to 12-bit OPCODE
    OPCODE_PARAM_MASK = 0x400
    OPCODE_DUAL_MASK = 0x800


class Opcode:
    def __init__(self, name, code, cmd_type, param):
        self.name = name
        self.code = code
        self.cmd_type = cmd_type
        self.param = param
        self._validate()

    def _validate(self):
        if self.cmd_type == "DUAL":
            assert (self.code & _Masks.OPCODE_DUAL_MASK.value != 0)
        else:
            assert (self.code & _Masks.OPCODE_DUAL_MASK.value == 0)
        if self.param == "PARAM":
            assert (self.code & _Masks.OPCODE_PARAM_MASK.value != 0)
        else:
            assert (self.code & _Masks.OPCODE_PARAM_MASK.value == 0)


_OPCODES = [
    # SINGLE WORD Commands
    ## Configuration Session
    Opcode("START_SESSION", 0, "SINGLE", "CONST"),
    Opcode("END_SESSION", 1, "SINGLE", "CONST"),
    Opcode("PAGE_SET_QUBIT_0", 2, "SINGLE", "CONST"),
    Opcode("PAGE_SET_QUBIT_1", 3, "SINGLE", "CONST"),
    Opcode("NOP", 4, "SINGLE", "CONST"),
    Opcode("STATE_PREPARATION_ALL", 5, "SINGLE", "CONST"),
    Opcode("STATE_PREPARATION", 6, "SINGLE", "CONST"),
    Opcode("QUBIT_MEASURE", 7, "SINGLE", "CONST"),

    ## Arbitrary Rotations
    Opcode("RX", 10 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("RY", 11 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("RZ", 12 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("R", 13 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),

    ## Paulis
    Opcode("PAULI_X", 20, "SINGLE", "CONST"),
    Opcode("PAULI_Y", 21, "SINGLE", "CONST"),
    Opcode("PAULI_Z", 22, "SINGLE", "CONST"),

    ## Others
    Opcode("H", 30, "SINGLE", "CONST"),
    Opcode("PHASE", 31 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("T", 32, "SINGLE", "CONST"),
    Opcode("S", 33, "SINGLE", "CONST"),
    Opcode("X", 34, "SINGLE", "CONST"),
    Opcode("Y", 35, "SINGLE", "CONST"),
    Opcode("Z", 36, "SINGLE", "CONST"),
    Opcode("INVT", 37, "SINGLE", "CONST"),
    Opcode("INVS", 38, "SINGLE", "CONST"),
    Opcode("SX", 39, "SINGLE", "CONST"),
    Opcode("SY", 40, "SINGLE", "CONST"),

    Opcode("PIXY", 41 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("PIYZ", 42 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("PIZX", 43 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("SQRT_X", 44, "SINGLE", "CONST"),

    ## Flow commands (still to be considered/not accepted yet)
    Opcode("FOR_START", 50 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("FOR_END", 51 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("IF", 52 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("WHILE", 53 | _Masks.OPCODE_PARAM_MASK.value, "SINGLE", "PARAM"),

    # DUAL WORD Commands
    Opcode("CNOT", 60 | _Masks.OPCODE_DUAL_MASK.value, "DUAL", "CONST"),
    Opcode("SWAP", 61 | _Masks.OPCODE_DUAL_MASK.value, "DUAL", "CONST"),
    Opcode(
        "PSWAP", 62 | (_Masks.OPCODE_DUAL_MASK.value | _Masks.OPCODE_PARAM_MASK.value),
        "DUAL", "PARAM"
    ),
    Opcode("RZZ", 63 | _Masks.OPCODE_DUAL_MASK.value | _Masks.OPCODE_PARAM_MASK.value, "DUAL", "PARAM"),
    Opcode("RXX", 64 | _Masks.OPCODE_DUAL_MASK.value | _Masks.OPCODE_PARAM_MASK.value, "DUAL", "PARAM"),

    # VERSIONING
    Opcode("ID", 1000, "SINGLE", "CONST")
]


def string_to_opcode(op: str) -> Opcode:
    for opcode in _OPCODES:
        if opcode.name == op:
            return opcode
    raise ValueError(f"{op} not found!")


def int_to_opcode(op_code: uint64) -> Opcode:
    for opcode in _OPCODES:
        if opcode.code == op_code:
            return opcode
    raise ValueError(f"{op_code} not found!")


def command_creator(
    op: str, arg0: int = 0, qidx0: int = 0, arg1: int = 0, qidx1: int = 0
) -> uint64:
    """Helper function to create HAL commands.

    Parameters
    ----------
    op : str
        Name of opcode.
    argument : int
        Integer representation of argument value
    qubit : int
        Integer representation of qubit address
    Returns
    -------
    uint64
        64-bit (8 bytes) HAL command.
    """

    opcode = string_to_opcode(op)

    cmd = (
        (opcode.code << _Shifts.OPCODE.value)
        | (arg0 << _Shifts.ARG0.value)
        | qidx0
    )

    if opcode.cmd_type == "DUAL":

        cmd = (
            (_Masks.OPCODE_DUAL_MASK.value << _Shifts.OPCODE.value)
            | (qidx1 << _Shifts.IDX1.value)
            | (arg1 << _Shifts.ARG1.value)
            | (cmd)
        )

    if opcode.cmd_type == "PARAM":
        cmd = cmd | _Masks.OPCODE_PARAM_MASK.value << _Shifts.OPCODE.value

    return cmd


def command_unpacker(
    cmd: uint64
) -> Tuple[str, str, List[int], List[int]]:
    """Helper function to unpack HAL commands.

    Parameters
    ----------
    cmd : uint64
        64-bit (8 bytes) HAL command.

    Returns
    -------
    op : str
        Name of opcode.
    cmd_type: str
        Type of opcode.
    arguments : List[int]
        List of integer representation of argument value(s).
    qubit_indexes : List[int]
        List of integer representation of qubit addresses.
    """

    cmd_op_section = (cmd >> (_Shifts.OPCODE.value))
    opcode = int_to_opcode(cmd_op_section)
    # Extracting args and qubits
    args = []
    qubits = []

    qubits.append(cmd & _Masks.QUBIT0_MASK.value)
    args.append((cmd & _Masks.ARG0_MASK.value) >> _Shifts.ARG0.value)

    if opcode.cmd_type == "DUAL":
        qubits.append((cmd & _Masks.QUBIT1_MASK.value) >> _Shifts.IDX1.value)
        args.append((cmd & _Masks.ARG1_MASK.value) >> _Shifts.ARG1.value)

    return (opcode.name, opcode.cmd_type, args, qubits)


def measurement_unpacker(bitcode: uint64) -> Tuple[int, int, int]:
    """Helper function to decode 64-bit measurement status result from HAL.
    Converts this:
    QUBIT INDEX [63-54] | OFFSET [53-14] | STATUS [13-9] | PADDING [8-1] | VALUE [0]
    to this:
    (QUBIT_INDEX, STATUS, VALUE)

    Parameters
    ----------
    bitcode : uint64
        64-bit measurement status from HAL.
    Returns
    -------
    Tuple[int, int, int]
        Tuple of decoded qubit index, status, and readout value.
    """

    return (
        (bitcode >> 54) + ((bitcode >> 14) & 68719476735),
        (bitcode & 15872) >> 9,
        bitcode & 1
    )
