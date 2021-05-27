Appendix 3: Use Case 2 – holoVQE
================================

Below is an implementation for a single circuit run of the XXZ 
model energy calculation circuit in [arXiv:2005.03023v1]. 
The circuit requires intermediate measurements and resets of qubits, 
but, it does not require modifying the circuit based on the measurement outcomes. 
Hence, assuming the hardware supports active qubit reset as a level 2 (3) 
command, this is an example of a level 2 (3) HAL algorithm. 

Note that if active qubit reset is not available, the algorithm can be 
run using level 1 HAL by replacing:

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

    int lattice_sites = 4; 	// number of ‘burn in’ state preparation lattice  sites
    qubit q[2];    	// declare qubit register with 2 qubits (1 bond, 1 physical)
    bits[4] c;    	// declare classical bit register with 4 bits  (4 measurement results stored)
    float theta = 1.234;	// parameterised angle

    // initialize qubit register
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




