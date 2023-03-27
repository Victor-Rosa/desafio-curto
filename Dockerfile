FROM python:3.9-slim

WORKDIR /app

COPY requeriments.txt .

RUN pip install -r requeriments.txt

COPY . .

CMD ["python", "extract_and_load.py"]