Use Case scenarios
==================

[UC]
To demonstrate the need for multiple HAL levels and the algorithms 
that can be run on each level, we provide example pseudocodes of the following algorithms:

1. Shor's Algorithm: Using Kitaev's Quantum Fourier Transform (QFT) approach, 
    the qubit count of the quantum circuits run as part of Shor's Algorithm can 
    be reduced. However, this reduction in qubit count needs to be compensated for 
    by performing intermediate measurements on the QFT qubit and also applying 
    rotation gates conditional on intermediate measurement results [REF_4]. 
    Hence, this algorithm will require level 1 HAL access. 

Pseudocode in Appendix 2: Use Case 1 – Shor's Algorithm.

1. HoloVQE: Circuits run as part of the HoloVQE algorithm [REF_5] require 
    intermediate measurements on qubits and require intermediate qubit resets. 
    For a user to implement active qubit reset themselves, they will 
    require HAL level 1 access due to the very low latency required. However, some hardware manufacturers may want to provide active qubit reset capabilities themselves as a HAL level 2/level 3 command. Hence, this is an example of an algorithm that will require HAL level 2/3 depending on the available optional HAL command.  The OpenQASM pseudocode is given in Appendix 3: Use Case 2 – holoVQE.
    Further use cases will be added in the future versions of this document, for example a minimal example of a conventional VQE code, and a minimal example of an alpha-VQE code.
