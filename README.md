# local chatbot ai

Local chatbot ai with the main design principle of running on personal consumer devices.

This is an intelligent chat AI that can respond very quickly to similar questions.

Supports RAG (Retrieval Augmentation for External Knowledge Bases).

![alt text](https://github.com/efengx/local_chatbot_ai/blob/main/resource/chat_1.jpg?raw=true)

![alt text](https://github.com/efengx/local_chatbot_ai/blob/main/resource/data_1.jpg?raw=true)

## ⚡️ Quick start

. step1: Install dependencies

```bash
# rest api 依赖
pip install -r ./docker/backend/requirements.txt
# web ui 依赖
pip install -r ./docker/frontend/requirements.txt
```

. step2: Download models

```python
# fx_data.ipynb
from huggingface_hub import hf_hub_download

hf_hub_download(repo_id="TheBloke/Llama-2-13B-chat-GGUF",
                filename="llama-2-13b-chat.Q4_0.gguf",
                local_dir="./models/")

```

. step3: Start the local data microservice milvus

```python
# fx_data.ipynb
from src.local_milvus import LocalMilvus

localMilvus = LocalMilvus.instance()
localMilvus.start()
```

. step4.1: Start restapi service

```shell
$ uvicorn main_restapi:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

. step4.2: Start web ui service

```bash
$ streamlit run main_web.py
```

## Contact

If you have any questions, feedback or would like to contact us, please feel free to contact us via email: [ixiang1926@outlook.com](mailto:ixiang1926@outlook.com)
