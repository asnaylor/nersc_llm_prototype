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
    shifter --module=gpu \
            --volume="$MODEL_DIRECTORY:/model" \
            --image=$LLM_SERVER_IMAGE \
                /usr/bin/python3 -m model_server $MODEL_TYPE \
                --max-input-length ${MODEL_MAX_INPUT_LENGTH:-3000} \
                --max-output-length ${MODEL_MAX_OUTPUT_LENGTH:-512} \
                --quantization ${QUANTIZATION:-None}
}

sleep_test(){
    sleep 200
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
    deploy_service "LLM" llm | while IFS= read -r line; do echo "[LLM] $line"; done
    deploy_service "Test_service2" sleep_test
    deploy_service "Test_service3" sleep_test

    echo "All services deployed. Ctrl + C to shutdown services..."
    wait
}


main
