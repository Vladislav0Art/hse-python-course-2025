import select
from multiprocessing import Queue, Process
from threading import Thread, Event
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


def main_routine(logger: logging.Logger, input_queue: Queue, output_queue: Queue, run_event: Event):
    try:
        while run_event.is_set():
            if select.select([sys.stdin], [], [], 0.1)[0]:
                line = sys.stdin.readline()
                line = line.strip()
                logger.info("sending '%s'", line)
                input_queue.put(line)

                transformed_line = output_queue.get()
                logger.info("received '%s'", transformed_line)
    except KeyboardInterrupt:
        logger.info("received KeyboardInterrupt")
    finally:
        # notify no more input will be provided
        input_queue.close()


def process_routine(whoami: str, log_filepath: str, input_queue: Queue, output_queue: Queue, transformation: Callable[[str], str]):
    logger = prepare_logger(f"communication-{whoami}", filepath=log_filepath)
    try:
        while True:
            line = input_queue.get()
            if line is None:
                logger.info("read None. Breaking...")
                break
            logger.info("read '%s'", line)

            transformed_line = transformation(line)
            logger.info("transformed into '%s'", transformed_line)
            logger.info("sending '%s'", transformed_line)

            output_queue.put(transformed_line)
            if whoami == 'A':
                timeout_s = 5
                logger.info("sleeping for %d seconds", timeout_s)
                time.sleep(timeout_s)
                logger.info("woke up!")
    except KeyboardInterrupt:
        logger.info("received KeyboardInterrupt")
    finally:
        # notifying that no more events will be sent
        logger.info("stopped")
        output_queue.close()


def main(logger: logging.Logger, log_filepath: str):
    # stdin -> main -> A ->_{lower()} B ->_{rot13} main
    # create processes
    queue_main_A = Queue()
    queue_A_B = Queue()
    queue_B_main = Queue()

    processA = Process(target=process_routine, name='A', args=('A', log_filepath, queue_main_A, queue_A_B, lower))
    processB = Process(target=process_routine, name='B', args=('B', log_filepath, queue_A_B, queue_B_main, rot13))
    processA.start()
    processB.start()

    run_event = Event()
    run_event.set()
    communication_thread = Thread(target=main_routine, name='communicator',
                                  args=(logger, queue_main_A, queue_B_main, run_event))
    communication_thread.start()

    try:
        while communication_thread.is_alive():
            communication_thread.join(timeout=0.1)
    except KeyboardInterrupt as e:
        label = "main"
        # logger.exception("Received exception during communication:", exc_info=e)
        logger.exception("received exception during communication")

        logger.info("terminating communication thread...")
        run_event.clear()
        communication_thread.join()
        # terminate subprocesses
        logger.info("terminating processes...")
        processA.join()
        processB.join()
        logger.info("finished")

if __name__ == "__main__":
    artifacts_dir = create_artifacts_dir(dirname="task3")
    log_filepath = os.path.join(artifacts_dir, "execution.log")

    logger = prepare_logger("communication", filepath=log_filepath)
    main(logger, log_filepath)
