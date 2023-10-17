# 参考：（GraphQL vs REST）https://aws.amazon.com/cn/compare/the-difference-between-graphql-and-rest/#:~:text=REST%20is%20good%20for%20simple,complex%2C%20and%20interrelated%20data%20sources.&text=REST%20has%20multiple%20endpoints%20in,has%20a%20single%20URL%20endpoint.
# feature:（完成）添加本地缓存机制
# feature:（完成）添加嵌入机制
# feature: vector embedding 的原理（需要支持中文嵌入）
# feature: 抽象cache init操作, 并进行初始化处理
# feature: 抽象prompt结构, 并进行自定义
# feature: 抽象llmresult结构, 并进行自定义
from src.chatbot.fx_chat import FxChat
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

fxChat = FxChat()


class Item(BaseModel):
    question: str


app = FastAPI()


@app.post("/predict/",  description="根据问题预测回答")
async def predict(item: Item):
    result = fxChat.predict(item.question)
    print(f"result={result}")
    return {"message": result}

@app.post("/chainllm/",  description="问答链")
async def chainllm(item: Item):
    result = fxChat.chainllm(item.question)
    return {"message": result}

@app.get("/cache/preloading", description="预先载入缓存")
async def cachePreloading():
    for data in open("input/hotelquestions.txt", "r"):
        print(data)
    return {"message": ""}


# openapi 元数据
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
