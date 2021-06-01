.. title:: hal_architecture

HAL Architecture
----------------

Introduction
------------

The HAL allows algorithm developers to abstract away the details of a 
hardware implementation by providing a standard set of commands which 
can be implemented to somedegree on most devices. 
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
reconducted into three main groups with growing requirements in classical 
to quantum latency. We associate these groups to three levels of HAL as follows.

The highest level is 3, the ability to run large batches of a static circuit. 
This is implementable in a setting with high latency, typically much larger 
than the decoherence time, and is equipotent to commercial quantum devices 
available over the cloud.

In level 2, there is no change to the quantum 
device's abilities, but the latency of the classicalcontrol is now in order 
of qubit decoherence time. 
The controlling hardware can now make circuit updates based upon a single 
circuit's results, without a significant proportion of qubit "dead time".

In level 1, the ability to make mid circuit measurements, and control of 
the QPU based on the measurement outcome, is included. 
This requires the controlling device to make changes or store results on 
the gate time order on the quantum device and hence well below the 
decoherence time, so communication must also be of very low latency. 
The following table summarises the HAL levels 3-1, the timescales and 
corresponding algorithms considered in the first version of the specification. 
A general aim is to define a multi-level HAL flexible enough to cater to 
future developments and additions. [q3]

    
.. list-table:: HAL Levels

    * - HAL Level
      - Timescale
      - Ability
    * - 3
      - Slow, communication between server and QPU (timescale much longer than coherence time)
      - Able to run large batches of circuits (e.g., may contain thousands of shots). Equipotent to what is available via IBM cloud, AWS, etc.Much slower than the coherence timeSupported algorithms: Gradient-free VQE
    * - 2
      - Faster, communication between QPU and controller (timescale in order of the coherence time)     
      - Actions can be taken based on the results of a single circuit and small batches of circuits 
        (e.g., may contain tenths of shots). 
        This usually cannot be done in level 1 due to the bandwidth or latency issues encountered 
        when making decisions on small numbers of circuits. Operates within coherence time.
    * - 1
      - Fastest, within decoherencetime of qubits (timescale much shorter than the coherence time)     
      - Results of qubit measurement can be acted upon within a single circuit. This requires the HAL to be implemented via fast local control elements (e.g. FPGAs, application-specific CPUs).Supported algorithms: QNN dropout, holo-VQE, quantum autoencoder, simple error correction


Multi-level HAL extra considerations
====================================

It is important to raise awareness of the following considerations:

- Hardware companies can expose one or more of the HAL levels
- Companies might want to certify the hidden levels (i.e., those considered 
  private and not exposed). In this case, care should be taken to implement 
  the levels above the exposed ones as per specifications. 
  An example of this approach's benefit: hardware company can outsource the 
  development of applications to a group of developers already familiar 
  with designing solutions at HAL Level 1-2-3, with a level of access 
  lower than the public one. 
- Metadata should allow the conversion of a sequence of HAL commands across 
  architectures and layers. Each conversion must come with an associated set 
  of acceptance checks that the user/hardware company can execute. 
  In order of complexity, we envision:
  d
  - Metadata checks. The conversion can be checked for feasibility by simply examining the metadata with no compilation. 
   
    - Example of conversion: from a Level 3 HAL representation targeting different hardware.
    
    - Example of check: the number of qubits and circuit depth required must be available on the new target architecture.
   
  - Compilation checks. A conversion that needs to be remapped to a new gate set and analysed to understand if they meet the hardware constraints. 
   
    - Example of conversion: from a Level 2 representation, Hardware A to a Level 2, Hardware B
   
    - Example of check: verify all original gates can be transpiled into Hardware B native gateset

  - Performance checks. In the case of guaranteed QOS (for example, on error rates), conversions need to analyse the final solution's performance. 
    
    - Example of conversion: from a Level 2 representation, Hardware A to a Level 2, Hardware B with user expecting final fidelity > X.
    
    - Example of check: on top of the compilation checks, verify that the transpiled version of the circuit can meet the QoS requirement by usingsingle and two qubits fidelities.
