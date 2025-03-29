from logging import Logger
from multiprocessing import Queue, Process
from typing import Callable, Any
import codecs
import logging
import os
import sys
import time

from hw4.utils import create_artifacts_dir, prepare_logger


def rot13(s: str) -> str:
    return codecs.encode(s, "rot_13")

def lower(s: str) -> str:
    return s.lower()


def process_routine(whoami: str, logger: logging.Logger, input_queue: Queue, output_queue: Queue, transformation: Callable[[str], str]):
    while True:
        line = input_queue.get()
        if line is None:
            logger.info("[%s]: read None. Breaking...", whoami)
            break
        logger.info("[%s]: read '%s'", whoami, line)

        transformed_line = transformation(line)
        logger.info("[%s]: transformed into '%s'", whoami, line)
        logger.info("[%s]: sending '%s'", whoami, line)

        output_queue.put(transformed_line)
        if whoami == 'A':
            timeout_s = 5
            logger.info("[%s]: sleeping for %d seconds", whoami, timeout_s)
            time.sleep(timeout_s)
            logger.info("[%s]: woke up!", whoami)

    logger.info("[%s]: stopped", whoami)
    # notifying that no more events will be sent
    output_queue.close()

def main(logger: logging.Logger):
    # stdin -> main -> A ->_{lower()} B ->_{rot13} main
    # create processes
    queue_main_A = Queue()
    queue_A_B = Queue()
    queue_B_main = Queue()

    label = "main"

    processA = Process(target=process_routine, name='A', args=('A', logger, queue_main_A, queue_A_B, lower))
    processB = Process(target=process_routine, name='B', args=('B', logger, queue_A_B, queue_B_main, rot13))

    try:
        processA.start()
        processB.start()

        for line in sys.stdin:
            line = line.strip()
            logger.info("[%s]: sending '%s'", label, line)
            queue_main_A.put(line)

            transformed_line = queue_B_main.get()
            logger.info("[%s]: received '%s'", label, transformed_line)
    except KeyboardInterrupt as e:
        logger.exception("Received exception during communication:", exc_info=e)
    finally:
        # no more events sent by main
        queue_main_A.close()
        # terminate subprocesses
        processA.join()
        processB.join()

if __name__ == "__main__":
    artifacts_dir = create_artifacts_dir(dirname="task3")
    log_filepath = os.path.join(artifacts_dir, "execution.log")

    logger = prepare_logger("communication", filepath=log_filepath)
    main(logger)
