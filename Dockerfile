FROM python:3.11-slim
WORKDIR /opt/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
ENV PORT 8080

CMD ["/bin/sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8080}"]
