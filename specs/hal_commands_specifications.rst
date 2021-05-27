HAL Commands Format specification
=================================

Introduction
------------

The HAL commands should have a format that provides the best generality and expressivity whilst keeping the decoding logic (and consequently its latency) to the minimum. Before describing the format, the considerations that have motivated the choice of this format are outlined. We will touch on the two main sets of implications that relate to the command format.

- Commands must be transmitted to the QPU
  
- Commands must be parsed and decoded. If errors occur in any of the two processes they should be returned. 

Considerations on transmission
------------------------------

- The transmission of the HAL commands occurs via physical wires (electrical or optical) and/or via internal on-chip traces (e.g. FPGA routing resources)

- We will assume error-free (or classically error-corrected) transmission of the commands in this version of this proposal.

- We will assume that different quantum hardware will have different requirements in terms of connectivity, required bandwidth (of commands), and link-latencies. For this reason, we have tentatively listed in Table 1 some metrics related to standard (public) interfaces.

- It is important to point out that:

    1.	Most transmission protocols listed in the physical layer could be adapted to handle arbitrary packet sizes. It is worth pointing out that this will require a custom implementation of the link-layer logic for both transmitter and receiver. 
    
    2.	Ad-hoc protocols might use generic parallel-busses of any width (i.e., not standard interfaces). We think that addressing these specific scenarios might lead to a loss of generality for this set of specifications. 


.. list-table:: Transport Protocols - illustration

  * - Protocol
    - Minimum Packet Size/Increments 
    - Technology Supported
    - Notes
  * - Ethernet (raw)
    - 46 bytes/1 byte (up to 1500 bytes)
    - CPU, FPGA, ASIC
    - Large transmission overhead 
  * - PCIe3.0/4.0
    - 128/256/512 bytes (Root complex dependant)
    - CPU, FPGA, ASIC
    - Short reach  
  * - USB3.x
    - 1 byte/1 byte (up to 1024 bytes)
    - CPU, FPGA[\*\], ASIC
    - Transmission overhead (protocol defined transmission timeslots) 
  * - Intra-chip communication (AMBA-AXI)
    - 4 bytes/4 bytes (up to 128 bytes[\**\])
    - FPGA, ASIC, CPU[\***\]
    - Ultra-short reach
  * - Serial Peripheral Interface (SPI) 
    - 1 byte/1 byte (up to 1024 bytes[\****\])
    - FPGA, ASIC, CPU
    - Low bandwidth

[\*\]	USB3.2 2x2 might require special cards to implement the initial speed negotiation (10 Gbps mode) that might not be commercially available.
[\**\]	The AMBA protocol does not set an upper limit on the size of the bus but the physical routing of the logic normally limits this value to be 1024 bits threshold
[\***\]	Hard/Soft-CPU only. Only CPU that are integrated into the same die as the ASIC/FPGA (either permanently or in a reconfigurable fashion).
[\****\]	Generally, controller limited. Some controllers support up to 65535 bytes.

Considerations on Decoding 
--------------------------

- To guarantee applications portability, we recommend for the HAL specification to define a consistent representation for all the commands in terms of the number of bits and their significance. 

- Bit shifts and bit masking can be implemented with limited effort and low latency on CPU, FPGA and ASICs

- The identifier of the command (OPCODE) can be of:
    
    1.	Fixed-length (i.e. all OPCODES are implemented using the same number of bits)
    
    2.	Variable-length (i.e. OPCODES can use a different number of bits)

(1) provides the fastest decoding (e.g. look-up tables based) while (2) can increase the content of information transmitted via better usage of the available bits

- Qubit indexing can be implemented as:

    1.	a combination of one-hot encoding (e.g. 1001 indicates that index 0 and 3 are active)

    2.	or in a binary format (e.g. 1001 indicates that the index 9 is active). 

/(1)/ enables the addressing of multiple qubits via a single command while /(2)/ provides a much larger qubit addressing space (N vs 2**N) 

- Commands that do not fit in a single word can be split and transmitted as a sequence of parts (multi-word commands). We envision three possible scenarios here:

    1.	The list of commands that require more than one word (multi-word commands) is fixed and predefined. Their OPCODE is sufficient to inform the decoding logic that they are composed of multiple words. 
    
    2.	The list of multi-word commands is not known a priori. A field/flag can be set to indicate that the command is composed of extra words. This field/flag will require at least one extra bit to be always dedicated to this specific purpose.
    
    3.	The list of multi-word commands is not known a priori. A special command needs to be issued to indicate that what follows is a sequence of multi-word commands. One possible implementation uses the first command argument to indicate the number of words composing the real multi-word command to execute.

