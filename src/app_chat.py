# 任务：（llamaindex）加载内容
# 参考：https://gpt-index.readthedocs.io/en/v0.8.25/examples/llm/llama_2_llama_cpp.html
# 参考：https://www.sbert.net/docs/pretrained_models.html
from langchain.embeddings import HuggingFaceEmbeddings
from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
)
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt


class AppChat:
    progress: int = 0
    maxProgress: int = 5
    
    def step(self):
        if hasattr(self, "isOpen"):
            return
        else:
            self.isOpen=True
        
        self.progress += 1
        print(self.progress)
        self.llm = self.createLLM()
        self.progress += 1
        print(self.progress)
        self.embed_model = self.createEmbedModel()
        self.progress += 1
        print(self.progress)
        self.index = self.createIndex()
        self.progress += 1
        print(self.progress)
        self.query_engine = self.createQueryEngine()
        self.progress += 1
        print(self.progress)
    
    def createLLM(self, modelPath="./models/llama-2-13b-chat.Q4_0.gguf"):
        # model_url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf"
        return LlamaCPP(
            # You can pass in the URL to a GGML model to download it automatically
            model_url=None,
            # optionally, you can set the path to a pre-downloaded model instead of model_url
            model_path=modelPath,
            temperature=0.1,
            max_new_tokens=256,
            # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
            context_window=3900,
            # kwargs to pass to __call__()
            generate_kwargs={},
            # kwargs to pass to __init__()
            # set to at least 1 to use GPU
            # model_kwargs={"n_gpu_layers": 1},
            # transform inputs into Llama2 format
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=True,
        )
    
    def createEmbedModel(self, modelName="sentence-transformers/all-mpnet-base-v2"):
        # use Huggingface embeddings
        return HuggingFaceEmbeddings(
            model_name=modelName
        )
    
    def createIndex(self, inputDir="./data/"):
        # create a service context
        service_context = ServiceContext.from_defaults(
            llm=self.llm,
            embed_model=self.embed_model,
        )
        documents = SimpleDirectoryReader(inputDir).load_data()
        return VectorStoreIndex.from_documents(documents, service_context=service_context)
    
    def createQueryEngine(self):
        return self.index.as_query_engine()

    def query(self, query):
        return self.query_engine.query(query)