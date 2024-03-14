#!/usr/bin/env bash

#=========================================
# 
# Title: deploy.sh
# Author: Andrew Naylor
# Date: Mar 24
# Brief: Deploy Triton + TensorRT-LLM on Perlmutter
#
#=========================================

# Load config
source env.cfg

# Script name for reference in help message
script_name=$(basename "$0")

# Define functions
function print_run {
    # print the function and then run
    if [[ "$verbose" = true ]]; then
        echo "$@"
    fi
    "$@"
}

function help {
  echo "Usage: $script_name [OPTION]... [ARGUMENTS]..."
  echo ""
  echo "Options:"
  echo "  -h, --help      Display this help message."
  echo "  -v, --verbose  Enable verbose output."
  
  echo ""
  echo "Arguments:"
  echo "  setup - Copy across LLama model and pull LLM container image"
  echo "  run - Deploy Triton + TensorRT-LLM"
  
  echo ""
  echo "Example:"
  echo "  $script_name -v [setup|run]"
  exit 0
}

# Process arguments
while getopts ":hv" opt; do
  case $opt in
    h)
      help
      ;;
    v)
      verbose=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# Shift arguments to remove processed options
shift $((OPTIND-1))

# Check for remaining arguments
if [ $# -eq 0 ]; then
  echo "Error: Please provide at least one argument."
  help
  exit 1
fi

#Set verbose
if [[ "$verbose" = true ]]; then
  echo "Verbose mode enabled."
  run_verbose_flags="-v -v"
fi

#Main
case $1 in
  setup)
    echo "<> Executing setup..."
    print_run mkdir -p $SCRATCH_DIR
    print_run cp -r $LLAMA_MODEL_DIR $MODEL_DIR
    # print_run module load python; python -m pip install langchain #need to install triton + langchain
    print_run podman-hpc pull $LLM_SERVER_IMAGE
    echo "<> Setup complete..."
    ;;
  run)
    echo "<> Deploying Triton + TensorRT-LLM"
    if [ -z "$SLURM_JOBID" ]; then
        echo "Error: As this process is very GPU intensive please run this in a slurm job. See the README for instructions."
        exit 1
    fi
    
    print_run podman-hpc run \
                -it \
                --rm \
                --gpu \
                --network host \
                --shm-size 20g \
                --volume $MODEL_DIR:/model \
                $LLM_SERVER_IMAGE \
                    $MODEL_TYPE \
                    --max-input-length ${MODEL_MAX_INPUT_LENGTH:-3000} \
                    --max-output-length ${MODEL_MAX_OUTPUT_LENGTH:-512} \
                    --quantization ${QUANTIZATION:-None} \
                    $run_verbose_flags
    ;;
  *)
    echo "Error: '$1' is not a valid arg"
    exit 1
    ;;
esac