(1) provides the simplest decoding logic (fixed-length commands with deterministic latency), (2) and (3) have slightly more complex logic with at least one extra conditional branch. If statistically, the likelihood of multi-word commands is low, (3) provides a lower bit requirement overhead than (2).

- Multi-Qubit commands (e.g. CNOT) require (a) the definition of two indexes as well as (b) the execution of two parallel sequences of control. While (a) is in line with previous considerations, (b) requires additional considerations. The decoder logic should effectively extract both the indexes (ideally in a single instruction) and inform the associated branches of the control logic (if independent). We identified the following options:

    1.	Single-word command with halved addressing space. We preserve the format of the command but consider the lower half of the index field pertaining to qubit 0 and the upper part to qubit 1

    2.	Longer command. We append a second indexing field to the end of the command to address the second index.

    3.	Double-word command. We extend the command with the second index and padding.

    4.	Two-words command. We split the command into two portions, and we send them as two separate tokens. e.g., we split a CNOT into in a "Control" and "Controlled" set of commands (CNOT_CTRL, CNOT_DATA).

(1)-(4) require almost no changes to the architecture for 1 qubit commands in storage and decoding. (4) though does introduces a barrier on execution. Because now the two commands are independent, the transport layer can delay the transmission of the second one, requiring buffering of the command. (2) - (3) require an extra buffer/register to store the second portion of the command and potentially forces us to decouple the command width from the transport layer width, but they do enforce the command's atomicity. 


Command Format: Option I
------------------------

We would like to conclude this Section by proposing at least one possible format for the HAL commands.
Table 9 contains two representations, a "single-word" command (64 bits) and a "dual-word" command (128 bits). The goals of this format are (a) low complexity decoding logic (with buffering), (b) no significant performance penalty. 

.. list-table:: Format proposal

    * - Command type
      - OPCODE 
      - ARGUMENT
      - QUBIT INDEX
    * - Single/Dual Word
      - Identifies the type of instruction to execute
      - Associate an argument to the instruction (e.g. the angle of a rotation)
      - Indicates the index of the QUBIT to manipulate
    * - SINGLE WORD 
      - [63-48]
      - [47-32]
      - [31-0]
    * - DUAL WORD
      - [127-112] + 16 bits padding 
      - [95-80] – qubit1, [79-63] – qubit0
      - [63-32] – qubit 1, [31-0] -  qubit0

The following considerations have been made:

- We recommend defining byte-aligned fields to avoid decoding penalty in the technologies (e.g. CPUs) with coarse access granularity.

- By fixing the OPCODE length, the decoder logic can use lookup tables. We consider 65536 codes (16 bits) to be more than sufficient. Note: It might be possible to reduce them to 256 (8 bits) by intelligent usage of special commands that allow an exception to the format (MODIFIERS, two examples will follow).
  
- The addressable number of qubits (2**32) should accommodate the needs of NISQ and the early post-NISQ era. Note: We could consider pre-emptively doubling the INDEX field's size at the cost of an initial transmission overhead.

- The full instruction space (2**16) and the argument field (2**16) should similarly be future proof.

- No field has been allocated to support multi-word commands.

- The DOUBLE-WORD command can be clearly identified by the OPCODE (we suggest using the MSB bit to indicate whether it is a SINGLE or DUAL WORD command). The implications in terms of logic are that we (a) need to buffer the command if the transport layer as width < 128 bits, (b) have a slightly different decoding logic for SINGLE WORD and DUAL WORD command. We consider (b) of minor impact being everything word aligned and in both CPU and FPGA/ASIC logic that can still be implemented via simple shifting. 

- We can introduce the following optional SINGLE WORD commands to define large scale atomicity and barriers:
    
  - MULTI_WORD. 
      Argument: the number (M) of words that compose the command. The command should be executed after the Mth word has been received. This requires special treatment on the buffer side but can be used to support commands with extra-long arguments. 

  - MULTI_CMD.
      Argument: the number (N) of commands that compose an "atomic" sequence. The N commands that will follow should be executed at the same time.
      
  