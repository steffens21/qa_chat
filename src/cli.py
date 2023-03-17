"""Command line interface for the chatbot."""

import os
import logging
import argparse

from rich import print
from rich.logging import RichHandler


def setup_logging(is_debug=False):
    """
    Setup basic logging using the RichHandler.
    """
    log_level = os.environ.get("LOG_LEVEL", logging.ERROR)
    if is_debug:
        log_level = logging.DEBUG
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )


def calc_embeddings():
    pass


def qa_chat():
    pass
