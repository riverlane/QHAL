HAL Features
============

For purposes of this document, the HAL features are presented as a 
set of commands and a set of metadata. The commands are categorised as either 
core, fundamental qubit commands which are common across all quantum technologies, or
advanced or optional as defined in this document, which is specific to the vendor implementation. 

Required HAL commands
---------------------

The following is a non-exhaustive list of core HAL commands that MAY be extended 
in the future.
Core HAL commands are mandatory and SHOULD be implemented for every system following 
the HAL specification. HAL command support will be conveyed through HAL metadata. 
Core commands MAY be extended in future with the introduction of new universal commands. 

Control commands
----------------
The following table lists control commands that are required to enable advanced functionalities (e.g. multi-users, large addressing).

.. list-table:: Control Commands
    :header-rows: 1
    
    * - Command
      - Parameters
      - Description
      - HAL Level
    * - Start of Session
      - Type of Section
      - Defines the type of session, emulator, hardware, simulator. It is used to route the commands to the right destinations.
      - 3-2 \[\*\]
    * - End of Session
      - None
      - Closes a session.
      - 3-2 \[\*\]
    * - Set Page Qubit0
      - Offset for the qubit index (0)
      - Modifies the offset used in the qubit index computation. The register associated with the offset must be reset by a new Start of Session Command. 
      - All
    * - Set Page Qubit1
      - Offset for the qubit index (1)
      - Modifies the offset used in the qubit index computation. The register associated with the offset must be reset by a new Start of Session Command.  
      - All
    
.. \[\*\] Due to the requirment that a Level 1 HAL operates well within qubit decoherence time, it is assumed that the latencies required to implement these commands are too large.

Single-qubit HAL commands
-------------------------

The following table lists the basic single qubit HAL commands.

.. list-table:: Single-qubit HAL commands
    :header-rows: 1

    * - Command
      - Parameters (excluding qubit address)
      - Description
      - HAL Level
    * - NOP
      - None
      - Performs no operation
      - All
    * - State Prepare
      - \|0>\ or \|1>\
      - Prepare specific qubit to a known state
      - All
    * - State Prepare all
      - \|0>\ or \|1>\
      - Prepares all the qubits to a known state
      - All
    * - Qubit measure
      - None
      - Return the measured state of a qubit
      - All
    * - Rx
      - Angle
      - Perform qubit rotation [1]_ about X axis of Bloch sphere
      - All
    * - Ry
      - Angle
      - Perform qubit rotation [1]_ about Y axis of Bloch sphere
      - All
    * - Rz
      - Angle
      - Perform qubit rotation [1]_ about Z axis of Bloch sphere
      - All
    * - X
      - None
      - Perform 180° qubit rotation about X axis of Bloch sphere 
      - All
    * - Y
      - None
      - Perform 180° qubit rotation about Y axis of Bloch sphere 
      - All
    * - Z
      - None
      - Perform 180° qubit rotation about Z axis of Bloch sphere 
      - All
    * - H
      - None
      - Perform Hadamard gate equivalent to Rx(180°) then Ry(90°)
      - All
    * - S
      - None
      - Perform Phase gate equivalent to Rz(90°)
      - All
    * - T
      - None
      - Perform T gate equivalent to Rz(45°)
      - All


Two-qubit HAL commands
----------------------

The implementation of 2 qubit gates commands across the HAL is for further 
consideration, and it might even be outside the scope of this document. [3]_

.. list-table:: Two-qubit HAL commands
    :header-rows: 1

    * - Command
      - Parameters
      - Description
      - HAL Level
    * - CNOT
      - Qubit addresses
      - Performs a Controlled-NOT operation
      - 3

However, implementing core native 2-qubit gate sets will, in most cases, 
be necessary. 
Each vendor should define via optional commands the Level 2 and Level 1 implementation 
of the CNOT command.

Native two-qubit gates
----------------------

Since native two-qubit gates are necessary to operate at a Level 1 HAL, 
hardware vendors SHOULD specify their native gates in the Optional HAL section.

Optional HAL commands
---------------------

Commands specific to qubit implementations that are not relevant to others 
or contain potentially confidential information of a specific hardware platform 
are optional. The disclosure of a specific native hardware gate or the hardware 
topology is optional: disclosure to the user will improve performance, but some 
vendors might prefer not to disclose such information. [4]_

Additionally, native 2-qubit gates are optional. For example, the RZZ 2-qubit gate or 
the CPHASE gate. 

.. list-table:: Optional HAL commands.  
    :header-rows: 1
    
    * - Command
      - Parameters
      - Description
      - HAL Level 
    * - 32 QBit Measure
      - Starting index of the qubit to read 
      - Returns 32 measurements in parallel.
      - All [5]_
    * - For/If/While
      - To be defined. 
      - Conditional execution. Hardware specific in terms of format and limits
      - All [5]_
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

- The circuit completes successfully. Only required at Level 3 and Level 2 and define as completion ACKNOWLEDGE. 
  
- The commands they sent are INVALID. An example would be CNOT(0,0), a CNOT with both inputs being qubit 0;
  
- An error has occurred in the quantum computer and the computation is INCORRECT.

Hardware labs can specify additional error codes to handle specific scenarios.  

The format of the response:

.. list-table:: Response format
    :header-rows: 1

    * - Response (4 bits)
      - CIRCUIT ID (12 bits)
    * - Defines the type of error as per Table 7.6 
      - Unique ID that identifies user and circuit. Needed in case of multi-user/multi-circuit execution

..
  Comment: Manual referece to table below becuase of sphinx bug with Tables and numref

And the codes for the responses:

.. list-table:: Response codes
    :header-rows: 1

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
  
Level 1 access types are not required to return responses as the latency to 
acknowledge them would impact significantly performance and quantum up time.

.. [1]	This is still open for debate and will depend on hardware provider as well as qubit tech. Likely, something to include in metadata rather than specify.
.. [3]	If a vendor conforms to the structure of the HAL for their internal features then they could benefit from examples and some standardisation for their group properties APIs even if not for their implementation.
.. [4]	Consequently, do we want to explicitly state that members of this category may not translate across implementations, resulting in defaulting back to core commands and speeds? [Tentative response in Multi-Level HAL additional considerations] 
.. [5] For optional commands, the hardware provider has to specify the HAL level(s) to which they apply.
