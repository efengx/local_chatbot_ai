# local chatbot ai

以在个人消费设备上运行为主要设计原则的local chatbot ai.

这是一个对于相似问题可以非常快响应的智能聊天ai.

支持RAG（外部知识库检索增强）.

```
![alt text](http://url/to/img.png)
```


## ⚡️ 快速开始

. step1: 安装依赖

```bash
# rest api 依赖
pip install -r ./docker/backend/requirements.txt
# web ui 依赖
pip install -r ./docker/frontend/requirements.txt
```

. step2: 下载models

```python
# fx_data.ipynb
from huggingface_hub import hf_hub_download

hf_hub_download(repo_id="TheBloke/Llama-2-13B-chat-GGUF",
                filename="llama-2-13b-chat.Q4_0.gguf",
                local_dir="./models/")

```

. step3: 开启本地数据微服务milvus

```python
# fx_data.ipynb
from src.local_milvus import LocalMilvus

localMilvus = LocalMilvus.instance()
localMilvus.start()
```

. step4: 开启restapi服务

```shell
$ uvicorn main_restapi:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 联系方式

如果您有任何问题、反馈意见或想要联系我们，欢迎随时通过电子邮件与我们联系： [ixiang1926@outlook.com](mailto:ixiang1926@outlook.com)
