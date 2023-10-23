import os
import langchain
from loguru import logger
# from langchain.callbacks import FileCallbackHandler
from src.chatbot.fx_llamacpp import LlamaCpp
from src.chatbot.fx_cache import FxCache
from langchain.cache import GPTCache
from src.chatbot.fx_open_llm import FxOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from src.chatbot.fx_chat_openai import FxChatOpenAI
from langchain.chains import LLMChain
from src.chatbot.fx_stuff_documents_chain import FxStuffDocumentsChain
from langchain.document_transformers import LongContextReorder
from langchain.vectorstores import Milvus
from langchain.llms import OpenAI
from src.chatbot.fx_chain_llm import FxLLMChain
from langchain.prompts import PromptTemplate
from src.chatbot.fx_callback import FxStdOutCallbackHandler
from src.chatbot.fx_llm import FxLLM
from dotenv import load_dotenv

load_dotenv()

# logfile = "output.log"
# logger.add(logfile, colorize=True, enqueue=True)
# handler = FileCallbackHandler(logfile)

class FxChat(object):

    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance FxChat')
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance
    
    step: int = 0
    model_type: str = ""

    def _load_cache(self):
        print(f"FxChat._load_cache: {self.step}")
        fxCache = FxCache.instance()
        langchain.llm_cache = GPTCache(fxCache.fx_init_cache)                             # 组合结构
        self.step = 1

    def _load_FxOpenAI(self):
        print(f"FxChat._load_FxOpenAI: {self.step} {self.model_type}")
        if self.model_type == "FxOpenAI":
            return

        os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
        
        self.step = 1
        self.model_type = "FxOpenAI"
        # self.llm = FxOpenAI(model_name="text-davinci-002", n=2, best_of=2)
        self.llm = FxOpenAI(model_name="gpt-4")
        self.step = 2

    def _load_llama2_chat_q4(self):
        print(f"FxChat._load_llama2_chat_q4: {self.step} {self.model_type}")
        if self.model_type == "LlamaCpp":
            return

        self.step = 1
        self.model_type = "LlamaCpp"
        self.llm = LlamaCpp(
            model_path="./models/llama-2-13b-chat.Q4_0.gguf",
            temperature=0.1,
            max_tokens=2000,
            verbose=True,                                               # Verbose is required to pass to the callback manager
        )
        self.step = 2

    def _load_fxllm(self):                                              # 自定义模型
        self.llm = FxLLM(n=10)
        self.step = 2

    def _load_chat_openai(self):
        # gpt-3.5-turbo and gpt-4 模型需要使用该model
        self.step = 1
        self.model_type = "ChatOpenAI"
        self.llm = FxChatOpenAI(model_name="gpt-3.5-turbo")
        self.step = 2

    def predict(self, question):                                                # 预测
        if self.step != 2:
            return  "模型加载中请稍后!"
        
        result = self.llm(question)
        return result

    def chainLlm(self, template_prompt: str, question: str):                    # 聊天链
        if self.step != 2:
            return "模型加载中请稍后!"
        
        handler = FxStdOutCallbackHandler()
        prompt = PromptTemplate(
            input_variables=["question"],
            template=template_prompt,
        )
        chain = FxLLMChain(llm=self.llm, prompt=prompt)
        
        result = chain.run(question, callbacks=[handler])
        return result

    def chainRagLlm(self, template_prompt: str, question: str, document: list):
        prompt = PromptTemplate(
            template=template_prompt, 
            input_variables=["context", "question"]
        )
        llm_chain = FxLLMChain(llm=self.llm, prompt=prompt)
        
        # 通过document重构提示模版
        document_prompt = PromptTemplate(
            input_variables=["page_content"], template="{page_content}"
        )
        # 该值与prompt中的template_prompt对应
        document_variable_name = "context"
        chain = FxStuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=document_prompt,
            document_variable_name=document_variable_name,
        )
        
        # 创建一个检索器，获取与question相关的文档
        if not hasattr(self, "embeddings"):
            self.embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")

        retriever = Milvus.from_texts(
            [document], 
            embedding=self.embeddings,
            connection_args={"host": os.getenv('MILVUS_HOST')}).as_retriever(search_kwargs={"k": 1})
        docs = retriever.get_relevant_documents(question)
        print("docs=", docs)
        # 重新对文档进行排序，相关性较高的位于文档的开头和结尾，相关性较低的位于中间
        # reordering = LongContextReorder()
        # reordered_docs = reordering.transform_documents(docs)
        # print("reordered_docs=", reordered_docs)
        # handler = FxStdOutCallbackHandler()
        result = chain.run(input_documents=docs, question=question)
        return result
