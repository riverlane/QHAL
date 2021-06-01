Security
========

Threat model
------------

Even at the end of the NISQ era, chances of having low-cost Quantum machines are negligible. This implies that most of the quantum resources will be shared among a large pool of users and potentially exposed via Cloud Interfaces. From a security perspective, various aspects make Quantum machines different from classical resources:

- Cost of the hardware, uptime concerns. Damage to some of the building blocks of a quantum machine might lead to extremely long lead times as well as high cost

- Intellectual Property protection. Malicious attackers will try to obtain information on the quantum machine internals to make profits or increase their visibility. 

The two problems have direct implications for the Quantum hardware providers but as explained in the Section require countermeasures to be implemented at the classical interface level. 

We would like to have the HAL to be future proof in terms of security with the caveat that additional work will be needed throughout the stack to guarantee the full security of the solution[3*].
The threats that we currently consider out of the scope for this document are:

- Side channel attacks. Malicious users might try to infer what other users are running if multi-user access to the quantum resource is allowed. The number of practical experiments on the subject is not sufficient to identify the need for them and the mitigation strategies.

- Unsigned execution of code. Compilers might be tampered, unverified and malicious code crafted. Currently no attack has been identified that could damage the quantum machine and/or cause repercussion on the next user. 

Implementation aspects
----------------------

We would like to start the discussion on Security of the Quantum machine and of the Quantum Operations. As for most other form of modern technologies, security in Quantum Systems requires the introduction of various mechanisms at potentially all the operational levels. In this Section will limit the scope to the measures that we think are implementable by the HAL or that have a direct effect on it.
With the broad-brush term of security, we will refer in the following to:

1.	Application security. We should define rules and guidelines to minimise the risk of the user:
    
    a.	Having their application executed on a target that is not the expected one. A specific example: man-in-the-middle attacks

    b.	Incurring extra costs caused by over-execution. A malicious attacker able to introduce extra computation causing unforeseen costs to the user.

2.	Quantum machine security. We should define rules and guidelines to minimise the risk of a Quantum Machine:
    
    a.	being damaged or its QoS reduced by the user via means of low-level attacks. Example: Attacks that leverage patterns to cause extra noise in the circuit execution (in case of multi-users), attacks that cause excessive power dissipation on the fridge logic etc.

    b.	being brought in a condition of not being able to take extra requests from other users. We should expect malicious users to try denial-of-service attacks by injecting small requests (in terms of their data payload) that cause an intense computation or conversely increase the delay in the communication by saturating input channels.

3.	Supply Chain Security. The Quantum Machine drivers can be compromised or modified by malicious attackers. This can cause identity theft and/or exposure of confidential information.   
We suggest the following level of severity for these class of security considerations:

- **Extremely severe**: 2.a

- **Severe**: 1.a, 1.b, 3.a

- **Moderate** 2.b,

And the level of potential complexity required to implement mitigation strategies around them:

- **High complexity**: 2.a

- **Medium complexity**: 2.b

- **Low complexity**: 1.a, 1.b

We will propose in the next sub-sections few potential measures to address the 
set of above-listed threats. All the solutions that address at least one vulnerability 
of severity severe and extremely severe will be indicated as "Rules" while lower severity 
vulnerability as "Guidelines".

Rule 1: parties' authentication
-------------------------------

We suggest that Post-Quantum cryptography or Quantum-Robust algorithms should be investigated in the near future as in the post NISQ era they will be relevant. As they don't significantly impact the HAL, we will try here to define a generic approach that should allow us to move to Quantum Robust implementations when needed. 
We start by establishing a trusted channel between the user and hardware provider. By doing this we should be able to minimise the likelihood of 1.a, 1.b, 1.c ,3.a. For the latter we assume that components of the hardware control stack have a signature that can be verified by the users. 
Further enhancements to traditional protocols can be embedded into this HAL specification by introducing the following commands:

- Request public key
  
- Request authentication scheme
  
- Send authentication challenge
  
- Retrieve authentication response
  
- Send driver challenge
  
- Retrieve driver response


Rule 2: Coarse-granularity machine statistics
---------------------------------------------

All the commands that return data that can directly or indirectly be used to infer:

- Number of users currently sharing the Quantum machine
  
- Status of the hardware components

Should return values that have sufficiently coarse granularity to prevent 
any type of reverse-engineering of power models, components behaviour and 
number of users. This to reduce the likelihood of success of attacks of type 2.a
A set of selected users (e.g. system maintainer) could be granted a finer 
grain visibility to these data. Additionally, research groups could be granted 
access to historical data for which users have been pre-approved public disclosure.

Guideline 1: Prevention of Denial of Service
--------------------------------------------

To prevent a malicious attacker from causing a denial of service to the 
Quantum machine we recommend implementing a variable response time for all 
the query operations. 
This type of requests tends to have an asymmetric computational cost 
and could be used to generate a system load on the Quantum machine interface 
with limited amount of data generated. As an example, consider Rule 1 and the 
challenge operation. If multiple requests of the same class of commands are to 
be issued to the quantum machine to perform a Denial-of-Service attack, the 
machine should respond with increasingly higher latency to this type of requests 
to invalidate the attack.
