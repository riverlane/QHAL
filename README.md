# QHAL - Quantum Hardware Abstraction Layer

## Scope and Purpose

This document sets out a Hardware Abstraction Layer (HAL) 
for quantum computers (QHAL) based on four leading qubit technologies: 
superconducting qubits, trapped-ion qubits, photonic systems
and silicon-based qubits. 
The aim is to define a multi-level HAL that makes software portable 
across platforms but not at the cost of performance. 
The HAL allows high-level quantum computer users, such as application 
developers, platform and system software engineers, cross-platform 
software architects, to abstract away the hardware implementation details 
while keeping the performance.

## Disclaimer

This specification must be considered a work in progress. 
The document is currently used to guide discovery, initiate discussion 
and enable future improvements. Even though all the parties involved 
are putting their best efforts on verifying the validity and correctness 
of what is stated, extensive reviews are still to be conducted.
This disclaimer will be removed once the document reaches sufficient maturity.

## Contributors

| Company/Entity                    |
| --------------------------------- |
| ARM                               |
| Duality Quantum Photonics (DQP)   |
| Hitachi Europe Ltd        (HEU)   |
| National Physical Laboratory (NPL)|
| Oxford Ionics (OI)                |
| Oxford Quantum Circuits (OQC)     |
| Riverlane (RL)                    |
| Seeqc                             |
| Universal Quantum (UQ)            |

## Current version

The specification file gets updated every time a merge into the dev branch happens.
Any PR that entails a change to the specification PDF document will not get built
until merged into the dev branch, so during a PR any changes on the PDF that need
to be inspected can be viewed as an artifact of this [workflow](https://github.com/riverlane/QHAL_internal/actions/workflows/specs_merge_pdf_build_check.yml).
See [specification](specifications.pdf) for the latest version. 

## Testing framework and code examples

More information are provided at [code and testing](code_and_testing.md)


## License 

see License [here](LICENSE)

[![Ochrona](https://img.shields.io/badge/secured_by-ochrona-blue)](https://ochrona.dev)
