from python:3.14-alpine
workdir /app
copy requirements.txt requirements.txt
run pip install -r requirements.txt
expose 8000
copy . .
cmd ["fastapi", "run", "main.py", "--host", "0.0.0.0"]
