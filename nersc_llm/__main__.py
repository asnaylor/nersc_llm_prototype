"""Main script for deploying LLM backends on Perlmutter."""
import argparse
import logging
import os
import sys

from . import main
from .backends import valid_backends
from pathlib import Path

_LOG_FMT = f"[{os.getpid()}] %(asctime)15s [%(levelname)7s] - %(name)s - %(message)s"
_LOG_DATE_FMT = "%b %d %H:%M:%S"
_LOGGER = logging.getLogger("main")

def _bootstrap_logging(verbosity: int = 0) -> None:
    """Configure Python's logger according to the given verbosity level.

    :param verbosity: The desired verbosity level. Must be one of 0, 1, or 2.
    :type verbosity: typing.Literal[0, 1, 2]
    """
    # determine log level
    verbosity = min(2, max(0, verbosity))  # limit verbosity to 0-2
    log_level = [logging.WARN, logging.INFO, logging.DEBUG][verbosity]

    # configure python's logger
    logging.basicConfig(format=_LOG_FMT, datefmt=_LOG_DATE_FMT, level=log_level)
    # update existing loggers
    _LOGGER.setLevel(log_level)
    # pylint: disable-next=no-member; false positive
    for logger_name in logging.root.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers:
            handler.setFormatter(logging.Formatter(fmt=_LOG_FMT, datefmt=_LOG_DATE_FMT))

def parse_args() -> argparse.Namespace:
    """Parse the comamnd line arguments."""
    parser = argparse.ArgumentParser(
        prog="nersc_llm",
        description="Deploy different LLM backends on Perlmutter",
    )

    #required
    parser.add_argument("backend", choices=[backend.name for backend in valid_backends], help="Select valid backend")

    #optional
    parser.add_argument("--hf_home", action="store", default=f"{Path.home()}/.cache/huggingface", help="Set the HuggingFace home folder (%(default)s). Does not override $HF_HOME env.")
    parser.add_argument("-v", "--verbose", action="count", default=1, help="Increase output verbosity")
    parser.add_argument("-q", "--quiet", action="count", default=0, help="Decrease output verbosity")

    args = parser.parse_args()

    return args 

if __name__ == "__main__":
    _ARGS = parse_args()
    _bootstrap_logging(_ARGS.verbose - _ARGS.quiet)
    sys.exit(main(_ARGS))



#Structure code taken from https://github.com/NVIDIA/GenerativeAIExamples/blob/main/RetrievalAugmentedGeneration/llm-inference-server/model_server/__main__.py