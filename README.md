# nersc_llm_prototype

## Nvidia RAG example
https://github.com/NVIDIA/GenerativeAIExamples/blob/main/RetrievalAugmentedGeneration/README.md#2-qa-chatbot----a100h100l40s-gpu

### To-do
- [ ] download + install scripts?
- [ ] Train script
- [ ] Deploy script
- [ ] Test script


## How to setup

### Step 1: Download files

Download nvidia repo to SCRATCH repo:
```bash
source env.cfg
mkdir -p $SCRATCH_DIR && cd "$_"
git clone git@github.com:NVIDIA/GenerativeAIExamples.git && cd GenerativeAIExamples
git lfs pull
```

Download LLama models:
```bash
cd $SCRATCH_DIR
git clone https://github.com/facebookresearch/llama.git
cd llama/
./download.sh #Select llama-2-13b-chat
mv tokenizer* llama-2-13b-chat/
ls llama-2-13b-chat/
```
Requires filling out [Llama request access form](https://ai.meta.com/resources/models-and-libraries/llama-downloads/).

### Step 2: Build Services
We have to build 3 out of the 6 services we are going to deploy.

#### LLM Inference Server
https://github.com/NVIDIA/GenerativeAIExamples/blob/main/RetrievalAugmentedGeneration/llm-inference-server/Dockerfile

```bash
cd $SCRATCH_DIR
cd GenerativeAIExamples/RetrievalAugmentedGeneration/llm-inference-server/
podman build --platform=linux/amd64 -f Dockerfile -t llm-inference-server:latest .
```
> [!NOTE]
> When building with podman I had a build permissions issue with the pip install line. Fixed it by copying instead of mounting the `requirments.txt` file.

> [!WARNING]
> podman-hpc currently disabled on Perlmutter.




### Step 3: Deploy

Run the script:
```bash
./deploy_rag.sh
```