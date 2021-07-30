"""
All the commands respect the following structure:

SINGLE_WORD commands:
OPCODE     |  ARGUMENT      |   QUBIT INDEX
[63-48]    |  [47-32]       |   [31-0]

DUAL_WORD commands:
OPCODE       | PADDING    |   ARGUMENT0  |  ARGUMENT1   | QUBIT_IDX0 | QUBIT_IDX1
[127-112]    |  [111-96]  |   [95-80]    |  [79-64]     |  [63-32]   |   [31-0]

OPCODE is structured as:
SINGLE/DUAL | CONSTANT/PARAMETRIC   |   OPCODE
[15]        |   [14]                |   [13-0]

"""

from enum import Enum, unique
from typing import List, Tuple, Iterable
from numpy import uint64


class _Shifts(Enum):
    """
    Defines the position of the command subfields.
    """
    OPCODE_TYPE = 63

    OPCODE = 48
    ARG0_SINGLE = 32
    IDX0_SINGLE = 0

    OPCODE_DOUBLE = 112
    ARG0_DOUBLE = 0
    ARG1_DOUBLE = 16
    IDX1_DOUBLE = 32
    IDX0_DOUBLE = 0


class _Masks(Enum):
    """ Masks used to decompose the commands """

    QUBIT0_MASK = 0xFFFF
    QUBIT1_MASK = 0xFFFF
    ARG1_MASK = 0xFFFF
    ARG0_MASK = 0xFFFF
    SINGLE_MASK = 0x0000
    DUAL_MASK = 0x8000
    CONST_MASK = 0x0000
    PARAM_MASK = 0x4000
    OPCODE_MASK = 0xFFFF
    TYPE_MASK = 0x1


class Opcode:
    def __init__(self, name, op_code, type, param):
        self.name = name
        self.op_code = op_code
        self.type = type
        self.param = param
        self._validate()

    def _validate(self):
        if self.type == "DUAL":
            assert (self.op_code & _Masks.DUAL_MASK.value != 0)
        else:
            assert (self.op_code & _Masks.DUAL_MASK.value == 0)
        if self.param == "PARAM":
            assert (self.op_code & _Masks.PARAM_MASK.value != 0)
        else:
            assert (self.op_code & _Masks.PARAM_MASK.value == 0)


