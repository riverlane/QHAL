# Code implementation and testing environment

A representative implementation of some of the main concepts defined in the [specifications](specifications.pdf) is provided in [lib](lib). 

The code is tested for correctness via a set of direct tests. 

The testing framework leverages Docker and makefiles to install all the dependencies required. 
It has been tested on Linux and MacOs platforms. 
For more information on Docker and how to install it [docs](https://docs.docker.com).

To execute them from a terminal:

```shell
  make tests
```


