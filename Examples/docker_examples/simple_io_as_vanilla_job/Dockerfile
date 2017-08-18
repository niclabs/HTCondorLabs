FROM ubuntu

RUN apt-get update && apt-get install -y make \
build-essential \
gcc

RUN mkdir /job && mkdir /output

COPY echo_to_file.c /job/

RUN cd /job && gcc -o echo_to_file echo_to_file.c

WORKDIR /job

ENTRYPOINT ["./echo_to_file"] 
