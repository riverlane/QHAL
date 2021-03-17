# Hardware Abstraction Layer

This repository provides the "canonical" code definition of the Hardware
Abstraction Layer.

## Example Code Usage
```
from lib.hal import HardwareAbstractionLayer, command_creator, measurement_unpacker
from lib.quantum_simulators import ProjectqQuantumSimulator

# set up the HAL
hal = HardwareAbstractionLayer(
    ProjectqQuantumSimulator(1)
)

# set up list of commands
command_list = [
    command_creator("STATE_PREPARATION"),
    command_creator("RX", 256, 0)
]

for command in command_list:
    hal.accept_command(command)

# final measurement command
measurement_res = hal.accept_command(command_creator("STATE_MEASURE"))
print(measurement_unpacker(measurement_res, [0]))
```


## Development
We recommend development using VSCode Docker tools, with the `.devcontainer/devcontainer_template.json`.

Alternatively, to manually build the Docker image run:
```
make build
```
From there you may develop inside a Docker container built from the resulting image.