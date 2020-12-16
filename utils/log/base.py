import logging
import logging.config
import os


def get_logger(name):
    filename = os.path.join(os.path.dirname(__file__), "logging.conf")
    logging.config.fileConfig(filename)

    return logging.getLogger(name)
