# 初始化gptcache
import langchain
import os
import json
from src.chatbot.fx_cache_gpt import FxGPTCache
from typing import Dict, Any
from gptcache import Cache, Config
from gptcache.processor.pre import get_prompt
from src.chatbot.cache.fx_manager import fx_get_data_manager
from gptcache.manager import CacheBase, VectorBase
from gptcache.similarity_evaluation.distance import SearchDistanceEvaluation
from gptcache.adapter.api import init_similar_cache
from gptcache.embedding import Huggingface
# from gptcache.embedding import onnx
# from sqlalchemy import create_engine, inspect, func, select

from dotenv import load_dotenv

load_dotenv()


def get_prompt_split(data: Dict[str, Any], **_: Dict[str, Any]) -> Any:
    """get the prompt of the llm request params

    :param data: the user llm request data
    :type data: Dict[str, Any]

    Example:
        .. code-block:: python

            from gptcache.processor.pre import get_prompt

            content = get_prompt({"prompt": "----- hello world ----- foo"})
            # " foo"
    """
    list_data = json.loads(data['prompt'])
    # list_data = data.get("prompt").split("-----")
    # data = list_data[len(list_data)-1]
    print("需要向量比较的内容:", list_data[1])
    print("提取回答问题的内容:", list_data[1]['kwargs']['content'])
    return list_data[1]['kwargs']['content']


class FxCache(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FxCache, cls).__new__(cls)
        return cls.instance

    def isCache(self):
        try:
            getattr(self, "embed_model")
            getattr(self, "cache_base")
            getattr(self, "vector_base")
            getattr(self, "data_manager")
            return True
        except AttributeError:
            print("cache 还未初始化，先初始化缓存")
            self.initCache()
            return False

    def initCache(self):
        # 对应的SearchDistanceEvaluation max_distance = 0.4
        self.embed_model = Huggingface(model="BAAI/bge-small-zh-v1.5")
        print("FxCache embed model")

        if not os.path.exists("./db"):
            os.makedirs("./db")
        self.cache_base = CacheBase('sqlite',
                                    sql_url="sqlite:///./db/sqlite.db")
        print("FxCache sqlite")
        self.vector_base = VectorBase('milvus',                                                  # 远程milvus服务器
                                      host=os.getenv('MILVUS_HOST'),
                                      dimension=self.embed_model.dimension)
        # self.vector_base = VectorBase('milvus',                                                 # 本地连接milvus服务器
        #                               host='localhost',
        #                               dimension=self.embed_model.dimension)
        # self.vector_base = VectorBase('milvus',                                               # 嵌入式milvus（需要抽象成数据微服务）
        #                               local_mode=True,
        #                               local_data="./db/milvus_data",
        #                               dimension=self.embed_model.dimension)
        print("FxCache load milvus")
        self.data_manager = fx_get_data_manager(self.cache_base, self.vector_base)
        print("FxCache data_manager")

    def getCache(self):
        if not self.isCache():
            print("初始化 langchain cache")
            langchain.llm_cache = FxGPTCache(self.fx_init_cache)
        elif langchain.llm_cache is None:
            print("重新初始化 langchain cache")
            langchain.llm_cache = FxGPTCache(self.fx_init_cache)
        return self

    def setCache(self, isCache: bool):
        if not isCache:
            print("不启用缓存")
            langchain.llm_cache = None
    
    def reBuildVectorBase(self, repository_name: str):
        if langchain.llm_cache is not None:
            self.data_manager.v.col.name
            print("准备更新知识库 name=", self.data_manager.v.col.name, repository_name)
            if repository_name == self.data_manager.v.col.name:
                return
            else:
                self.data_manager.v = VectorBase('milvus',                                                  # 远程milvus服务器
                                                host=os.getenv('MILVUS_HOST'),
                                                dimension=self.embed_model.dimension,
                                                collection_name=repository_name)
        else:
            print("开启了debug模式，跳过知识库逻辑。")

    def search(self):
        print(self.data_manager.s.count())
        print(self.data_manager.v)

    def fx_init_cache(self, cache_obj: Cache, llm_string: str):
        print("FxCache.fx_init_cache")

        init_similar_cache(                                                                              # 初始化缓存
            cache_obj=cache_obj,
            data_manager=self.data_manager,
            # 设置需要比较的问题 = pre_embedding_func
            pre_func=get_prompt_split,
            embedding=self.embed_model,
            evaluation=SearchDistanceEvaluation(max_distance=0.4),
            # config=Config(data_check=True),
        )

    # 依赖倒置，将sqlalchemy转换成字典, 便于fastapi序列化
    # @staticmethod
    # def as_dict(obj):
    #    return {c.name: str(getattr(obj, c.name)) for c in obj.__table__.columns}

    def paginate(self, limit: int, offset: int):
        session = self.cache_base.Session()
        return [item._mapping for item in session.query(
                self.cache_base._answer.id, self.cache_base._answer.answer, self.cache_base._ques.question).filter(
                self.cache_base._answer.question_id == self.cache_base._ques.id).limit(limit).offset(offset)]

# 单例模式
fxCache = FxCache().getCache()
