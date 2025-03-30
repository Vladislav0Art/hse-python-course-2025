# Report

## Task 4.1

1. The implementation script resides at [task1/main.py](./task1/main.py).
2. See the execution log at [artifacts/task1/execution.log](./artifacts/task1/execution.log).

Since the calculation of the Fibonacci function is a CPU-bound problem (not IO-bound), threading does not improve the performance of the sequential approach.
The approach with processes, on the other hand, introduces a significant improvement in performance due to real parallelism.


## Task 4.2

1. The implementation script resides at [task2/main.py](./task2/main.py).
2. See the execution log at [artifacts/task2/execution.log](artifacts/task2/execution.log).

As expected, because the given task is CPU-bound (not IO-bound), an increase in the number of threads does not yield any improvement in terms of performance (due to GIL).
Unlike for threads, creation of additional processes introduces performance improvement up to a certain point when the overhead of process management (creation and stopping) prevails.


## Task 4.3

1. The implementation script resides at [task3/main.py](./task3/main.py).
1. See the communication log at [artifacts/task3/execution.log](./artifacts/task3/execution.log).

The implementation creates two processes, A and B,
and three interprocess message-passing queues to facilitate communication in the direction `main -> A -> B -> main`.
The main process creates an additional communication thread that conducts non-blocking reading from stdin and sends the lines to the queue.
This additional thread in the main process is required to implement graceful shutdown on `KeyboardInterrupt`.