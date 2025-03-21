FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install fastapi[all] elasticsearch
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9567"]
