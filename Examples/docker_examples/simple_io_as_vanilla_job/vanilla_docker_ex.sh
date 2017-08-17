#!/bin/bash
# file name: vanilla_docker_ex.sh

echo "Building image"
/usr/bin/docker build -t image .
echo "Running image"
/usr/bin/docker run --name="condor_job" image
echo "Extracting files"
/usr/bin/docker cp condor_job:/myvol .
echo "Cleaning up"
/usr/bin/docker rm condor_job

