from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_redis


def make_mock_redis(hit_count=1):
    mock = MagicMock()
    mock.incr.return_value = hit_count
    return mock


def make_mock_etcd():
    mock = MagicMock()
    mock.get.return_value = (b'localhost:8000', None)
    return mock


def test_read_root():
    mock_redis = make_mock_redis(hit_count=42)
    # mock_etcd = make_mock_etcd()

    app.dependency_overrides[get_redis] = lambda: mock_redis
    # app.dependency_overrides[get_etcd] = lambda: mock_etcd

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Hello": "w 42"}
    mock_redis.incr.assert_called_once_with('hits')
    # mock_etcd.get.assert_called_once_with('/services/myserver')

    app.dependency_overrides.clear()


def test_read_item():
    client = TestClient(app)
    response = client.get("/items/5?q=hello")

    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "q": "hello"}


def test_read_item_no_query():
    client = TestClient(app)
    response = client.get("/items/3")

    assert response.status_code == 200
    assert response.json() == {"item_id": 3, "q": None}


def test_websocket_echo():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        ws.send_text("hello")
        data = ws.receive_text()
        assert data == "Message text was: hello"


def test_websocket_multiple_messages():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        for msg in ["first", "second", "third"]:
            ws.send_text(msg)
            data = ws.receive_text()
            assert data == f"Message text was: {msg}"
