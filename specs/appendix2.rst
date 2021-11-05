Appendix 2: Use Cases
=========================================

Use Case 1 – Shor's Algorithm
-----------------------------

Here we provide two ways of implementing quantum circuits used in Shor's algorithm
The first implementation uses a FOR loop to repeat sets of circuit operations whereas the second implementation avoids using a loop by repeating the code for the set of circuit operations an appropriate number of times. Another difference between the two implementation is that in the first implementation, consecutive controlled phase gates are combined using classical logic before the command is sent to the quantum device.


Implementation 1 pseudocode
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

    /*
    * Shor's algorithm circuit
    * 1+4 qubits example with k=3, N = 15, a = 11
    */

    /* 1 + number of bits used to represent N */
    int n = 5; 

    /* number of QFT bits */  		
    int k = 3;

    /* declare qubit register with n qubits */
    qubit q[n];

    /* declare classical bit register with QFT bits ordered from most 
    * significant(c[0]) to least significant (c[k-1]) */
    bits[k] c;
    
    /* initialise qubit register */
    reset q;
    
    /* prepare qubits register |00001> */
    x q[n-1];
    
    /* define function that runs the appropriate pulse sequence */
    def apply_controlled_unitary(int[k]: op_index) {
            // Apply appropriate controlled unitary
            //  = controlled-a^(2^(k-(1+op_index)))%N  
    
            if (op_index == 0) {
                    // Apply controlled (11^4)%15 = controlled 1%15
                    // Identity operation => Nothing to do
            }
    
            if (op_index == 1) {
                    // Apply controlled (11^2)%15 = controlled 1%15
                    // Identity operation => Nothing to do
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
    
            /* phase shift to apply depends on previous measurements; 
            * sum up the phase rotation angles and then apply a 
            * phase gate with the summed angle */
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
            
            /* Newest measurement outcome is associated with a pi/2 phase shift
            * in the next iteration, so shift all bits of c to the right */
            c >>= 1;
            
            /* Measure QFT qubit and save result to 0th index of 
            * classical bit register */
            measure q[0] -> c[0];   	
    }

    
Implementation 2 pseudocode
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    /*
    * Shor's algorithm circuit
    * 1+4 qubits example with k=3, N = 15, a = 11
    */


    /* 1 + number of bits used to represent N */
    int n = 5; 

    /* number of QFT bits */  		
    int k = 3;

    /* declare qubit register with n qubits */
    qubit q[n];

    /* declare classical bit register with QFT bits ordered from most 
    * significant(c[0]) to least significant (c[k-1]) */
    bits[k] c;
    
    /* initialise qubit register */
    reset q;
    
    /* prepare qubits register |00001> */
    x q[n-1];

    /* Shor's algorithm loop
    * ------------------------------------------------
    * ------------------- k = 0 ----------------------
    * ------------------------------------------------ */

    // reset QFT qubit to |+> state
    reset q[0];
    h q[0];

    // apply controlled (11^4)%15 = controlled 1%15
    // Identity operation => Nothing to do

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
    /* newest measurement outcome is associated with a pi/2 phase shift
    * in the next iteration, so shift all bits of c to the right */
    c >>= 1;
    measure q[0] -> c[0];

    /* ------------------------------------------------
    *  ------------------- k = 1 ----------------------
    *  ------------------------------------------------ */

    // reset QFT qubit to |+> state
    reset q[0];
    h q[0];

    // apply controlled (11^2)%15 = controlled 1%15
    // Identity operation => Nothing to do


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
    /* newest measurement outcome is associated with a pi/2 phase shift
    * in the next iteration, so shift all bits of c to the right */
    c >>= 1;
    measure q[0] -> c[0];

    /* ------------------------------------------------
    *  ------------------- k = 2 ----------------------
    *  ------------------------------------------------ */

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
    /* newest measurement outcome is associated with a pi/2 phase shift
    * in the next iteration, so shift all bits of c to the right */
    c >>= 1;
    measure q[0] -> c[0];

    /* ------------------------------------------------
    *  ------------------- DONE ----------------------
    *  ------------------------------------------------ */

Use Case 2 – holoVQE
--------------------------------

Below is an implementation for a single circuit run of the XXZ 
model energy calculation circuit in [REF_5]. 
The circuit requires intermediate measurements and resets of qubits, 
but, it does not require modifying the circuit based on the measurement outcomes. 
Hence, assuming the hardware supports active qubit reset as a Level 2 (3) 
command, this is an example of a Level 2 (3) HAL algorithm. 

Note that if active qubit reset is not available, the algorithm can be 
run using Level 1 HAL by replacing:

.. code-block::

    reset q[1]; 

with the following:

.. code-block::

    measure  q[1] -> c[0];
    if (c[0] == 1) {
        x q[1];
    }


.. code-block::

    /*
    * holoVQE circuit for XXZ spin chain energy calculation
    * 1 physical qubit, 1 bond qubit; 4 ‘burn in’ lattice sites
    */

    /* number of ‘burn in’ state preparation lattice  sites */
    int lattice_sites = 4;

    /* declare qubit register with 2 qubits (1 bond, 1 physical) */
    qubit q[2];

    /* declare classical bit register with 4 bits  (4 measurement results stored) */
    bits[4] c;

    /* parametrised angle */
    float theta = 1.234;

    /* initialise qubit register */
    reset q;

    // State preparation
    for i in [0: lattice_sites - 1] {
        // Apply G_theta
        rx (pi/2) q[0];
        ry (pi/2) q[1];
        cz q[0] q[1];
        rx (-theta) q[0];
        ry (theta) q[1];
        cz q[0] q[1];
        rx (-pi/2) q[0];
        ry (-pi/2) q[1];

        // Reset physical qubit
        reset q[1];

        // Apply G_theta_tilda
        rx (pi/2) q[0];
        ry (pi/2) q[1];
        cz q[0] q[1];
        rx (-theta) q[0];
        ry (theta) q[1];
        cz q[0] q[1];
        rx (-pi/2) q[0];
        ry (-pi/2) q[1];
        x q[1];

        // Reset physical qubit
        reset q[1];
    }
    //Expectation value measurement

    //Apply G_theta, measure in X basis, then reset physical qubit
    rx (pi/2) q[0];
    ry (pi/2) q[1];
    cz q[0] q[1];
    rx (-theta) q[0];
    ry (theta) q[1];
    cz q[0] q[1];
    rx (-pi/2) q[0];
    ry (-pi/2) q[1];

    h q[1];
    measure q[1] -> c[0];

    reset q[1];

    //Apply G_theta_tilda, measure in X basis, then reset physical qubit
    rx (pi/2) q[0];
    ry (pi/2) q[1];
    cz q[0] q[1];
    rx (-theta) q[0];
    ry (theta) q[1];
    cz q[0] q[1];
    rx (-pi/2) q[0];
    ry (-pi/2) q[1];
    x q[1];

    h q[1];
    measure q[1] -> c[1];

    reset q[1];

    //Apply G_theta, measure in Z basis, then reset physical qubit
    rx (pi/2) q[0];
    ry (pi/2) q[1];
    cz q[0] q[1];
    rx (-theta) q[0];
    ry (theta) q[1];
    cz q[0] q[1];
    rx (-pi/2) q[0];
    ry (-pi/2) q[1];

    measure q[1] -> c[2];

    reset q[1];

    //Apply G_theta_tilda, measure in Z basis, then reset physical qubit
    rx (pi/2) q[0];
    ry (pi/2) q[1];
    cz q[0] q[1];
    rx (-theta) q[0];
    ry (theta) q[1];
    cz q[0] q[1];
    rx (-pi/2) q[0];
    ry (-pi/2) q[1];
    x q[1];

    measure q[1] -> c[3];

    reset q[1];

    //------------------------------------------------
    //------------------- DONE -----------------------
    //------------------------------------------------




