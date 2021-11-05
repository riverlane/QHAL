Appendix 1
==========

Notes and questions 
-------------------

1. How will metadata be implemented in other systems? Is this info stored in a config file? Assuming an application developer is writing an algorithm that then needs to be built to run on hardware, it would make sense that this data is store on the user's machine and used to compile and build?

2. Is metadata confined to static information that is especially useful at initialisation time? Does it include dynamic properties? Can it be extended by the vendor to include information that is specific to a specific machine, such as the calibration and quality of specific qubits hints that can be used by algorithm developers to select how to distribute computation across the qubits made available to them or even for the OS to allocate qubits based on quality or length of computation or even cost to the application customer for their use. These factors could make it important to authenticate such information. Therefore, should the metadata also be decomposed into "levels" of revelation? [Should be addressed by the Section Metadata Specification]

3. Should we have controlled rotation gates? [Added to the Notes on commands Layer 2 and 1]

4. Multi-user and session management – should this be part of the specification? [Addressed by HAL Commands Minimum Requirements]

5. Should qubit indices be handled as indices rather than bit fields? [Addressed in Command Format: Option I]

6. Should we include gates with more than two qubits? ? [Added to the Notes on commands Layer 2 and 1]

7. Add a command to the standard regarding selection of the backend - emulator or hardware. Deltaflow.OS can utilise this command to select a backend for HAL Software to run the algorithms on? [Addressed by HAL Commands Minimum Requirements]
