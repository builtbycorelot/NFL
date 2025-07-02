FROM python:3.11-slim
WORKDIR /opt/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
ENV PORT 8080

CMD ["/bin/sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-8080} app:app"]
