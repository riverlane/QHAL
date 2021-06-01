Optional HAL packages/modules
=============================

The following modules MAY be considered in the future releases.

Boson sampling HAL commands for Photonic Qubits
-----------------------------------------------

Boson Sampling is a catchall term for a set of NISQ devices in hardware 
based on today's photonic technologies.

HAL Transpiler Module support
-----------------------------

CNOT gates are implemented on hardware using sets of native gates. 
Therefore, a transpile step is required to transform a CNOT gate into 
hardware compatible gate sequences. It is also possible to perform optimisation, 
converting native gate sequences into an equivalent but shorter circuit. 
The transpiler would generate circuits comprised of Level 1 commands.
