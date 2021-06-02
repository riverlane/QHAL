from enum import Enum, unique
from typing import List, Tuple, Iterable
from numpy import uint64


@unique
class Opcode(Enum):
    """Operational codes for HAL."""

    # OPCODE
    # 15            | 14            | 13:0
    # Single/Dual   | Const/Param   | Code

    SINGLE_MASK = 0 << 15
    DUAL_MASK = 1 << 15

    CONST_MASK = 0 << 14
    PARAM_MASK = 1 << 14

    # SINGLE WORD Commands
    ## Configuration Session
    NOP = (0, "SINGLE", "CONST")
    STATE_PREPARATION = (1, "SINGLE", "CONST")
    STATE_MEASURE = (2, "SINGLE", "CONST")

    ## Rotations
    RX = (10, "SINGLE", "PARAM")
    RY = (11, "SINGLE", "PARAM")
    RZ = (12, "SINGLE", "PARAM")

    ## Paulis
    PAULI_X = (20, "SINGLE", "CONST")
    PAULI_Y = (21, "SINGLE", "CONST")
    PAULI_Z = (22, "SINGLE", "CONST")

    ## Others
    HADAMARD = (30, "SINGLE", "CONST")
    PHASE = (31, "SINGLE", "PARAM")
    T = (32, "SINGLE", "CONST")

    # Flow commands (still to be considered/not accepted yet) - SINGLE WORD Commands
    FOR_START = (50, "SINGLE", "PARAM")
    FOR_END = (51, "SINGLE", "PARAM")
    IF = (52, "SINGLE", "PARAM")
    WHILE = (53, "SINGLE", "PARAM")

    # DUAL WORD Commands
    CNOT = (40, "DUAL", "CONST")
    SWAP = (41, "DUAL", "CONST")
    PSWAP = (42, "DUAL", "CONST")

    # VERSIONING
    ID = (1000, "SINGLE", "CONST")

    def __init__(self, op_code, type, param="CONST"):
        self.op_code = op_code
        self.type = type
        self.param = param

    @property
    def is_single(self):
        return self.type == "SINGLE"

    @property
    def is_dual(self):
        return self.type == "DUAL"

    @property
    def is_parametric(self):
        return self.param == "PARAM"

    @property
    def is_constant(self):
        return self.param == "CONST"

    def encode(self):
        code = self.op_code
        if not self.is_single():
            code = code | self.DUAL_MASK
        if self.is_parametric():
            code = code | self.PARAM_MASK
        return code

    def decode(self):
        code = self.op_code
        if not self.is_single():
            code = code | self.DUAL_MASK
        if self.is_parametric():
            code = code | self.PARAM_MASK
        return code


    def __repr__(self):
        return self.name


class Sizes(Enum):
    """
    All the commands respect the following structure:

    SINGLE_WORD commands:
    OPCODE     |  ARGUMENT      |   QUBIT INDEX
    [63-48]    |  [47-32]       |   [31-0]

    DUAL_WORD commands:
    OPCODE       | PADDING    |   ARGUMENT0  |  ARGUMENT1   | QUBIT_IDX0 | QUBIT_IDX1
    [127-112]    |  [111-96]  |   [95-80]    |  [79-64]     |  [63-32]   |   [31-0]
    """

    # length of single and dual words in bytes
    SINGLE = 8
    DUAL = 16

    # Common
    OPCODE = 2

    # Single (bytes)
    ARG_SINGLE = 2
    QIDX_SINGLE = 4

    # Dual (bytes)
    PADDING_DUAL = 2
    ARG0_DUAL = 2
    ARG1_DUAL = 2
    QIDX0_DUAL = 4
    QIDX1_DUAL = 4


class Shifts(Enum):
    """
     .. TODO:: Missing description.
     """

    OPCODE_SINGLE = 48
    ARG0_SINGLE = 32
    IDX0_SINGLE = 0

    OPCODE_DOUBLE = 112
    ARG0_DOUBLE = 64
    ARG1_DOUBLE = 80
    IDX1_DOUBLE = 32
    IDX0_DOUBLE = 0


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

    if "SINGLE" in Opcode[op].type:
        cmd_h = (
            (Opcode[op].encode() << Shifts.OPCODE_SINGLE.value)
            | (arg0 << Shifts.ARG0_SINGLE.value)
            | qidx0
        )
        cmd_l = 0x0
    else:
        cmd_h = (
            (Opcode[op].encode() << (Shifts.OPCODE_DOUBLE.value - 64))
            | (arg1 << (Shifts.ARG1_DOUBLE.value - 64))
            | (arg0 << (Shifts.ARG0_DOUBLE.value - 64))
        )
        cmd_l = (qidx1 << Shifts.IDX1_DOUBLE.value) | (
            qidx0 << Shifts.IDX0_DOUBLE.value
        )
    return (cmd_h, cmd_l)


def command_unpacker(cmd: Tuple[uint64,uint64]) -> Tuple[str, List[int], List[int]]:
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
    try:
        opcode = Opcode((op, "SINGLE", "CONST"))
    except:
        opcode = Opcode((op, "DUAL", "CONST"))

    # Extracting args
    args = []
    qubits = []
    if opcode.type == "SINGLE":
        
        args.append(
            int.from_bytes(cmd[idx : idx + Sizes.ARG_SINGLE.value], byteorder="big")
        )
        idx += Sizes.ARG_SINGLE.value
        qubits.append(int.from_bytes(cmd[idx:], byteorder="big"))
    else:
        idx += Sizes.PADDING_DUAL.value
        args.append(
            int.from_bytes(cmd[idx : idx + Sizes.ARG0_DUAL.value], byteorder="big")
        )
        idx += Sizes.ARG0_DUAL.value
        args.append(
            int.from_bytes(cmd[idx : idx + Sizes.ARG1_DUAL.value], byteorder="big")
        )
        idx += Sizes.ARG1_DUAL.value
        qubits.append(
            int.from_bytes(cmd[idx : idx + Sizes.QIDX0_DUAL.value], byteorder="big")
        )
        idx += Sizes.QIDX0_DUAL.value
        qubits.append(int.from_bytes(cmd[idx:], byteorder="big"))

    return (opcode.name, args, qubits)


def hal_command_sequence_decomposer(cmd: bytes) -> (bytes, bytes):
    """ Decompose hal command sequence in lead word an remainder, return both.

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

def measurement_unpacker(bitcode: uint64, qubits: Iterable) -> List:
    pass