from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
import redis
# import etcd3
import time
import os
from lib.test import TestClass

app = FastAPI()


def get_redis():
    return redis.Redis(host='redis', port=6379)


# def get_etcd():
#     return etcd3.client(
#         host=os.environ.get('ETCD_HOST', 'localhost'),
#         port=int(os.environ.get('ETCD_PORT', 2379)),
#     )


# @app.on_event("startup")
# def register_service():
#     client = get_etcd()
#     lease = client.lease(ttl=10000000)
#     client.put('/services/myserver', 'localhost:8000', lease)


def get_hit_count(cache):
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.get("/")
def read_root(cache=Depends(get_redis), ):
    count = get_hit_count(cache)
    testClass = TestClass()
    testClass.test_function()
    return {"Hello": f"w {count}"}


@app.websocket('/ws')
async def chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
