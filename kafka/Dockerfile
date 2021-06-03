FROM python:3.8-slim

COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

COPY src ./src

ENTRYPOINT [ "python3" ]
