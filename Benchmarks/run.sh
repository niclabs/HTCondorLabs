#!/bin/bash
# file name: run.sh

echo "Building image"
/usr/bin/docker build -t image .
echo "Running image"
/usr/bin/docker run --name="benchmark" image
echo "Extracting files"
/usr/bin/docker cp benchmark:/benchmark/results .
echo "Cleaning up"
/usr/bin/docker rm benchmark
