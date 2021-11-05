.. title:: hal_architecture

HAL Architecture
----------------

Introduction
============

The HAL allows algorithm developers to abstract away the details of a 
hardware implementation by providing a standard set of commands which 
can be implemented to some degree on most devices. 
This brings two benefits:

- the developer can focus on the algorithm as opposed to the implementation.
  
- the algorithm can be easily ported to other devices. 
  
Basic quantum algorithms and software use a high-level HAL representing a circuit 
model, which means taking advantage in a controlled way of advanced hardware 
capabilities. There are now algorithms being developed that require functionalities 
which this circuit model does not support. 

In general, it is because they require some functionality that cannot be implemented 
by a classical CPU model connected over some high latency link (e.g. the cloud) 
to a quantum device. These algorithms require much quicker communication between 
a classical controller and device to be efficient and/or access to some native 
functionalities of the device.

Multi-level HAL and associated algorithms
=========================================

The HAL must be capable of supporting advanced algorithms with different 
degrees of quantum/classical interaction. Current algorithms can be 
classified into three main groups according to requirements on classical 
to quantum latency. We associate these groups to three levels of HAL as follows.

The highest level is 3, which supports the ability to run large batches of static circuits. 
This is implementable in a setting with high latency, typically much larger 
than the decoherence time, and is equipotent to commercial quantum devices 
available over the cloud.

In Level 2, there is no change to the quantum device's abilities, 
but the latency of the classical control is now on the order 
of qubit decoherence time. 
The controlling hardware can now make circuit updates based upon the results of
a single circuit, without significant qubit "dead time".

In Level 1, the ability to make mid-circuit measurements, and control of 
the QPU based on the measurement outcome, is included. 
This requires the controlling device to make changes or store results on the quantum device, 
on the order of gate time and hence well below the decoherence time, 
so communication must also be of very low latency. 
The following table summarises the HAL three levels, and the timescales and 
corresponding algorithms considered in the first version of the specification. 
A general aim is to define a multi-level HAL flexible enough to cater to 
future developments and additions. [1]_

    
.. list-table:: HAL Levels
    :header-rows: 1

    * - HAL Level
      - Timescale
      - Ability
    * - 3
      - Slow, communication between server and QPU (timescale much longer than coherence time)
      - Able to run large batches of circuits (e.g., may contain thousands of shots). Equipotent to what is available via IBM cloud, AWS, etc. Much slower than the coherence time. Supported algorithms: Gradient-free VQE.
    * - 2
      - Faster, communication between QPU and controller (timescale on the order of coherence time)     
      - Actions can be taken based on the results of a single circuit and small batches of circuits 
        (e.g., may contain tenths of shots).
        This usually cannot be done in Level 1 due to the bandwidth or latency issues encountered 
        when making decisions on small numbers of circuits. Operates within coherence time.
    * - 1
      - Fastest, within decoherence time of qubits (timescale much shorter than coherence time)     
      - Results of qubit measurement can be acted upon within a single circuit. This requires the HAL to be implemented via fast local control elements (e.g. FPGAs, application-specific CPUs). 
        Supported algorithms: QNN dropout, holo-VQE, quantum autoencoder, simple error correction.


Multi-level HAL extra considerations
====================================

It is important to raise awareness of the following considerations:

- Hardware companies can expose one or more of the HAL levels
- Companies may want to expose a high HAL level publicly, 
  but only expose a lower HAL level to selected partners or customers.
  In this case, care should be taken to implement public level(s) as per specifications. 
  A potential benefit of this approach: 
  A hardware company can outsource the development of applications to preferred developers, 
  to whom privileged low-level HAL access is given. 
- Metadata should allow the conversion of a sequence of HAL commands across 
  architectures and layers. Each conversion must come with an associated set 
  of acceptance checks that the user/hardware company can execute. 
  In order of complexity, we envision:

  - Metadata checks. The conversion can be checked for feasibility by simply examining the metadata with no compilation. 
   
    - Example of conversion: from a Level 3 HAL representation targeting different hardware.
    
    - Example of check: the number of qubits and circuit depth required must be available on the new target architecture.
   
  - Compilation checks. A conversion that needs to be remapped to a new gate set and analysed to understand if they meet the hardware constraints. 
   
    - Example of conversion: from a Level 2 representation, Hardware A to a Level 2, Hardware B
   
    - Example of check: verify all original gates can be transpiled into Hardware B native gateset

  - Performance checks. In the case of guaranteed QoS (for example, on error rates), conversions need to analyse the final solution's performance. 
    
    - Example of conversion: from a Level 2 representation, Hardware A to a Level 2, Hardware B with user expecting final fidelity > X.
    
    - Example of check: on top of the compilation checks, verify that the transpiled version of the circuit can meet the QoS requirement by using single- and two-qubit fidelities of Hardware B.

.. [1]	Again, are we going to encourage vendors to follow the level structure for their internal use, even if they don't expose them to any customers? Is Level 3 mandatory? Is Level 2 encouraged? Is Level 1 truly optional? Is there an implication that some or all levels may be licensed? Is it anticipated that some vendors may choose to open source their implementations? It is likely that there will be a need to validate the authenticity of any level for supply chain and security-related reasons. [Tentative response in Multi-Level HAL additional considerations] 
