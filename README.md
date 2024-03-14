# NERSC Perlmutter Triton + TensorRT-LLM Demo

This demo uses content from this repo https://github.com/NVIDIA/GenerativeAIExamples/tree/main 

## Setup

To copy across the model files and download the container image on Perlmutter run on a login node:
```bash
./deploy.sh setup
```

## Deploy

Once the setup is complete, start up an interactive slurm job (replacing your account):
```bash
salloc -N 1 -C gpu -G 4 --gpu-bind=closest -t 01:00:00 -q interactive -A <account>
```

Inside the slurm job run:
```bash
./deploy.sh run
```

## Connect & Test

Open up [notebook.ipynb](notebook.ipynb) to connect to the LLM container and test.