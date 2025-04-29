# src/app/Dockerfile
FROM python:3.10-alpine

# 1) no build: atualiza repositórios e instala toolchain
RUN apk update && \
    apk add --no-cache rust cargo build-base

WORKDIR /usr/src/app

# 2) copia código e instala dependências Python
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# 3) entrypoint: roda o uvicorn
CMD ["uvicorn", "routers.app:app", "--host", "0.0.0.0", "--port", "8000"]
