import logging
import os.path
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from hw4.utils import prepare_logger, create_artifacts_dir, measure_execution_time
import math


def integrate_chunk(f, a, *, step, start: int, end: int):
    acc = 0
    for i in range(start, end):
        acc += f(a + i * step) * step
    return acc


def integrate(f, a, b, *, create_executor, n_jobs=1, n_iter=10000000):
    with create_executor(n_jobs) as executor:
        futures = []
        step = (b - a) / n_iter

        # start chunked execution
        for i in range(n_jobs):
            chunk_start = math.floor(i * n_iter / n_jobs)
            chunk_end = math.ceil((i + 1) * n_iter / n_jobs)

            # task = lambda start, end: integrate_chunk(f, a, step=step, start=start, end=end)
            # future = executor.submit(task, chunk_start, chunk_end)
            future = executor.submit(integrate_chunk, f, a, step=step, start=chunk_start, end=chunk_end)
            futures.append(future)

        # collect results
        acc = 0
        for future in futures:
            acc += future.result()

        return acc


def create_thread_pool(workers_count: int):
    return ThreadPoolExecutor(max_workers=workers_count, thread_name_prefix="thread-")
def create_process_pool(workers_count: int):
    return ProcessPoolExecutor(max_workers=workers_count)

def integrate_on_threads(n_jobs: int):
    return integrate(math.cos, a=0, b=math.pi / 2, create_executor=create_thread_pool, n_jobs=n_jobs)
def integrate_on_processes(n_jobs: int):
    integrate(math.cos, a=0, b=math.pi / 2, create_executor=create_process_pool, n_jobs=n_jobs)


def main(logger: logging.Logger):
    max_threads = os.cpu_count() * 2

    for jobs in range(1, max_threads + 1):
        threads_elapsed_time_s = measure_execution_time(integrate_on_threads, n_jobs=jobs)
        processes_elapsed_time_s = measure_execution_time(integrate_on_processes, n_jobs=jobs)

        logger.info("n_jobs: %d, threads_elapsed_time: %.6f, processes_elapsed_time: %.6f",
                    jobs, threads_elapsed_time_s, processes_elapsed_time_s)


if __name__ == "__main__":
    artifacts_dir = create_artifacts_dir(dirname="task2")
    log_filepath = os.path.join(artifacts_dir, "execution.log")

    logger = prepare_logger("integrate", filepath=log_filepath)
    main(logger)