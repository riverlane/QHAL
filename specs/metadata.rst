.. title:: metadata

Metadata Format Specification
=============================

General
-------

The primary purpose of Metadata is to:

- Allow the hardware companies to defend their trade secrets

- Allow the users to identify the hardware platform most suitable for their problems and utilise it to its best
  
- Discourage independent efforts to extract/infer undisclosed information. 
  This prevents hardware companies from being falsely accused of suboptimal service and/or overcharging consumers.

To reach these goals, we believe metadata should be different at the different layers of the HAL. 
Table entries marked as required are described in more details at the bottom of this section.
We will use the definition *valid* to indicate that the circuit, shot, or gate does not infringe 
the information provided by the metadata (e.g. a five-qubit circuit on a four-qubit system).

Tables should be seen as extensions of the higher levels. For example, Level 2 MUST contain all the fields of Level 3. 
Fields of an higher level HAL MAY be converted from OPTIONAL to REQUIRED but not vice-versa.

Level 3 HAL – application level
-------------------------------

"Able to run large batches of circuits".

At this level, the final stage compiler (executed by the hardware lab) takes care 
of converting an abstract representation made with universal gatesets, into a native one.

Users are entitled to:

- Fair billing. Note that the cost per time on the quantum machine will likely be different from that on the supporting classical infrastructure.

Users won't appreciate:

- If they send a valid circuit and it gets refused/does not complete in time.

Hardware companies won't appreciate:

- Unfair accusations on performance/correctness/costing that can't be easily disproved 
  and might lead to legal actions.

.. list-table:: Level 3 Metadata
  :header-rows: 1

  * - Metadata
    - Description
    - Required
    - Notes
  * - **NUM_QBITS**
    - Number of qubits available
    - Yes
    - It can be smaller than the actual number of qubits in the quantum machine.
  * - **MAX_DEPTH** (as universal gates)
    - Maximum depth of the circuit to execute
    - Yes
    - If **NATIVE_GATES** are not provided, this needs to be a conservative value. The conversion from a universal to a native gate set causes not deterministic (but bound) overhead.
  * - **NATIVE_GATES**
    - List of Native Gates
    - No
    - The **MAX_DEPTH** could be improved significantly by providing the definition of native gates here. Effect: Users will benefit from longer circuits.
  * - **GATE_TIMES**
    - The duration of the gates in **NATIVE_GATES**
    - No
    - With this information, users will be able to optimise their running costs. Note that advanced users are able to infer this information regardless of whether it is provided by the HAL. 


- **NUM_QUBITS**: 
  
  - Type: unsigned int
  
  - Example: 5
  
  - Forbidden Values: [0]
     
- **MAX_DEPTH**:

  - Type: unsigned int
  
  - Example: 200
  
  - Forbidden Values: [0]

Level 2 HAL – shot level
------------------------

"The results of a single circuit and small batches of circuits can be acted upon."

At this level, the final stage compiler (executed by the hardware lab) takes care of converting 
and mapping a native representation of a circuit and executing it. 
Conversion is performed "on the fly".

Users are entitled to:

- Fair billing. Note that the cost per time on the quantum machine will likely be different from that on the supporting classical infrastructure.

- Guaranteed execution. If they send a valid circuit, it shouldn't get refused as it might be part of a long sequence.
  
Users won't appreciate:

- Unknown QoS – mainly if the error rates are unknown

Hardware companies won't appreciate:

- Unfair accusations on performance/costing that can't be easily disproved and might lead to legal actions.


.. list-table:: Level 2 Metadata
  :header-rows: 1

  * - Metadata
    - Description
    - Required
    - Notes
  * - **NUM_QBITS**
    - Number of Qubits available
    - Yes
    - It can be smaller than the actual number of qubits in the quantum machine.
  * - **MAX_DEPTH** (as native gates)
    - Maximum depth of the circuit to execute
    - Yes
    - Total number of gates that can be executed. Without the **GATE_TIMES** information the depth will be conservative to allow for additional margin within the coherence time.
  * - **NATIVE_GATES**
    - List of Native Gates
    - Yes
    - It can be a subset of all the available gates
  * - **CONNECTIVITY**
    - The connectivity matrix of the Qubits
    - Yes
    - It is required to support correct compilation of circuits. 
      The hardware company can return a subgraph of the connectivity as 
      they deem appropriate (e.g. when only a subset of the qubits is exposed 
      they won’t need to expose the full connectivity).
      Connectivity MUST be maintained within two Metadata updates.
  * - **GATE_TIMES**
    - The duration of the gates in **NATIVE_GATES**
    - No
    - With this information, users will be able to optimise their running costs. Note that advanced users are able to infer this information regardless of whether it is provided by the HAL. 
  * - **ERROR_RATE**
    - The average error rate for one- and two-qubit operations in **NATIVE_GATES**
    - No
    - Without this information the users will have to personally evaluate the performance of the hardware before committing to run intensive applications. 
      Users at this level have all the information required to run randomised benchmarking or similar techniques to extract the metrics.


