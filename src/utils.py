"""Utility functions for the project."""

from typing import Generator
import json


def read_scraper_output(path: str) -> Generator:
    """
    Read scraper output and yield parsed input.
    """
    lines = list()
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            line_data = json.loads(line)
            yield line_data
