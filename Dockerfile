FROM mhoush/psycopg2

WORKDIR /app

COPY . .

RUN cd ./app

CMD ["python3", "extract_and_load.py", "password", "password"]