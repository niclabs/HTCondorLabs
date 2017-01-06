# Example jobs for condor.

T1.c is a C program that needs 2 arguments: 'name' and 'word'. 'name' is used to create a file in which to write 'word'.
Its a simple program but help understand Condor's behavior, like when Condor takes back a generated file with it.

There are 2 examples in this directory.

1.- Docker universe job

2.- Vanilla universe running a Docker job

1* To run the Docker universe job submit 'docker.job' to Condor. This template will tell Condor that the job will be using
a certain docker image to run. Condor will take care of all this and run the job inside the container.
To run this job you first have to compile T1.c like follows: gcc -o T1 T1.c

2* To run the Vanilla universe with a Dockerfile submit 'vanilla_docker.job'. This template will tell condor to use the
'vanilla_docker_exc.sh' executable that will build and run the Dockerfile, then copy the folder out of the container
and tell Condor to take that folder back when the job is done.
