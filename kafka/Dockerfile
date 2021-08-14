FROM python:3.8-slim

RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
        netcat \
    && apt-get clean \
    && rm -rf -- /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --requirement requirements.txt

COPY src ./src
COPY start.sh ./start.sh

RUN chmod +x ./start.sh

ENTRYPOINT [ "/bin/bash" ]
