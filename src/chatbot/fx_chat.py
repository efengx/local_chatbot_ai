import os
import langchain
from loguru import logger
# from langchain.callbacks import FileCallbackHandler
from src.chatbot.fx_llamacpp import LlamaCpp
from src.chatbot.fx_cache import FxCache
from langchain.cache import GPTCache
from src.chatbot.fx_open_llm import FxOpenAI
from langchain.chains import LLMChain
from src.chatbot.fx_chain_llm import FxLLMChain
from langchain.prompts import PromptTemplate
from src.chatbot.fx_callback import FxStdOutCallbackHandler
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
            cls._init(cls)
            
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance
    
    step: int = 0
    model_type: str = ""
    
    def _init(self):
        print(f"FxChat.init: {self.step}")
        self._load_cache(self)
        self._load_llama2_chat_q4(self)

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
        self.llm = FxOpenAI(model_name="text-davinci-002", n=2, best_of=2)
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

    def predict(self, text):                                            # 预测
        if self.step != 2:
            return  "模型加载中请稍后!"
        
        result = self.llm(text)
        return result

    def chainllm(self, text):                                           # 聊天链
        if self.step != 2:
            return "模型加载中请稍后!"
        
        handler = FxStdOutCallbackHandler()
        prompt = PromptTemplate(
            input_variables=["question"],
            template="你是一个说中文的智能客服，尽可能用中文回答问题。{question}",
        )
        chain = FxLLMChain(llm=self.llm, prompt=prompt)
        
        # Run the chain only specifying the input variable.
        result = chain.run(text, callbacks=[handler])
        print(result)
        return result
