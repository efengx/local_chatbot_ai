# 初始化gptcache
# import langchain
import os
from typing import Dict, Any
from gptcache import Cache, Config
from gptcache.processor.pre import get_prompt
from gptcache.manager import CacheBase, VectorBase, get_data_manager
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
    list_data = data.get("prompt").split("-----")
    data = list_data[len(list_data)-1]
    print("需要向量比较的内容:", data)
    return data

class FxCache(object):
    
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance FxCache')
            cls._init(cls)
            
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance
    
    def _init(self):
        self.embed_model = Huggingface(model="BAAI/bge-small-zh-v1.5")                          # 对应的SearchDistanceEvaluation max_distance = 0.4
        print("FxCache embed model")
        self.cache_base = CacheBase('sqlite', 
                                    sql_url="sqlite:///./db/sqlite.db")
        print("FxCache sqlite")
        self.vector_base = VectorBase('milvus',                                               # 远程milvus服务器
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
        self.data_manager = get_data_manager(self.cache_base, self.vector_base)
        print("FxCache data_manager")
    
    def search(self):
        print(self.data_manager.s.count())
        print(self.data_manager.v)
        
        
    def fx_init_cache(self, cache_obj: Cache, llm_string: str):
        print("FxCache.fx_init_cache")
        # testText = "你是一个说中文的智能客服，尽可能用中文回答问题。酒店可以为客人预订迪士尼乐园门票吗？"
        
        # 参考：https://github.com/zilliztech/GPTCache/issues/478
        # embed_model = Huggingface(model='uer/albert-base-chinese-cluecorpussmall')      # 对应的SearchDistanceEvaluation max_distance = 2.4
        # embed_model = Huggingface(model="BAAI/bge-large-zh-v1.5")
        # embed_model = Huggingface(model="BAAI/bge-small-zh-v1.5")                       # 对应的SearchDistanceEvaluation max_distance = 0.4
        # embed = embed_model.to_embeddings(testText)
        # print(f"huggingface={embed}")

        # embed_model = Onnx()
        # embed = embed_model .to_embeddings(testText)
        # print(f"onnx={embed}")

        # cache_base = CacheBase('sqlite', sql_url="sqlite:///./db/sqlite.db")
        # vector_base = VectorBase('milvus', host='39.104.228.125', dimension=embed_model.dimension)
        
        # 当faiss不存在时。解决重复查询时，存在无法找到向量的问题
        # index_file_path="./db/index.faiss"
        # if not os.path.isfile(index_file_path):
        #     index = faiss.index_factory(embed_model.dimension, "IDMap,Flat", faiss.METRIC_L2)
        #     faiss.write_index(index, index_file_path)
        # vector_base = VectorBase('faiss', index_path=index_file_path, dimension=embed_model.dimension)
        # data_manager = get_data_manager(cache_base, vector_base)


        # searchDistanceEvaluation = SearchDistanceEvaluation()   
        # cache_obj.init(
        #     pre_embedding_func=get_prompt,                                                             # 从请求中提取关键信息并进行预处理，以确保编码器模块嵌入函数的输入信息简单且准确。
        #     embedding_func=embed_model.to_embeddings,                                                  # 生成文本的嵌入
        #     data_manager=data_manager,                                                                 # 管理缓存数据
        #     similarity_evaluation=searchDistanceEvaluation,                                            # 使用搜索距离来评估相似度
        # )

        init_similar_cache(                                                                              # 初始化缓存
            cache_obj=cache_obj,
            data_manager=self.data_manager,
            pre_func=get_prompt_split,                                                                         # 设置需要比较的问题 = pre_embedding_func
            embedding=self.embed_model,
            evaluation=SearchDistanceEvaluation(max_distance=0.4),
            # config=Config(data_check=True),
        )

    # 依赖倒置，将sqlalchemy转换成字典, 便于fastapi序列化
    @staticmethod
    def as_dict(obj):
       return {c.name: str(getattr(obj, c.name)) for c in obj.__table__.columns}
    
    def paginate(self, limit: int, offset: int):
        session = self.cache_base.Session()
        
        return [item._mapping for item in session.query(
                self.cache_base._answer.id, self.cache_base._answer.answer, self.cache_base._ques.question).filter(
                self.cache_base._answer.question_id == self.cache_base._ques.id).limit(limit).offset(offset)]