# Simple input output example
This example runs a simple C program that receives a filename and a word as commandline arguments and writes the word to a file. It uses a script to build a container which will contain a copy of the echo_to_file program and will compile and execute it.

## Instructions

1. Create the directory for logs
```
 mkdir logs
```
2. Submit the job to execute on condor using:
```
 condor_submit vanilla_docker.job
```

This will execute the `vanilla_docker_ex.sh` script, which will build and run a docker container. This container will compile and execute the echo_to_file program.
