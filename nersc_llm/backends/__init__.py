import typing
import logging
import subprocess
import os
import yaml

from enum import Enum, auto
from shlex import split
from pathlib import Path

_LOGGER = logging.getLogger(__name__)

class yamlConfig:
  def __init__(self, data):
    for key, value in data.items():
      setattr(self, key, value)

def _read_yaml_config(backend: typing.AnyStr):
    """Read the yaml config for the backend."""

    backends_dir = Path(__file__).resolve().parent
    backend_yaml_file = f"{backends_dir}/{backend}.yml"

    _LOGGER.debug("Reading config file: %s", backend_yaml_file)
    with open(backend_yaml_file) as stream:
        try:
            return yamlConfig(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            _LOGGER.error("YAMLError: %s", exc)
    return

class valid_backends(Enum):
    """A enumerator of the valid backends."""
    vllm = auto()
    tritontrt = auto()
    tgi = auto()


class Backend:
    """Template class for LLM backends."""

    def __init__(self, args) -> None:
        """Intialise the backend class."""
        self.hf_home = self._get_os_var('HF_HOME', args.hf_home)
        self.hf_token = self._get_os_var('HF_TOKEN', args.hf_token)
        self.port = args.port
        pass

    def _get_os_var(self, env_var, arg_var):
        """Get the env variable if exist."""
        return os.getenv(env_var, arg_var)

    @property
    def _cmd(self) -> None:
        """Generate the full command."""
        pass
    
    @property
    def _env(self) -> typing.Dict[str, str]:
        """Return the environment variable for the triton inference server."""
        env = dict(os.environ)
        return env

    def run(self) -> int:
        """Start the backend server."""
        cmd = split(self._cmd)
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
        self.backend = 'vLLM'
        self._yamlConfig = _read_yaml_config(self.backend)
        self.container_img = self._yamlConfig.container_img
        super().__init__(args)

    @property
    def _cmd(self) -> typing.AnyStr:
        """Generate the full command."""
        cmd = 'ls'
        return cmd


class tritontrtllmBackend(Backend):
    """A class to deploy the tritontrtllmBackend."""
    def __init__(self, args):
        self.backend = 'tritontrtllm'
        self._yamlConfig = _read_yaml_config(self.backend)
        self.container_img = self._yamlConfig.container_img
        super().__init__(args)

    @property
    def _cmd(self) -> typing.AnyStr:
        """Generate the full command."""
        cmd = 'pwd'
        return cmd

class tgiBackend(Backend):
    """A class to deploy the tgiBackend."""
    def __init__(self, args):
        self.backend = 'tgi'
        self._yamlConfig = _read_yaml_config(self.backend)
        self.container_img = self._yamlConfig.container_img
        self.model_id = args.model_id
        super().__init__(args)

    @property
    def _cmd(self) -> typing.AnyStr:
        """Generate the full command."""
        cmd = (
            f'podman-hpc'
            f'  run'
            f'  --rm'
            f'  --name {self.backend}_backend'
            f'  --gpu'
            f'  --shm-size=1g'
            f'  --ulimit memlock=-1'
            f'  -p {self.port}:80'
            f'  -v {self.hf_home}:/data'
            f' {f"-e HF_TOKEN={self.hf_token}" if self.hf_token else ""}'
            f'  {self.container_img}'
            f'      --model-id {self.model_id}'
        )
        return cmd
