FROM ubuntu
RUN apt-get update && apt-get install -y make \
build-essential \
python-dev \
gcc \
g++ \
libigraph0-dev \
libxml2-dev \
libz-dev \
virtualenv \
time

RUN mkdir /benchmark
COPY . /benchmark
RUN virtualenv /benchmark/venv
RUN cd /benchmark && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
CMD cd /benchmark && . venv/bin/activate && ./benchmark_run.sh