_OPCODES = [
    # SINGLE WORD Commands
    ## Configuration Session
    Opcode("NOP", 0, "SINGLE", "CONST"),
    Opcode("STATE_PREPARATION_ALL", 1, "SINGLE", "CONST"),
    Opcode("STATE_PREPARATION", 2, "SINGLE", "CONST"),
    Opcode("QUBIT_MEASURE", 3, "SINGLE", "CONST"),

    Opcode("RX", 10 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("RY", 11 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("RZ", 12 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("R", 13 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),

    ## Paulis
    Opcode("PAULI_X", 20, "SINGLE", "CONST"),
    Opcode("PAULI_Y", 21, "SINGLE", "CONST"),
    Opcode("PAULI_Z", 22, "SINGLE", "CONST"),

    ## Others
    Opcode("H", 30, "SINGLE", "CONST"),
    Opcode("PHASE", 31 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("T", 32, "SINGLE", "CONST"),
    Opcode("S", 33, "SINGLE", "CONST"),
    Opcode("X", 34, "SINGLE", "CONST"),
    Opcode("Y", 35, "SINGLE", "CONST"),
    Opcode("Z", 36, "SINGLE", "CONST"),
    Opcode("INVT", 37, "SINGLE", "CONST"),
    Opcode("INVS", 38, "SINGLE", "CONST"),
    Opcode("SX", 39, "SINGLE", "CONST"),
    Opcode("SY", 40, "SINGLE", "CONST"),

    Opcode("PIXY", 41 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("PIYZ", 42 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("PIZX", 43 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("SQRT_X", 44, "SINGLE", "CONST"),

    ## Flow commands (still to be considered/not accepted yet)
    Opcode("FOR_START", 50 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("FOR_END", 51 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("IF", 52 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),
    Opcode("WHILE", 53 | _Masks.PARAM_MASK.value, "SINGLE", "PARAM"),

    # DUAL WORD Commands
    Opcode("CNOT", 60 | _Masks.DUAL_MASK.value, "DUAL", "CONST"),
    Opcode("SWAP", 61 | _Masks.DUAL_MASK.value, "DUAL", "CONST"),
    Opcode(
        "PSWAP", 62 | (_Masks.DUAL_MASK.value + _Masks.PARAM_MASK.value),
        "DUAL", "PARAM"
    ),

    # VERSIONING
    Opcode("ID", 1000, "SINGLE", "CONST")
]


def string_to_command(command: str) -> Opcode:
    for opcode in _OPCODES:
        if opcode.name == command:
            return opcode
    raise ValueError(f"{command} not found!")


def _opcode_to_command(op_code: uint64) -> Opcode:
    for opcode in _OPCODES:
        if opcode.op_code == op_code:
            return opcode
    raise ValueError(f"{op_code} not found!")


def command_creator(
    op: str, arg0: int = 0, qidx0: int = 0, arg1: int = 0, qidx1: int = 0
) -> Tuple[uint64]:
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
    List[uint64]
        Tuple of 2 64-bit (8 bytes) parts of the command. Upper and lower half.
    """

    command = string_to_command(op)

    if "SINGLE" in command.type:
        cmd_h = (
            (command.op_code << _Shifts.OPCODE.value)
            | (arg0 << _Shifts.ARG0_SINGLE.value)
            | qidx0
        )
        cmd_l = 0x0
    else:
        cmd_h = (
            (command.op_code << (_Shifts.OPCODE.value))
            | (arg1 << (_Shifts.ARG1_DOUBLE.value))
            | (arg0 << (_Shifts.ARG0_DOUBLE.value))
        )
        cmd_l = (qidx1 << _Shifts.IDX1_DOUBLE.value) | (
            qidx0 << _Shifts.IDX0_DOUBLE.value
        )
    return (cmd_h, cmd_l)


def command_unpacker(
    cmd: Tuple[uint64, uint64]
) -> Tuple[str, List[int], List[int]]:
    """Helper function to unpack HAL commands.

    Parameters
    ----------
    cmd : Tuple[uint64,uint64]
        Tuple of 2 64-bit (8 bytes) parts of the command. Upper and lower half.

    Returns
    -------
    op : str
        Name of opcode.
    arguments : List[int]
        Integer representation of argument value.
    qubit_indexs : List[int]
        Integer representation of qubit address.
    """
    cmd_hi, cmd_low = cmd
    # Dual command
    cmd_type = cmd_hi >> (_Shifts.OPCODE_TYPE.value) & _Masks.TYPE_MASK.value
    cmd_code = (cmd_hi >> (_Shifts.OPCODE.value)) & _Masks.OPCODE_MASK.value

    command = _opcode_to_command(cmd_code)

    # Extracting args
    args = []
    qubits = []
    if command.type == "SINGLE":
        args.append(
            (cmd_hi >> _Shifts.ARG0_SINGLE.value) & _Masks.ARG0_MASK.value
        )
        qubits.append(cmd_hi & _Masks.QUBIT0_MASK.value)
    else:
        args.append(
            (cmd_hi >> _Shifts.ARG1_DOUBLE.value) & _Masks.ARG1_MASK.value
        )
        args.append(
            (cmd_hi >> _Shifts.ARG0_DOUBLE.value) & _Masks.ARG0_MASK.value
        )
        qubits.append(
            (cmd_low >> _Shifts.IDX1_DOUBLE.value) & _Masks.QUBIT1_MASK.value
        )
        qubits.append(cmd_low & _Masks.QUBIT0_MASK.value)

    return (command.name, args, qubits)


def measurement_unpacker(bitcode: uint64) -> Tuple[int, int, int]:
    """Helper function to decode 64-bit measurement status result from HAL.
    Converts this:
    QUBIT INDEX [63-32] | STATUS [31-27] | PADDING [26-1] | VALUE [0]
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
        bitcode >> 32,
        (bitcode & 4294967295) >> 32,
        bitcode & 1
    )


def hal_command_sequence_decomposer(
    cmd: Tuple[uint64, uint64]
) -> Tuple[bytes, bytes]:
    """ Decompose hal command sequence in lead word an remainder, return both.
    TODO: is this function required?

    Parameters
    ----------
    cmd : bytes
        sequence of 64-bit or 128-bit HAL commands

    Returns
    -------
    hal_cmd : bytes
        64-bit or 128-bit HAL command
    cmd_remainder : bytes
        sequence of 64-bit or 128-bit HAL commands with lead word removed
    """
    idx = Sizes.OPCODE.value
    op = int.from_bytes(cmd[:idx], byteorder="big")
    # Initial way to retrieve the value
    try:
        opcode = Opcode((op, "SINGLE"))
    except ValueError:
        opcode = Opcode((op, "DUAL"))

    # Extracting args
    if opcode.type == "SINGLE":
        idx = Sizes.SINGLE.value
    else:
        idx = Sizes.DUAL.value

    return cmd[:idx], cmd[idx:]
