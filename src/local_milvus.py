# 校验：http://localhost:9091/healthz
from milvus import MilvusServer
from milvus import default_server
from milvus import debug_server

class LocalMilvus:
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
        self.local_data="./db/milvus_data"
        self.port="19530"
    
    def start(self):
        # 开启默认模式
        default_server.set_base_dir('./db/milvus_data')
        default_server.start()
        print("start finish!")
        # 开启debug模式
        # debug_server.set_base_dir('./db/milvus_data')                       # 设置数据和日志的存储路径
        # debug_server.start()
        
    def stop(self):
        default_server.stop()
        
        # debug_server.stop()
        
