from fastapi import FastAPI
import uvicorn
from API.groupone.doc import doc
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，不推荐在生产中使用
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，不推荐在生产中使用
    allow_headers=["*"],  # 允许所有头部，不推荐在生产中使用
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(doc,prefix="/doc",tags=["doc相关接口"])

if __name__ == "__main__":
    uvicorn.run(app, host="10.2.3.117", port=8000)

