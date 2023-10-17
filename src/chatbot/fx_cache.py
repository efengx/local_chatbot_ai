# 初始化gptcache
from gptcache import Cache
from gptcache.processor.pre import get_prompt
from gptcache.manager import CacheBase, VectorBase, get_data_manager
from gptcache.similarity_evaluation.distance import SearchDistanceEvaluation
from gptcache.adapter.api import init_similar_cache

def init_gptcache(cache_obj: Cache, llm_string: str):
    # testText = "你是一个说中文的智能客服，尽可能用中文回答问题。酒店可以为客人预订迪士尼乐园门票吗？"
    from gptcache.embedding import Huggingface
    # 参考：https://github.com/zilliztech/GPTCache/issues/478
    # embed_model = Huggingface(model='uer/albert-base-chinese-cluecorpussmall')    # 对应的SearchDistanceEvaluation max_distance = 2.4
    # embed_model = Huggingface(model="BAAI/bge-large-zh-v1.5")
    embed_model = Huggingface(model="BAAI/bge-small-zh-v1.5")                       # 对应的SearchDistanceEvaluation max_distance = 0.4
    # embed = embed_model.to_embeddings(testText)
    # print(f"huggingface={embed}")

    # from gptcache.embedding import Onnx
    # embed_model = Onnx()
    # embed = embed_model .to_embeddings(testText)
    # print(f"onnx={embed}")

    cache_base = CacheBase('sqlite', sql_url="sqlite:///./db/sqlite.db")
    # vector_base = VectorBase('milvus', host='39.104.228.125', dimension=embed_model.dimension)
    vector_base = VectorBase('faiss', index_path="./db/faiss.index", dimension=embed_model.dimension)
    data_manager = get_data_manager(cache_base, vector_base)
    
    print(f"data_manager sqlite count: {data_manager.s.count()}")
    print(f"data_manager milvus: {data_manager.v}")
    
    # searchDistanceEvaluation = SearchDistanceEvaluation()   
    # cache_obj.init(
    #     pre_embedding_func=get_prompt,                                                             # 从请求中提取关键信息并进行预处理，以确保编码器模块嵌入函数的输入信息简单且准确。
    #     embedding_func=embed_model.to_embeddings,                                                  # 生成文本的嵌入
    #     data_manager=data_manager,                                                                 # 管理缓存数据
    #     similarity_evaluation=searchDistanceEvaluation,                                            # 使用搜索距离来评估相似度
    # )

    init_similar_cache(                                                                              # 初始化缓存
        cache_obj=cache_obj,
        data_manager=data_manager,
        embedding=embed_model,
        evaluation=SearchDistanceEvaluation(max_distance=0.4)
    )
