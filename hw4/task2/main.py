import logging
import os.path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from hw4.utils import prepare_logger, create_artifacts_dir
import math

def integrate_slow(f, a, b, *, n_jobs=1, n_iter=10000000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate(f, a, b, *, create_executor, n_jobs=1, n_iter=10000000):
    def integrate_chunk(f, a, *, step, start: int, end: int):
        acc = 0
        for i in range(start, end):
            acc += f(a + i * step) * step
        return acc

    with create_executor(n_jobs) as executor:
        futures = []
        step = (b - a) / n_iter

        # start chunked execution
        for i in range(n_jobs):
            chunk_start = math.floor(i * n_iter / n_jobs)
            chunk_end = math.ceil((i + 1) * n_iter / n_jobs)
            print(f"chunk: [{chunk_start}, {chunk_end})")

            task = lambda start, end: integrate_chunk(f, a, step=step, start=start, end=end)
            future = executor.submit(task, chunk_start, chunk_end)
            futures.append(future)

        # collect results
        acc = 0
        for future in futures:
            acc += future.result()

        return acc


def main(logger: logging.Logger):
    def create_thread_pool(workers_count: int):
        return ThreadPoolExecutor(max_workers=workers_count, thread_name_prefix="thread-")
    def create_process_pool(workers_count: int):
        return ProcessPoolExecutor(max_workers=workers_count)

    result = integrate(math.cos, a=0, b=math.pi / 2, create_executor=create_thread_pool, n_jobs=10)
    result_slow = integrate_slow(math.cos, a=0, b=math.pi / 2)

    print(f"result: {result}")
    print(f"result_slow: {result_slow}")
    # logger.info("result: %f", result)


if __name__ == "__main__":
    artifacts_dir = create_artifacts_dir(dirname="task1")
    log_filepath = os.path.join(artifacts_dir, "execution.log")

    logger = prepare_logger("integrate", filepath=log_filepath)
    main(logger)