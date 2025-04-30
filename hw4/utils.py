import os
import logging
import time


def measure_execution_time(block, *args, **kwargs):
    start_time = time.time()
    block(*args, **kwargs)
    end_time = time.time()

    elapsed_time = end_time - start_time
    return elapsed_time



def create_artifacts_dir(dirname: str) -> str:
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = os.path.join(cur_dir, "artifacts", dirname)
    os.makedirs(artifacts_dir, exist_ok=True)

    return artifacts_dir


def prepare_logger(logger_name: str, filepath: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s: [process: %(processName)s, thread: %(threadName)s] %(levelname)s: %(message)s")

    # log into stdout and file
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filepath)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
