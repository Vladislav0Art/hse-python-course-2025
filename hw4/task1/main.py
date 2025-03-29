import logging
import threading
import multiprocessing
import time

def measure_execution_time(block, *args, **kwargs):
    start_time = time.time()
    block(*args, **kwargs)
    end_time = time.time()

    elapsed_time = end_time - start_time
    return elapsed_time


def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1

    prev = 0 # n = 0
    curr = 1 # n = 1

    for i in range(2, n + 1):
        prev, curr = curr, prev + curr

    return curr


def execute_threads(n: int, threads_count: int) -> None:
    """Execute fibonacci function in multiple threads."""
    threads = []

    for i in range(threads_count):
        thread = threading.Thread(target=fibonacci, args=(n,))
        thread.name = f"thread-{i}"
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def execute_processes(n: int, processes_count: int) -> None:
    """Execute fibonacci function in multiple processes."""
    processes = []

    for i in range(processes_count):
        process = multiprocessing.Process(target=fibonacci, args=(n,))
        process.name = f"process-{i}"
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


def execute_sequential(n: int, count: int) -> None:
    """Execute fibonacci function in sequential manner."""
    for i in range(count):
        fibonacci(n)


def main(n: int, times: int):
    # function, tag
    executions = [
        (execute_sequential, "execute_sequential"),
        (execute_threads, "execute_threads"),
        (execute_processes, "execute_processes"),
    ]

    logging.info("Running fibonacci(%d) %d times in %d different scenarios", n, times, len(executions))

    for execution in executions:
        function, tag = execution
        # logging.info("Running %s", tag)

        time_elapsed_s = measure_execution_time(function, n, times)
        # logging.info("Execution time for '%s': %.6f seconds", block.__name__, elapsed_time)
        logging.info("[%s] fibonacci(%d) required: %.6f seconds", tag, n, time_elapsed_s)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s: [process: %(processName)s, thread: %(threadName)s] %(levelname)s: %(message)s"
    )
    main(n=300_000, times=10)
