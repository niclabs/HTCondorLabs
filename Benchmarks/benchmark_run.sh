#!/bin/bash
# file name: benchmark_run.sh

mkdir results

echo "Running 100 nodes test"
cat > results/100nodes_test.txt << EOF1
100 node test
EOF1
time ./benchmark_run_100nodes.sh > results/100nodes_test.txt
echo '20 tests' >> results/100nodes_test.txt

echo "Running 200 nodes test"
cat > results/200nodes_test.txt << EOF1
200 node test
EOF1
time ./benchmark_run_200nodes.sh > results/200nodes_test.txt
echo '20 tests' >> results/200nodes_test.txt

echo "Running 500 nodes test"
cat > results/500nodes_test.txt << EOF1
500 node test
EOF1
time ./benchmark_run_100nodes.sh > results/500nodes_test.txt
echo '10 tests' >> results/500nodes_test.txt
