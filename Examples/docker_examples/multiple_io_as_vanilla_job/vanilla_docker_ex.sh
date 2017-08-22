#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function clean_up () {
  docker rm -f $1
  exit
}

args_list=(
"The quick"
"brown fox"
"jumps"
"over the"
"lazy dog"
)

number=$1
name="simple-io-example-$number"
## Trap the signal used by condor to terminate a job.
## When the signal is received, stop the running container and exit
trap "clean_up $name" SIGINT SIGTERM

## Create the output directory, which will be mounted
## as a volume to the docker container.
## We create it beforehand to assure it it owned by the
## same user that runs the container, otherwise it will be
## created but it will be owned by root.
mkdir -p $DIR/output

docker rm -f $name
docker build --tag simple-io-example .
docker run --name $name -v $DIR/output:/output \
 -u $(id -u):$(id -g) simple-io-example \
  /output/output-$number.txt "${args_list[$number]}"

clean_up $name
