# src/worker/Dockerfile
FROM python:3.14.0a1-alpine3.20

ENV PYTHONPATH=/usr/src/app
WORKDIR /usr/src/app

# 1) Dependências
COPY requirements.txt .
RUN apk add --no-cache supervisor \
 && pip install --no-cache-dir -r requirements.txt \
 && mkdir -p /var/log/supervisor

# 2) Copia o sintegra_goias e, em seguida, extrai o controllers
COPY sintegra_goias          ./sintegra_goias
COPY sintegra_goias/controllers ./controllers   

# 3) Se você tiver config local
COPY config                  ./config

# 4) Supervisor
COPY supervisor/sintegra_goias.conf \
     /etc/supervisor/conf.d/sintegra_goias.conf

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/sintegra_goias.conf"]

