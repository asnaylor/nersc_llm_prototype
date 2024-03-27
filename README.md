# NERSC LLM Prototype

This repo is how to deploy an LLM backend on Perlmutter.

!["Picture of NERSC LLM Prototype diagram"](img/nersc_llm_v2.drawio.png)

# Run

## Deploy backend

To deploy one of the supported backend you can use this in a slurm job:
```bash
module load python/3.11
python -m nersc_llm [backend-type] <cli-args>
```

| Backend | backend-name |
|---|---|
| [vLLM](https://docs.vllm.ai/en/latest/) | `vllm` [WIP] |
| [Triton + TensorRT-LLM](https://github.com/triton-inference-server/tensorrtllm_backend) | `tritontrt` [WIP] |
| [HF Text Generation Inference](#huggingface-text-generation-inference) | `tgi` |


### HuggingFace Text Generation Inference

https://huggingface.co/docs/text-generation-inference/en/index 

Example deploy:
```bash
python -m nersc_llm tgi --hf_home $SCRATCH/huggingface --hf_token <HF_TOKEN> --model_id HuggingFaceH4/zephyr-7b-beta --port 9090
```


## Client

### curl

Example curl:
```bash
curl $ADDRESS:9090/generate \
    -X POST \
    -d '{"inputs":"How can i cancel my slurm job?","parameters":{"max_new_tokens":100}}' \
    -H 'Content-Type: application/json'
```

### python requests

Example script:
```python
import requests

headers = {
    "Content-Type": "application/json",
}

data = {
    'inputs': 'How can i cancel my slurm job?',
    'parameters': {
        'max_new_tokens': 100,
    },
}

response = requests.post('http://127.0.0.1:9090/generate', headers=headers, json=data)
print(response.json())
```

--- 

# Notes 

- WIP