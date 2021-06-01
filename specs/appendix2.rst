Appendix 2: Use Case 1 – Shor's Algorithm
=========================================

Here we provide two ways of implementing quantum circuits used in Shor's algorithm
The first implementation uses a FOR loop to repeat sets of circuit operations whereas the second implementation avoids using a loop by repeating the code for the set of circuit operations an appropriate number of times. Another difference between the two implementation is that in the first implementation, consecutive controlled phase gates are combined using classical logic before the command is sent to the quantum device.


Implementation 1 pseudocode
---------------------------

.. code-block::

    /*
    * Shor's algorithm circuit
    * 1+4 qubits example with k=3, N = 15, a = 11
    */


    int n = 5;   		// 1 + number of bits used to represent N
    int k = 3;   		// number of QFT bits
    qubit q[n];    	// declare qubit register with n qubits
    bits[k] c;    	// declare classical bit register with QFT bits ordered from most significant(c[0]) to least significant (c[k-1])
    
    
    //initialise qubit register
    reset q;
    
    // prepare qubits register |00001>
    x q[n-1];
    
    // define function that runs the appropriate pulse sequence
    def apply_controlled_unitary(int[k]: op_index) {
            // Apply appropriate controlled unitary
            //  = controlled-a^(2^(k-(1+op_index)))%N  
    
            if (op_index == 0) {
                    // Apply controlled (11^4)%15 = controlled 1%15
                    
    // Nothing to do
            }
    
            if (op_index == 1) {
                    // Apply controlled (11^2)%15 = controlled 1%15
                    
    // Nothing to do
            }
    
            if (op_index == 2) {
                    // Apply controlled (11^1)%15 = controlled 11%15
    
                    // swap q[2] and q[4] conditioned on q[0]
    cswap q[0] q[2] q[4];   
                cswap q[0] q[1] q[3];
                    
    // apply X on q[1] conditioned on q[0]
    cx q[0] q[1];           
                    cx q[0] q[2];
                    cx q[0] q[3];
                    cx q[0] q[4];
            }
    }
    
    // Shor's algorithm loop
    for i in [0: k - 1] {
            // Reset QFT qubit to |0> state
            reset q[0];     
            
    // Apply Hadamard gate to create |+> state
    h q[0];         
    
            apply_controlled_unitary(i)
    
    // phase shift to apply depends on previous measurements; sum up the phase rotation angles and then apply a phase gate with the summed angle
    float phase_shift = 0;
    
    if (c[0] == 1) {
                    phase_shift += pi/2;
    }
    if (c[1] == 1) {
                phase_shift += pi/4;
    }
    if (c[2] == 1) {
                phase_shift += pi/8;
    }
    rz (phase_shift) q[0];        
    
    // Apply Hadamard
    h q[0];         
    
            // Newest measurement outcome is associated with a pi/2 phase shift
            // in the next iteration, so shift all bits of c to the right
            c >>= 1;
    
    // Measure QFT qubit and save result to 0th index of classical bit register
            measure q[0] -> c[0];   	
    }

    
Implementation 2 pseudocode
---------------------------

.. code-block::

    /*
    * Shor's algorithm circuit
    * 1+4 qubits example with k=3, N = 15, a = 11
    */


    int n = 5;   		// 1 + number of bits used to represent N
    int k = 3;   		// number of QFT bits
    qubit q[n];    	// declare qubit register with n qubits
    bits[k] c;    	// declare classical bit register with QFT bits ordered from most significant(c[0]) to least significant (c[k-1])


    //initialise qubit register
    reset q;

    // prepare qubits register |00001>
    x q[n-1];

    // Shor's algorithm loop
    //------------------------------------------------
    //------------------- k = 0 ----------------------
    //------------------------------------------------

    // reset QFT qubit to |+> state
    reset q[0];
    h q[0];

    // apply controlled (11^4)%15 = controlled 1%15
    // nothing to do

    // phase shift to apply depends on previous measurements
    if (c[0] == 1) {
            rz (pi/2) q[0];
    }
    if (c[1] == 1) {
            rz (pi/4) q[0];
    }
    if (c[2] == 1) {
            rz (pi/8) q[0];
    }

    h q[0];
    // newest measurement outcome is associated with a pi/2 phase shift
    // in the next iteration, so shift all bits of c to the right
    c >>= 1;
    measure q[0] -> c[0];
    }

    //------------------------------------------------
    //------------------- k = 1 ----------------------
    //------------------------------------------------

    // reset QFT qubit to |+> state
    reset q[0];
    h q[0];

    // apply controlled (11^2)%15 = controlled 1%15
    // nothing to do

    if (c[0] == 1) {
            rz (pi/2) q[0];
    }
    if (c[1] == 1) {
            rz (pi/4) q[0];
    }
    if (c[2] == 1) {
            rz (pi/8) q[0];
    }

    h q[0];
    // newest measurement outcome is associated with a pi/2 phase shift
    // in the next iteration, so shift all bits of c to the right
    c >>= 1;
    measure q[0] -> c[0];
    }

    //------------------------------------------------
    //------------------- k = 2 ----------------------
    //------------------------------------------------

    // reset QFT qubit to |+> state
    reset q[0];
    h q[0];

    // apply controlled (11^1)%15 = controlled 11%15
    cswap q[0] q[2] q[4];
    cswap q[0] q[1] q[3];
    cx q[0] q[1];
    cx q[0] q[2];
    cx q[0] q[3];
    cx q[0] q[4];

    if (c[0] == 1) {
            rz (pi/2) q[0];
    }
    if (c[1] == 1) {
            rz (pi/4) q[0];
    }
    if (c[2] == 1) {
            rz (pi/8) q[0];
    }

    h q[0];
    // newest measurement outcome is associated with a pi/2 phase shift
    // in the next iteration, so shift all bits of c to the right
    c >>= 1;
    measure q[0] -> c[0];
    }

    //------------------------------------------------
    //------------------- DONE -----------------------
    //------------------------------------------------
