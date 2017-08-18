# Example jobs for condor.


All examples in this directory run the C program `echo_to_file.c` which is executed like this:
```
./echo_to_file filename "content to write"
```
This creates a file with name `filename` and writes `content to write` to it.

The examples show different ways of running this program on a cluster of machines using condor.

There are 4 examples in this directory.

* `simple_input_output`: The simplest way to execute a program, transfers the pre-compiled executable to the target machine.
* `simple_io_as_docker_job`: Tranfers the pre-compiled executable and runs it on a docker container. You must specify the docker image to build the container.
* `simple_io_as_vanilla_job`: Runs a script which builds a container from a Dockerfile and executes it, the container compiles and runs the program.
* `multiple_io_as_vanilla_job`: Same as the last one but executes multiple copies of the job on, potentially on different machines. It then collects all the results and transfers them back to the submitter machine.
