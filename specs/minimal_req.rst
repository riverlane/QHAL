HAL Commands Minimal Requirements
=================================

To allow for the best usage of resources while preserving the desired user intents, 
we should allow each HAL layer to have a different set of commands. 
This allows a tuning of the commands to fit the associated level best.
In this Section we have used the following considerations to drive our proposal:

- Level 3 and Level 2 need to perform one or more compilation, transpilation and 
  timing allocation of instructions. Level 1 instead should present commands that 
  are already usable by the hardware.
- Users will want to execute on emulation as well as on real quantum resources. 
  Hardware vendors might want to expose a single HAL interface and internally route 
  the circuits to an emulator or the real system. To ease this process and consequently 
  allocation, billing and scheduling, Level 2 and Level 3 HAL should have exposed 
  this concept.
- We don't believe the user needs a complete set of traditional sequence modifiers 
  (for, while, do etc) but just the bare minimum to express repetition and branching. 
  We are suggesting for and if statement to achieve that.

Level 3 HAL
-----------

"Able to run large batches of circuits"

.. list-table:: Level 3 HAL commands

    * - Command
      - Motivations
      - Implications
      - Notes
    * - A universal gateset
      - Define the circuits to execute
      - Compilers and transpilers are needed to convert it to a usable representation
      - None
    * - Section commands
      - Confines the code that belong to one user and associate it to hardware or emulation facilities
      - The compilation flow should support both targets
      - The user can transmit circuits back-to-back as a binary sequence. Section commands are used to delimite these sequences (as a START and STOP equivalent) allowing optimizatons and compilations on the received circuits.

At Level 3, the classical logic is in charge of acting upon measurements and 
selecting the next sequence of circuits to execute. 
Circuits can be fully precompiled and buffered. 
Acceptance criteria may be applied to the provided code to verify that it is 
within the capabilities of the compiler and the hardware.

Requires:

- Validation of the user-provided algorithm to access its feasibility
  
- Highly parallelised compilation flow to avoid execution underflowing and suboptimal 
  utilisation of the quantum hardware.

Level 2 HAL
-----------

"The results of a single circuit and small batches of circuits can be acted upon."

.. list-table:: Level 2 HAL commands 

    * - Command
      - Motivations
      - Implications
      - Notes
    * - A native gateset
      - Define the circuits to execute
      - Transpilers are needed to convert it to a hardware representation (e.g. sequence of pulses)
      - It can contain optional commands (e.g. CPHASE, CCX, ACTIVE RESET) that the hardware supports

At Level 2, the classical logic is in charge of acting upon measurements and select the next circuit(s) to execute. 

Requires:

- Parallel compilation of circuits to handle branching statements
  
- Low overhead repetition/reloading of the same circuit

Level 1 HAL
-----------

"Results of qubit measurement can be acted upon within a single circuit."

.. list-table:: Level 1 HAL commands 

    * - Command
      - Motivations
      - Implications
      - Notes
    * - A native gateset
      - Define the circuits to execute
      - None
      - If the hardware supports them the user should be allowed to use: (a) arbitrary controlled gates (e.g. CPHASE) (b) multi (>2) qubits gates 

At Level 1, the classical logic is in charge of acting upon measurements and select the next gate(s) to execute. 

Requires:

- Fast conversion of native gateset representation to hardware controls
  
- Fast loading of these sequences
  
- Fast path from measurement to user logic
      