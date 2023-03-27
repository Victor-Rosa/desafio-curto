import psycopg2
import os

# Funçao para concectar o banco de dados Postgress
def connect_db(hostname, name_db, user, password, port):
    try:
        conn = psycopg2.connect(
            host=str(hostname),
            database=str(name_db),
            user=str(user),
            password=str(password),
            port=int(port)
        )
        return conn
    except psycopg2.Error as e:
        print("Error ao se conectar com o Banco de Dados", e)


# Conexão com o banco de dados de Transacional (OLTP) - Origem
db_transactional_conn = connect_db(
    "localhost", "dvdrental", "postgres", "password", 5432)

# Conexão com o banco de dados de Análise (OLAP) - Destino
db_analytics_conn = connect_db(
    "localhost", "analytics", "postgres", "password", 5440)

# Fazendo o dump do banco de dados Transacional
dump_file = "data/dump.sql"
dump_command = f'pg_dump -U postgres -h localhost dvdrental > {dump_file}'
os.system(dump_command)

# Copiando o dump do banco de dados Transacional para o banco Analítico
copy_dump_command = 'psql -U postgres -h localhost -p 5440 -d analytics -f data/dump.sql'
os.system(copy_dump_command)


# Encerrando as Conexões
db_transactional_conn.close()
db_analytics_conn.close()
