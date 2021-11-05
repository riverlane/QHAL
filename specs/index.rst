.. title:: Overview

Hardware Abstraction Layer (HAL)
================================

Scope and Purpose
-----------------

This document sets out a Hardware Abstraction Layer (HAL) 
for quantum computers based on four leading qubit technologies: 
superconducting qubits, trapped-ion qubits, photonic systems
and silicon-based qubits. 
The aim is to define a multi-level HAL that makes software portable 
across platforms but not at the cost of performance. 
The HAL allows high-level quantum computer users, such as application 
developers, platform and system software engineers, cross-platform 
software architects, to abstract away the hardware implementation details 
while keeping the performance.

This document defines the HAL levels, categorised by the types of applications 
that they enable. 
The definition includes the general HAL architecture, HAL features 
(e.g. which commands need to be implemented) and the HAL specification format. 
The document does not define the HAL implementation or how to compile/transpile 
between the different levels. This document is a part of the NISQ.OS ISCF project as 
a collaborative effort of ARM, Duality Quantum Photonics, Hitachi Europe Limited, 
the National Physical Laboratory, Oxford Ionics, Oxford Quantum Circuits, 
Riverlane, Seeqc, and Universal Quantum. 
    
This joint project's commitment is to implement applications that 
require the fastest classical/quantum interaction, such as measurement 
and control-based applications and error correction. 
Deltaflow.OS, the operating system for quantum computers which will be developed 
within the ISCF NISQ.OS project, builds on this open HAL specification. 
    
The HAL is to be an open standard on which other parties can also build. 
One aim of the ISCF project is to engage in international standardisation 
efforts with this HAL.

.. list-table:: Contributors
    :header-rows: 1

    * - Company/Entity
    * - ARM
    * - Duality Quantum Photonics (DQP)
    * - Hitachi Europe Ltd (HEU)
    * - National Physical Laboratory (NPL)
    * - Oxford Ionics (OI)
    * - Oxford Quantum Circuits (OQC)
    * - Riverlane (RL)
    * - Seeqc
    * - Universal Quantum (UQ)


Disclaimer
==========
    
This specification must be considered a work in progress. 
The document is currently used to guide discovery, initiate discussion 
and enable future improvements. Even though all the parties involved 
are putting their best efforts on verifying the validity and correctness 
of what is stated, extensive reviews are still to be conducted.
This disclaimer will be removed once the document reaches sufficient maturity.


.. toctree::
    :maxdepth: 2
    :caption: Contents
    :hidden:

    glossary
    general
    hal_architecture
    metadata
    minimal_req
    hal_features
    hal_commands_specifications
    security
    optional_packages
    standards
    use_case_scenarios
    appendix1
    appendix2
    further_reading


