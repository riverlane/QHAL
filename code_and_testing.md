# Code implementation and testing environment

A representative implementation of some of the main concepts defined in the [specifications](specifications.pdf) is provided in [lib](lib). 

The code is tested for correctness via a set of direct tests. 

The testing framework leverages Docker and makefiles to install all the dependencies required. 
It has been tested on Linux and MacOs platforms. 
For more information on Docker and how to install it [docs](https://docs.docker.com).

**Test Execution**

To execute all the tests run from a terminal:

```sh
 make tests
```

**Example usage**

The QHAL allows different backends to be connected. In the following example we have a 3 qubits system simulated via ProjectQ.

```python
from lib import HardwareAbstractionLayer, ProjectqQuantumSimulator
from lib.hal import command_creator, measurement_unpacker

# set up HAL using projectq backend for 3 qubits
hal = HardwareAbstractionLayer(
    ProjectqQuantumSimulator(3)
)

# prepare commands
circuit = [
    ["STATE_PREPARATION", 0, 0],
    ['X', 0, 0],
    ['H', 0, 2],
    ["T", 0, 0],
    ["SX", 0, 1],
    ["T", 0, 2],
    ["S", 0, 2],
    ["SWAP", 1, 2],
    ["T", 0, 2],
    ["INVS", 0, 2],
    ['RZ', 672, 1],
    ['SQRT_X', 0, 0],
    ['PSWAP', 200, 0, 0, 1],
    ["CNOT", 0, 2],
    ["H", 0, 2],
    ["PIXY", 458, 1],
]

# send commands to HAL
for commands in circuit:

    hal_cmd = command_creator(*commands)
    hal.accept_command(hal_cmd)

# send measure command to HAL and get encoded HAL result
hal_result = hal.accept_command(command_creator(*['QUBIT_MEASURE', 0, 2]))

# decode hal result and print qubit index, status, readout
print(measurement_unpacker(hal_result))
```
