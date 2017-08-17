FROM ubuntu
RUN apt-get update && apt-get install -y make \
build-essential \
gcc
RUN mkdir /myvol
COPY T1.c /myvol

CMD cd /myvol && gcc -o test T1.c && ./test file1 testing
