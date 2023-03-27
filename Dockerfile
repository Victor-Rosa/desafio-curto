FROM mhoush/psycopg2

WORKDIR /app

COPY . .

CMD ["python", "extract_and_load.py"]