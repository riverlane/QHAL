# Code implementation and testing environment

A representative implementation of some of the main concepts defined in the [specifications](specifications.pdf) is provided in [lib](lib). 

The code is tested for correctness via a set of direct tests. 

To execute them:

```shell
  make tests
```

The testing framework leverages Docker and makefiles to install all the dependencies required. 
It has been tested on Linux and MacOs platforms. 
For more information on Docker: [docs](https://docs.docker.com).

