# 校验：http://localhost:9091/healthz
from milvus import MilvusServer

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
        self.server = MilvusServer()
        self.server.set_base_dir(self.local_data)
        self.server.listen_port = int(self.port)
        self.server.start()
        
    def stop(self):
        self.server.stop()