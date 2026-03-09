# Basic python server using fastapi

Server can be run with: `docker compose up --build`

## Tests

Unit tests (no Docker required):
```
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python python -m pytest tests/test_unit.py -v
```

Integration tests (requires `docker compose up`):
```
python -m pytest tests/test_integration.py -v
```
