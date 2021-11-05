Use Case Scenarios
==================

To demonstrate the need for multiple HAL levels and the algorithms 
that can be run on each level, we provide example pseudocodes of the following algorithms:

1.  Shor's Algorithm: Using Kitaev's Quantum Fourier Transform (QFT) approach, 
    the qubit count of the quantum circuits run as part of Shor's Algorithm can 
    be reduced. However, this reduction in qubit count needs to be compensated for 
    by performing intermediate measurements on the QFT qubit and also applying 
    rotation gates conditional on intermediate measurement results [1]_. 
    Hence, this algorithm will require Level 1 HAL access. 

2.  HoloVQE: Circuits run as part of the HoloVQE algorithm [2]_ require 
    intermediate measurements on qubits and require intermediate qubit resets. 
    For a user to implement active qubit reset themselves, they will 
    require HAL Level 1 access due to the very low latency required. However, some hardware manufacturers may want to provide active qubit reset capabilities themselves as a HAL Level 2/Level 3 command. Hence, this is an example of an algorithm that will require HAL Level 2/3 depending on the available optional HAL command.
    
The pseudocodes are given in Appendix 2. Further use cases will be added in the future versions of this document, for example a minimal example of a conventional VQE code, and a minimal example of an alpha-VQE code.

.. [1] Monz, Thomas, et al. "Realisation of a scalable Shor algorithm." Science 351.6277 (2016): 1068-1070.
.. [2] Foss-Feig, Michael, et al. "Holographic quantum algorithms for simulating correlated spin systems." https://arxiv.org/abs/2005.03023 (2020).