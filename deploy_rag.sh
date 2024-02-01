#!/usr/bin/env bash

#=========================================
# 
# Title: deploy_rag.sh
# Author: Andrew Naylor
# Date: Jan 24
# Brief: Deploy RAG on Perlmutter
#
#=========================================

# Variables
CMD_PID_ARRAYS=()

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' #https://en.wikipedia.org/wiki/ANSI_escape_code

#To-do: Add verbose switch

# Load config
source env.cfg

# Functions
deploy_service(){
    local SERVICE_NAME=$1
    local FUNC=$2

    #Run cmd in background
    echo "Deploying service..."
    $FUNC &

    #then save pid
    local CMD_PID=$!
    CMD_PID_ARRAYS+=($CMD_PID)
    echo $CMD_PID > ${SERVICE_NAME}.pid

}

llm(){
    podman-hpc run \
            --rm \
            --gpu \
            --network host \
            --shm-size 20g \
            --volume $MODEL_DIRECTORY:/model \
            $LLM_SERVER_IMAGE \
                $MODEL_TYPE \
                --max-input-length ${MODEL_MAX_INPUT_LENGTH:-3000} \
                --max-output-length ${MODEL_MAX_OUTPUT_LENGTH:-512} \
                --quantization ${QUANTIZATION:-None} \
                -v -v
}


control_c(){
    echo "KeyboardInterrupt detected"
    echo "Kill all services..."

    for i in "${CMD_PID_ARRAYS[@]}"
    do
        kill $i
    done

    echo "All services killed"
    exit
}
trap control_c SIGINT


#Main
main() {
    deploy_service "LLM" llm | while IFS= read -r line; do echo -e "${RED}[LLM]${NC} $line"; done

    echo "All services deployed. Ctrl + C to shutdown services..."
    wait
}


main
