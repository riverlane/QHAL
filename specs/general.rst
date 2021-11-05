.. title:: general

Introduction
------------

The main purpose of the HAL is to establish a unified northbound API-based 
framework across different QPU technologies.
The challenges and architectural issues we endeavour to resolve in developing 
the HAL are:

#. Defining the position of Multi-level HAL within the system stack (see :numref:`fig_multi_level_hal` below) [1]_

#. Maximising portability with minimal loss of performance

#. Maximising the range of common features, while keeping the optional, hardware dependent features at a minimum

#. Supporting for advanced features such as compiler optimisations, measurement-based control, and error correction

.. _fig_multi_level_hal:

.. figure:: ./images/image1.png

  Positions of Multi-level HAL layers within the QPU system stack 


The HAL APIs considered in this document MAY be divided into the following groups: [2]_ 

* General APIs
  These are most common APIs across different interfaces and platforms.

  * Register/De-register APIs
  
  * Discover APIs

  * HAL/APIs authentication/authorisation

  * HAL versioning

* Technical area specific (QPU System related)

  * Metadata of the system capabilities/properties

  * Required HAL/QPU commands

  * Optional HAL/QPU hardware specific commands

* Technical area specific (QPU System advanced features related)

  * HAL supported level authentication and authorisation

  * HAL Advanced/Optional features

.. [1]	Metadata is part of the HAL, and in some cases, it seems that data may reflect details of the lowest levels of the QPU stack including some details of the qubit implementation to help guide cross-implementation translation. The CPU could be involved in translation too, especially if it changes across implementations as should be anticipated (example: a constant representing the CPU architecture). If this is correct, then The HAL may cover as much as the whole stack, not just the middle. [Does it need clarifications?]

.. [2]	Are groups and levels disjoint and distinct? Are all groups (or levels) expected to be implemented by all vendors even if they are not all exposed to all customers? Or may vendors choose to build bespoke versions of some in ways that do not coordinate with other components? This could prove relevant if the OS implementation and HAL components are "certified" or "conformant" for use and might even be commercially traded among parties to Deltaflow.OS, since the HAL itself appears to have the option to be closed source software even if Deltaflow.OS itself remains open source. If they are not required to be implemented should some be explicitly denoted as optional, and if they are, then should that be stated here at the start? [Added Multi-Level HAL extra specifications]
