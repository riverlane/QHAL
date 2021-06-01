Appendix 1
==========

Notes and Questions 
-------------------

[Metadata*]	How will this be implemented in other systems. Is this info stored in a config file? Assuming an application developer is writing an algorithm that then needs to be built to run on hardware, it would make sense that this data is store on the user's machine and used to compile and build?

[Examples*]	Pseudo-language code example of a HAL feature implementation 

[UC]	Use-case scenarios

[1*]	This is still open for debate and will depend on HW provider as well as qubit tech. Likely, something to include in metadata rather than specify.

[2*]	If a vendor conforms to the structure of the HAL for their internal features then they could benefit from examples and some standardisation for their group properties APIs even if not for their implementation.

[3*]	The one attack that could be most worrisome already is on the device firmware itself or on the management system—whether it be by alteration or replacement. Hence signatures and attestation should probably be assumed

[q1]	Metadata is part of the HAL, and in some cases, it seems that data may reflect details of the lowest levels of the QPU stack including some details of the qubit implementation to help guide cross-implementation translation. The CPU could be involved in translation too, especially if it changes across implementations as should be anticipated (example: a constant representing the CPU architecture). If this is correct, then The HAL may cover as much as the whole stack, not just the middle. [Does it need clarifications?]

[q2]	Groups and levels disjoint and distinct? Are all groups (or levels) expected to be implemented by all vendors even if they are not all exposed to all customers? Or may vendors choose to build bespoke versions of some in ways that do not coordinate with other components? This could prove relevant if the OS implementation and HAL components are "certified" or "conformant" for use and might even be commercially traded among parties to Deltaflow OS, since the HAL itself appears to have the option to be closed source software even if Deltaflow itself remains OSS. If they are not required to be implemented should some be explicitly denoted as optional, and if they are, then should that be stated here at the start? [Added Multi-Level HAL extra specifications]

[q3]	Again, are we going to encourage vendors to follow the level structure for their internal use, even if they don't expose them to any customers? Is Level 3 mandatory? Is level 2 encouraged? Is Level 1 truly optional? Is there an implication that some or all levels may be licensed? Is it anticipated that some vendors may choose to open source their implementations? It is likely that there will be a need to validate the authenticity of any level for supply chain and security-related reasons. [Tentative response in Multi-Level HAL additional considerations] 

[q4]	Consequently, do we want to explicitly state that members of this category may not translate across implementations, resulting in defaulting back to core commands and speeds? [Tentative response in Multi-Level HAL additional considerations] 


[q5]	Is metadata confined to static information that is especially useful at initialisation time? Does it include dynamic properties? Can it be extended by the vendor to include information that is specific to a specific machine, such as the calibration and quality of specific qubits hints that can be used by algorithm developers to select how to distribute computation across the qubits made available to them or even for the OS to allocate qubits based on quality or length of computation or even cost to the application customer for their use. These factors could make it important to authenticate such information. Therefore, should the metadata also be decomposed into "levels" of revelation? [Should be addressed by the Section Metadata Specification]

[q6]	Should we have controlled rotation gates? [Added to the Notes on commands Layer 2 and 1]

[q7]	Multi-user and session management – should this be part of the specification? [Addressed by HAL Commands Minimum Requirements]

[q8]	Should qubit indices be handled as indices rather than bit fields? [Addressed in Command Format: Option I]

[q9]	Should we include gates with more than two qubits? ? [Added to the Notes on commands Layer 2 and 1]

[q10]	Add a command to the standard regarding selection of the backend - emulator or hardware. Deltaflow OS can utilise this command to select a backend for HAL Software to run the algorithms on? [Addressed by HAL Commands Minimum Requirements]
