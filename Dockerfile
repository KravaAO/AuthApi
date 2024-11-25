FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN mkdir -p /app/instance

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
