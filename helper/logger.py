import argparse
import logging
import os
import pathlib

LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']


def log_level_string_to_int(log_level_string):
    log_level_string = log_level_string.upper().strip()

    if log_level_string not in LOG_LEVEL_STRINGS:
        message = f'invalid choice: {log_level_string} (choose from {LOG_LEVEL_STRINGS})'
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.INFO)
    assert isinstance(log_level_int, int)
    return log_level_int


def init_logging(log_level):
    if isinstance(log_level, str):
        log_level = log_level_string_to_int(log_level)
    os.chdir(pathlib.Path(__file__).resolve().parents[1])
    os.makedirs('logs', exist_ok=True)
    log_path = os.path.join('logs', 'log.log')
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s :: %(levelname)-6s :: %(name)s :: %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ])