- **NATIVE_GATES**: 
  
  - Type: List of unsigned ints representing HAL gate indexes (specified in HAL library)
  
  - Example: 10 (RX gate), 30 (H Gate), 60 (CNOT)

  - Forbidden Values:
   
    - Any index not included in HAL library


- **CONNECTIVITY**:
  
  - An adjacency matrix (symmetric) of size N x N (where N is the number of qubits) that represents with a 1 an edge that connects two qubits and with a 0 a not-connected edge 
  
  - Example (refer to :numref:`fig_topology_example`): 
  
  .. code-block::

                    [0 1 0 1 0 0 0 0]
                    [1 0 1 0 1 0 0 0]
                    [0 1 0 0 0 1 0 0]
                    [1 0 0 0 1 0 0 0]
    CONNECTIVITY =  [0 1 0 1 0 0 0 0]
                    [0 0 1 0 0 0 0 1]
                    [0 0 0 0 0 0 0 1]
                    [0 0 0 0 0 1 1 0]

  - Forbidden Values: Empty matrices
  
- **ERROR RATE**:
  
  - Error rate is defined as the probability for a quantum operation to introduce an error. 
    A matrix of size N x N (where N is the number of qubits that contains: 
    on the diagonal an average error rate for 1 qubit gate(s); 
    off-diagonal the average error rate of 2 qubits gate(s). 
    To clarify **ERROR_RATE** (1,1) describes the average error rate when 
    executing single qubit gates on qubit0; **ERROR_RATE** (1,2) indicates 
    the average error rate when executing gates two qubit gates on qubit0 
    and qubit1 with (where applicable) 1 being the control qubit and 2 the 
    target one. Multiple matrices can be returned to define the behaviour of 
    different gates. Optionally the values can be provided as intervals.

- Example:

.. code-block::

                    [0.014 0.02  0     0     0     0     0      0    ]
                    [0.02  0.014 1     0     0     0     0      0    ]
                    [0     0.021 0.013 0     0     0     0      0    ]
                    [0     0     0     0.015 1     0     0      0    ]
    ERROR_RATE =    [0     0     0     0     0.012 0     0      0    ]
                    [0     0     0     0     0     0.016 0      0    ]
                    [0     0     0     0     0     0     0.011  0    ]
                    [0     0     0     0     0     0     0.02   0.012]
    
- Forbidden Values: Empty matrices and matrices that violate connectivity. Entries outside the range [0,1].

.. _fig_topology_example:

.. figure:: ./images/image2.png

  Topology used in the example


Level 1 HAL – gate level
------------------------

"Results of qubit measurement can be acted upon within a single circuit."

At this level, the final stage compiler (executed by the hardware lab) takes care of converting and mapping a single gate and executing it. 

.. list-table:: Level 1 Metadata
  :header-rows: 1

  * - Metadata
    - Description
    - Required
    - Notes
  * - **NUM_QBITS**
    - Number of Qubits available
    - Yes
    - It can be lower than the actual number of available qubits.
  * - **MAX_DEPTH** (as native gates)
    - Maximum depth of the circuit to execute
    - Yes
    - Total number of gates that can be executed.
  * - **NATIVE_GATES**
    - List of Native Gates
    - Yes
    - It can be a subset of all the available gates
  * - **CONNECTIVITY**
    - The connectivity matrix of the Qubits
    - Yes
    - It is required to support correct compilation of circuits. 
  * - **GATE_TIMES**
    - The duration of the gates in **NATIVE_GATES**
    - Yes
    - Shuttling time should be considered as an atomic command of which time execution will be required. This to prevent performance inconsistencies 
  * - **ERROR_RATE**
    - The average error rate for one- and two-qubit operations in **NATIVE_GATES**
    - No
    - Without this information the users will have to personally evaluate the performance of the hardware before committing to run intensive applications. 
      Users at this level have all the information required to run randomised benchmarking or similar techniques to extract the metrics.
  
**MAX_DEPTH**:
  
  - Type: unsigned int [unit ps]
  
  - Example: 32000000 ps\ \ [32 us]
  
  - Forbidden Values: [0]

**GATE_TIMES**:
    
    - Type: List of unsigned int [unit ps]
    
    - Example: X: 16000, Y: 16000, CNOT: 28000
    
    - Forbidden Values: [0]

**ERROR_RATE**: [optional]

  - Type: List of decimal numbers (between 0 and 1) defining probability of quantum
    gate to introduce an error.
  
  - Example: X: 0.05 , Y: 0.04
  
  - Forbidden Values: Any usage of NaN (not a number)


Metadata Encoding
------------------------

Here we outline the format in which metadata requests and results are encoded
into 64 bit HAL commands. Depending on the metadata requested the result will
either be returned as a single 64 bit integer or a stream of 64 bit integers
to be collected and decoded into the appropriate data format.

Below is the list of individual metadata items that may be requested and the
structure of their corresponding HAL command request:

.. list-table:: Summary of metadata indexes
  :header-rows: 1

  * - Metadata 
    - Index (binary)
  * - NUM_QUBITS
    - 1 (001)
  * - MAX_DEPTH
    - 2 (010)
  * - NATIVE_GATES/GATE_TIMES 
    - 3 (011)
  * - CONNECTIVITY
    - 4 (100)
  * - ERROR_RATE
    - 5 (101)


**NUM_QUBITS**:


- Request
.. list-table:: HAL command for NUM_QUBITS metadata
  :header-rows: 1

  * - Opcode [12]
    - Argument [16]
    - Padding [36]
  * - 000000001000
    - 0000000000000001
    - 000000000000000000000000000000000000


- Response (single)
.. list-table:: HAL response for NUM_QUBITS metadata
  :header-rows: 1

  * - Metadata Index [3] *(NUM_QUBITS = 1)*
    - Number of qubits [61] *(e.g. 4 qubits)*
  * - 001
    - 000000000000000000000000000000000000000000000000000000000100


**MAX_DEPTH**:


- Request
.. list-table:: HAL command for MAX_DEPTH metadata
  :header-rows: 1

  * - Opcode [12]
    - Argument [16]
    - Padding [36]
  * - 000000001000
    - 0000000000000010
    - 000000000000000000000000000000000000


- Response (single)
.. list-table:: HAL response for MAX_DEPTH metadata
  :header-rows: 1

  * - Metadata Index [3] *(MAX_DEPTH = 2)*
    - Number of qubits [61] *(e.g. 200)*
  * - 010
    - 000000000000000000000000000000000000000000000000000011001000


**NATIVE_GATES/GATE_TIMES**:


- Request
.. list-table:: HAL command for NATIVE_GATES/GATE_TIMES metadata
  :header-rows: 1

  * - Opcode [12]
    - Argument [16] *(3)*
    - Padding [36]
  * - 000000001000
    - 0000000000000011
    - 000000000000000000000000000000000000


- Response (one per native gate)
.. list-table:: HAL response for NATIVE_GATES/GATE_TIMES metadata
  :header-rows: 1

  * - Metadata Index [3] *(3)*
    - Final [1] *(e.g. True)*
    - Gate index [4] *(e.g. 0)*
    - Opcode [12] *(e.g. 10 = RX gate)*
    - Gate Time [44] *(e.g. 16000 ps)*
  * - 011
    - 1
    - 0000
    - 000000001010
    - 0000000000000000000000000000000011111010000000

- Notes:
   
    - **Final**: flag used to specify last stream packet
    - **Gate index**: used to enumerate the native gates, where the gates can
      be described by the opcode+parameter. The gate indexes are used when
      requesting native gate-specific metadata, such as the ERROR_RATE below
    - **Gate Time**: 44-bit unsigned integer for gate time, specified in picoseconds


**CONNECTIVITY**:


- Request
.. list-table:: HAL command for CONNECTIVITY metadata
  :header-rows: 1

  * - Opcode [12]
    - Argument [16] *(4)*
    - Single row [1] *(e.g. False)*
    - Row index [35] *(e.g. 0)*
  * - 000000001000
    - 0000000000000100
    - 0
    - 00000000000000000000000000000000000


- Response (one per N/3 groupings of non-zero off-diagonal matrix elements)
.. list-table:: HAL response for CONNECTIVITY metadata
  :header-rows: 1

  * - Metadata Index [3] *(4)*
    - Final [1] *(e.g. False)*
    - Row idx 1 [10] *(e.g. 0)*
    - Col idx 1 [10] *(e.g. 1)*
    - Row idx 2 [10] *(e.g. 1)*
    - Col idx 2 [10] *(e.g. 2)*
    - Row idx 3 [10] *(e.g. 2)*
    - Col idx 3 [10] *(e.g. 3)*
  * - 100
    - 0
    - 0000000000
    - 0000000001
    - 0000000001
    - 0000000010
    - 0000000010
    - 0000000011

- Notes:
   
    - We make use of the 36-bit padding in the HAL request to specify if we 
      want the whole matrix back or just a single row
    - **Final**: Non-zero off-diagonal row/column pairs are returned in groups 
      of 3 in row-order, where the final respone packet is marked by this flag
    - Connectivity matrix is symmetric, so only off-diagonal upper half of
      matrix is returned


**ERROR_RATE**:


- Request
.. list-table:: HAL command for ERROR_RATE metadata
  :header-rows: 1

  * - Opcode [12]
    - Argument [16] *(5)*
    - Gate index [3] *(e.g. 2)*
    - Single row [1] *(e.g. False)*
    - Row index [32] *(e.g. 0)*
  * - 000000001000
    - 0000000000000101
    - 010
    - 0
    - 00000000000000000000000000000000000


- Response (one per N/4 groupings of non-zero matrix elements)
.. list-table:: HAL response for ERROR_RATE metadata (first 8 bits)
  :header-rows: 1

  * - Metadata Index [3] *(5)*
    - Final [1] *(e.g. False)*
    - Diagonal [1] *(e.g. True)*
    - Gate index [3] *(e.g. 2)*
  * - 101
    - 0
    - 1
    - 010


.. list-table:: HAL response for ERROR_RATE metadata (final 56 bits)
  :header-rows: 1

  * - Mantissa 1 [10] *(e.g. 2)*
    - Exponent 1 [4] *(e.g. 1)*
    - Mantissa 2 [10] *(e.g. 3)*
    - Exponent 2 [4] *(e.g. 1)*
    - Mantissa 3 [10] *(e.g. 4)*
    - Exponent 3 [4] *(e.g. 1)*
    - Mantissa 3 [10] *(e.g. 3)*
    - Exponent 3 [4] *(e.g. 1)*
  * - 0000000010
    - 0001
    - 0000000011
    - 0001
    - 0000000100
    - 0001
    - 0000000011
    - 0001

- Notes:
  
  - We make use of the 36-bit padding in the HAL request to specify which
    native gate we want data for (obtained from the order of NATIVE_GATES 
    metadata responses), and if we want the whole matrix back or just a single row
  - **Final**: Non-zero error rate values are returned in groups 
    of 4 in top-left to bottom-right order for diagonal (1-qubit gate) data,
    and in the same order of row/column indexes returned from CONNECTIVITY metadata
    request for off-diagonal (2-qubit gate) data. The final respone packet
    for a given gate is marked by this flag
  - Error rate data (value between 0 and 1) is stored in a pair of integers
    with a 10-bit mantissa and 4-bit exponent (distance of mantissa from decimal
    point). This allows us to store mantissas up to three 9s, up to 15 places
    after the decimal point. For example, the number 0.01 is expressed by
    0000000001|0001, and the number 0.00245 is expressed by 0011110101|0010
  - Error rate matrix is **not** symmetric, so off-diagonal upper and lower
    halves of matrix returned. Upper half row is returned in the same order of
    row/column indexes returned from CONNECTIVITY metadata request (row-wise).
    Each row return is followed by column return from lower half with same index,
    before moving to the next upper half row.
  - **Must** have knowledge of CONNECTIVITY metadata in order to map the error
    rate values to appropriate qubits