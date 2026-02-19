FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY iot_device_management /app

WORKDIR /app

CMD ["gunicorn", "iot_device_management.wsgi:application", "--bind", "0.0.0.0:8000"]