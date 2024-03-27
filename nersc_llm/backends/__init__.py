import typing
import logging
import subprocess
import os

from enum import Enum, auto

_LOGGER = logging.getLogger(__name__)


class valid_backends(Enum):
    """A enumerator of the valid backends."""
    vllm = auto()
    tritontrt = auto()
    tgi = auto()


class Backend:
    """Template class for LLM backends."""

    def __init__(self, args) -> None:
        """Intialise the backend class."""
        pass

    @property
    def _cmd(self) -> typing.List[str]:
        """Generate the full command."""
        cmd = ['ls']
        return cmd
    
    @property
    def _env(self) -> typing.Dict[str, str]:
        """Return the environment variable for the triton inference server."""
        env = dict(os.environ)
        return env

    def run(self) -> int:
        """Start the backend server."""
        cmd = self._cmd
        env = self._env

        _LOGGER.debug("Starting server with the command: %s", " ".join(cmd))
        _LOGGER.debug("Starting server with the env vars: %s", repr(env))
        with subprocess.Popen(cmd, env=env) as proc:
            try:
                retcode = proc.wait()
            except KeyboardInterrupt:
                proc.kill()
                return 0
        return retcode
    
class vLLMBackend(Backend):
    """A class to deploy the vLLMBackend."""
    def __init__(self, args):
        super().__init__(args)


class tritontrtllmBackend(Backend):
    """A class to deploy the tritontrtllmBackend."""
    def __init__(self, args):
        super().__init__(args)

class tgiBackend(Backend):
    """A class to deploy the tgiBackend."""
    def __init__(self, args):
        super().__init__(args)
