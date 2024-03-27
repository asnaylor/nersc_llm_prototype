import argparse
import logging
import os

from .backends import valid_backends, vLLMBackend, tritontrtllmBackend, tgiBackend

_LOGGER = logging.getLogger(__name__)

def main(args: argparse.Namespace) -> int:
    """Deploy the backend."""
    
    if (not "SLURM_JOBID" in os.environ) and (not args.force):
        _LOGGER.debug("Not running in a slurm job")
        raise RuntimeError("Not running in a slurm job. To run on a login node use `--force` but consider other users")

    _LOGGER.info(f"Deploying the {args.backend} backend")

    args.backend = valid_backends[args.backend]

    if args.backend == valid_backends.vllm:
        inference_server = vLLMBackend(args)

    elif args.backend == valid_backends.tritontrt:
        inference_server = tritontrtllmBackend(args)

    elif args.backend == valid_backends.tgi:
        inference_server = tgiBackend(args)

    return inference_server.run()