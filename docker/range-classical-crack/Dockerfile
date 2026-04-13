FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY config.yaml .
COPY templates ./templates

EXPOSE 8083

CMD ["python", "app.py"]