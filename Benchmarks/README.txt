Usage:

For docker benchmarking:
    *Just run the run.sh script. It will build and run the dockerfile,
    copy the generated files in the current directory and remove the container.
    
For normal benchmarking:
    *You will need to install the libraries in requirements.txt.
        **It is recommended to install virtualenv and install them there.
    *Run the benchmark_run.sh script. It will run the tests and generate
    the files with the output.
    
    
The benchmark will only write the time elapsed since the start of the program
to the end of it. To find this number go to the end of the files generated,
it will be in the following format: DD:HH:MM:SS.. Just divide the time elapsed
by the number of tests and you get the average execution time.
