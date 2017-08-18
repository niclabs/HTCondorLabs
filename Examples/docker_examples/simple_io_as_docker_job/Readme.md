# Simple input output example
This example runs a simple C program that receives a filename and a word as commandline arguments and writes the word to a file. It tranfers the pre-compiled executable and runs it on a docker container.

## Instructions

1. Compile the C program
 ```
 gcc echo_to_file.c -o echo_to_file
 ```
2. Create directory for logs
```
mkdir logs
```
3. Submit the job to execute on condor
```
 condor_submit docker.job
```

Once executed the output file `output.txt` should be transferred back to the submitter machine.
