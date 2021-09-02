HAL Features
============

For this document's purpose, the HAL features are presented as a 
set of commands and a set of metadata. The commands are categorised as 
core, fundamental qubit commands, common across all quantum technologies and 
advanced or optional as defined in this document, which is instead vendor 
implementation specific. 

Required HAL commands
---------------------

The following is a non-exhaustive list of core HAL commands that MAY be extended 
in the future.
Core HAL commands are mandatory and SHOULD be implemented for every system following 
the HAL specification. HAL command support will be conveyed through HAL metadata. 
Core commands MAY be extended in future with the introduction of new universal commands.

Control Commands
----------------
The following table lists control commands that are required to enable advanced functionalities (e.g. multi-users, large addressing).

.. list-table:: Control Commands
    
    * - Command
      - Parameters
      - Description
      - HAL Level
    * - Start of Session
      - Type of Section
      - Defines the type of session, emulator, hardware, simulator. It is used to route the commands to the right destinations.
      - 3-2
    * - End of Session
      - None
      - Closes a session.
      - 3-2
    * - Set Page Qubit0
      - Offset for the qubit index (0)
      - Modifies the offset used in the qubit index computation. The register associated with the offset must be reset by a new Start of Session Command. 
      - All
    * - Set Page Qubit1
      - Offset for the qubit index (1)
      - Modifies the offset used in the qubit index computation. The register associated with the offset must be reset by a new Start of Session Command.  
      - All
    

Single Qubit HAL
----------------

The following table lists the basic single qubit HAL commands.

.. list-table:: Single Qubit HAL

    * - Command
      - Parameters
      - Description
      - HAL Level
    * - NOP
      - None
      - Performs no operation
      - All
    * - State Prepare
      - \|0>\ or \|1>\, qubit address
      - Prepare specific qubit to a known state
      - All
    * - State Prepare all
      - \|0>\ or \|1>\, qubit address
      - Prepares all the qubits to a known state
      - All
    * - Qubit measure
      - None
      - Return the measured state of a qubit
      - All
    * - Arbitrary rotate x
      - Angle
      - Perform qubit rotation [1*]
      - All
    * - Arbitrary rotate y
      - Angle
      - Perform qubit rotation [1*]
      - All
    * - Arbitrary rotate z
      - Angle
      - Perform qubit rotation [1*]
      - All
    * - Pauli-X
      - None
      - None
      - All
    * - Pauli-Y
      - None
      - None
      - All
    * - Pauli-Z
      - None
      - None
      - All
    * - Hadamard
      - None
      - None
      - All
    * - Phase
      - None
      - None
      - All
    * - T
      - None
      - None
      - All


Two Qubits commands
-------------------

The implementation of 2 qubit gates commands across the HAL is for further 
consideration, and it might even be outside the scope of this document. [2*]

.. list-table:: Two Qubit HAL

    * - Command
      - Parameters
      - Description
      - HAL Level
    * - CNOT
      - Qubit addresses
      - Performs a CNOT operation
      - 3

However, implementing core native 2-qubit gate sets will, in most cases, 
be necessary. 
Each vendor should define via optional commands the Level2 and Level1 implementation 
of the CNOT command.

Native two-qubit gates
----------------------

Since native two-qubit gates are necessary to operate at a level 1 HAL, 
hardware vendors SHOULD specify their native gates in the Optional HAL section.

Optional HAL commands [q4]
--------------------------

Commands specific to qubit implementations that are not relevant to others 
or contain potentially confidential information of a specific hardware platform 
are optional. The disclosure of a specific native hardware gate or the hardware 
topology is optional: disclosure to the user will improve performance, but some 
vendors might prefer not to disclose such information.

Additionally, native 2-qubit gates are optional. For example, the RZZ 2-qubit gate or 
the CPHASE gate.

.. list-table:: Optional HAL commands. * For optional commands the hardware provider has to define the HAL level(s) they apply to.
    
    * - Command
      - Parameters
      - Description
      - HAL Level
    * - 32 QBit Measure
      - Starting index of the qubit to read 
      - Returns 32 measurements in parallel.
      - All*
    * - For/If/While
      - To be defined. 
      - Conditional execution. Hardware specific in terms of format and limits
      - All*
    * - Opt1
      - None
      - Optional commands for hardware-specific instructions.
      - Specific.
    * - Opt2
      - None
      - Optional commands for hardware-specific instructions.
      - Specific.

Required HAL responses
----------------------

Users should at least be informed when:

- The circuit completes successfully. Only required at Level3 and Level2 and define as completion ACKNOWLEDGE. 
  
- The commands they have send are INVALID. An example would be CNOT(0,0), a cnot with both inputs being qubit 0;
  
- An error has occurred in the quantum computer and the computation is INCORRECT.

Hardware labs can specify additional error codes to handle specific scenarios.  

The format of the response:

.. list-table:: Response format

    * - Response (4 bits)
      - CIRCUIT ID (12 bits)
    * - Defines the type of error as per Table 
      - Unique ID that identifies user and circuit. Needed in case of multi-user/multi-circuit execution

And the codes for the responses:

.. list-table:: Response codes

    * - Response 
      - VALUE 
      - Description
    * - ACKNOWLEDGE 
      - 0
      - The circuit execution was succesful
    * - INCORRECT 
      - 1
      - The execution encountered an error. Returned measurements should be discarded
    * - INVALID 
      - 2
      - One or more of the commands sent are incorrect. Nothing has been executed.
  
Level-1 access types are not required to return responses as the latency to 
acknowledge them would impact significantly performance and quantum up time.
