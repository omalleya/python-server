import httpx
import websockets
import pytest

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws"


@pytest.fixture
def client():
    return httpx.Client(base_url=BASE_URL)


def test_root_returns_hit_count(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "Hello" in body
    assert body["Hello"].startswith("w ")


def test_root_increments_count(client):
    r1 = client.get("/")
    r2 = client.get("/")
    count1 = int(r1.json()["Hello"].split(" ")[1])
    count2 = int(r2.json()["Hello"].split(" ")[1])
    assert count2 > count1


def test_items_endpoint(client):
    response = client.get("/items/10?q=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": 10, "q": "test"}


@pytest.mark.asyncio
async def test_websocket_echo():
    async with websockets.connect(WS_URL) as ws:
        await ws.send("integration test")
        response = await ws.recv()
        assert response == "Message text was: integration test"
