from fastapi import FastAPI
import uvicorn

app = FastAPI()


async def start_fastapi_server():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()
