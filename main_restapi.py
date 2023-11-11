# 参考：（GraphQL vs REST）https://aws.amazon.com/cn/compare/the-difference-between-graphql-and-rest/#:~:text=REST%20is%20good%20for%20simple,complex%2C%20and%20interrelated%20data%20sources.&text=REST%20has%20multiple%20endpoints%20in,has%20a%20single%20URL%20endpoint.
# feature:（完成）添加本地缓存机制
# feature:（完成）添加嵌入机制
# feature:（完成）vector embedding 的原理（需要支持中文嵌入）
# feature:（完成）抽象cache init操作, 并进行初始化处理
# feature:（完成）抽象prompt结构, 并进行自定义
# feature:（完成）抽象llmresult结构, 并进行自定义
# feature: 开发chat rag模型
# feature: 自定义data storage信息
import json
from src.chatbot.fx_chat import FxChat
from src.chatbot.fx_cache import fxCache
from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, Union, List, Annotated, Any

# input
class Item(BaseModel):
    # 默认知识库为: gptcache, 可以手动添加
    repository_name: str = Field(
        default="gptcache",
        description="集合名称只能包含数字、字母和下划线"
    )
    meta_data: str = "{\"temperature\": 0.7, \"n\": 1, \"organization\": \"\"}"
    load_model: str = "FxChatOpenAI"
    
    question: str = "酒店可以安排机场接送服务吗？"

class ItemPrompt(Item):
    prompt_system: str = "你是名迪城市酒店(尖沙咀)的在线客服。\n{question}"

class ItemRAG(Item):
    model_name: str = "gpt-4"

    prompt_system: str = """您好GPT，请扮演一个香港小型酒店客服并根据以下context去回答问题，如果context未涵盖问题，请根据你的知识库来回答问题,甚至是猜测，尽你最大可能去回答问题而不是回避问题。一定要注意这些事项：
不要暴露出自己是ai；
不要表示出你是根据context来回答问题的，如果context里面没有涉及到问题，就直接回答问题，不要回答信息不够或者没有提及；
不要让回答让客人打电话去询问，除非客人是直接询问电话号码；
可以基于常识的理解去回答；
你无法直接提供预定服务，而是解答问题，如果客人要预定，请让客人到‘天天住’微信小程序进行房间预定操作；
如果问题超出了客服范围，或者涉及政治，制度，人权等敏感信息，请回避该类问题；
用中文回答问题。

context为：
{context}"""
    
    documents: str = Field(
        default="""名迪城市酒店(尖沙咀) (Metacity Hotel (Tsim Sha Tsui)):
**酒店地址**：名迪城市酒店(尖沙咀) 位于中国香港香港香港尖沙咀这个地理位置便利，毗邻城市的主要景点和商业区域。
**房型：**名迪 - 標準雙人間,名迪 - 標準雙床房/雙人房,名迪 - 寬敞雙人間,名迪城市景觀 - 豪華家庭房,名迪城市景觀 - 豪華三人間,名迪城市豪华双人城景房,测试,钟点房测试宽敞而精致的名迪 - 標準雙人間配备现代化设施，为宾客提供一个温馨的栖息地，是商务旅行者和度假者的首选。
**酒店设施：**名迪城市酒店(尖沙咀) 通常提供婴儿床,洗衣服务,酒吧,可提供相连房,Wi-Fi上网(公共区域),停车场[附近],按摩,花园,家庭房,儿童游泳池,行李存放服务,电梯,出租车服务,儿童活动室,行李员,保姆(需预约),每日客房清洁服务,24小时前台,票务服务,可捞带宠物,按摩游泳池,酒店设停车场,洗衣机,餐厅,客房清洁服务(限定时周),旅游服务,地铁[附近],无障碍通道,干洗,水疗,游泳池,24小时送餐服务,健身中心,快速办理入住/退房,所有客房免费WiFi,无障碍设施,24小时办理入住,礼宾服务,健身中心(24 小时),送餐服务(有限时间),吸烟区,保险箱一系列豪华的设施，以确保客人在住宿期间享受到最大的舒适和便利。
如果您考虑入住我们名迪城市酒店，请拨打18600248705我们随时为您提供计划帮助。""", 
        title="这是RAG需要的文档"
    )
    
    prompt_human: str = """{question}"""
    
    # 为True时，使用缓存。为False时不使用缓存
    is_cache: bool = True


# 查询分页对象
class PaginatedRequest(BaseModel):
    limit: int = 10
    offset: int = 0

# output
class Message(BaseModel):
    message: str

# 声明返回的分页对象
class ChatRecord(BaseModel):
    id: int
    question: str
    answer: str
    
class PaginatedResponse(BaseModel):
    count: int = Field(description='Number of items returned in the response')
    items: List[ChatRecord]

app = FastAPI()


# /cache/


# /data/storage/list
# /data/storage/save
# /data/vector/list
async def common_parameters(
    limit: int = 10, offset: int = 0
):
    return {"limit": limit, "offset": offset}

# response_model=PaginatedResponse
@app.get("/data/storage/list", tags=["data"], 
         description="查询sqlite数据",
         response_model=PaginatedResponse)
async def data_storage_list(commons: Annotated[dict, Depends(common_parameters)]) -> Any:
    return PaginatedResponse(
        count=fxCache.data_manager.s.count(), 
        items=fxCache.paginate(limit=commons['limit'], offset=commons['offset']))

@app.get("/data/storage/save", tags=["data"], description="保存storage信息")
async def data_storage_save():
    return ""

# post /chat
# post /chat/chain
# post /chat/chain/rag

# 该方法需要重新推演模型
@app.post("/chat", tags=["chat"], description="聊天")
async def chat(item: Item):
    result = FxChat.getModel(item.load_model, model_name="gpt-4").predict(item.question)
    print(f"result={result}")
    return {"result": result}


@app.post("/chat/chain", tags=["chat"], description="链式聊天")
async def chat_chain(item: ItemPrompt):
    result = FxChat.getCache(isCache=item.is_cache).getModel(item.load_model, model_name="gpt-4").chainLlm(
        question=item.question, 
        prompt_system=item.prompt_system)
    return {"result": result}


@app.post("/chat/chain/rag", tags=["chat"], description="基于RAG的链式聊天")
async def chat_chain_rag(item: ItemRAG):
    print("chat_chain_rag item:", item)
    meta_data = json.loads(item.meta_data)
    print("chat_chain_rag meta_data:", meta_data)
    
    result = FxChat.getCache(isCache=item.is_cache).getModel(item.load_model, model_name=item.model_name, **meta_data).chainRagLlm(
        prompt_system=item.prompt_system,
        document=item.documents,
        prompt_human=item.prompt_human,
        question=item.question,
        repository_name=item.repository_name,
    )
    return {"result": result}


# openapi 基础文档结构
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="RjxAI Chat",
        version="0.0.1",
        summary="非常快的聊天",
        description="这是一个对于相似问题可以非常快响应的智能聊天ai。",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
