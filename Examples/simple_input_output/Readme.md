# Simple input output example
This example runs a simple C program that receives a filename and a word as commandline arguments and writes the word to a file.

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
 condor_submit simple.job
```

Once executed the output file `output.txt` should be transferred back to the submitter machine. You can check that it contains the word `hello`.
By changing the line
 ```
 arguments = output.txt hello
 ```
you can change the output file's name or it's content. If you change the output file's name you must also change the line
```
transfer_output_files   = output.txt
```
to assure the output file is transferred back to the submitter machine.
