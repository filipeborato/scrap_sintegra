# src/worker/Dockerfile
FROM python:3.14.0a1-alpine3.20

# instala supervisor só no build
RUN apk update && \
    apk add --no-cache supervisor

WORKDIR /usr/src/app

# copia fonte e config do supervisor
COPY . .
COPY supervisor/sintegra_goias.conf /etc/supervisor/conf.d/

# instala deps Python
RUN pip install --no-cache-dir -r requirements.txt

# entrypoint: supervisor no foreground
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/sintegra_goias.conf"]
