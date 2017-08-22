# Simple input output example
This example runs multiple copies if a simple C program that receives a filename and a word as commandline arguments and writes the word to a file. It tranfers the pre-compiled executable and runs it on a docker container.

## Instructions

1. Create a directory for logs
 ```
 mkdir logs
 ```
2. Submit the job to execute on condor using:
```
 condor_submit multi_vanilla_docker.job
```

This will create 5 jobs, each corresponding to an execution of the C program.
Each job will execute the vanilla_docker_ex.sh with a different numeric argument from 0 to 4. The script will translate this number into the string arguments for the C program. Once each job finishes execution it will create separate output and log files.
