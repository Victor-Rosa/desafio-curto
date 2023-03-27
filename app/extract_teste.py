import psycopg2

def truncate_string(string, max_length):
    if len(string) > max_length:
        return string[:max_length]
    else:
        return string


# Conexão com o banco de dados de Transacional (OLTP) - Origem
db_transactional_conn = psycopg2.connect(
    host="localhost",
    database="dvdrental",
    user="postgres",
    password="password", 
    port= 5432)

# Conexão com o banco de dados de Análise (OLAP) - Destino
db_analytics_conn = psycopg2.connect(
    host="localhost",
    database="analytics",
    user="postgres",
    password="password",
    port=5440)

transactional_cur = db_transactional_conn.cursor()
analytics_cur = db_analytics_conn.cursor()

transactional_cur.execute(
    "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ")
transactional_tables = transactional_cur.fetchall()

for table in transactional_tables:
    table_name = table[0]
    transactional_cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name=\'{table_name}\'")
    columns = transactional_cur.fetchall()
    columns_definitions = [f"{col[0].replace(' ', '_')} {col[1].replace('USER-DEFINED', 'varchar')}" for col in columns]
    analytics_cur.execute(f"CREATE TABLE {table_name} ({', '.join(columns_definitions)})")
    transactional_cur.execute(f"SELECT * FROM {table_name}")
    rows = transactional_cur.fetchall()
    column_lengths = []    
    for column in columns:
      transactional_cur.execute(f"SELECT CHARACTER_MAXIMUM_LENGTH FROM information_schema.columns WHERE table_name = '{table_name}' AND column_name = '{column[0]}'")
      length = transactional_cur.fetchone()[0]
      column_lengths.append(length)

    for row in rows:
        truncated_row = [truncate_string(cell, n) for cell, n in zip(row, column_lengths)]
        placeholder = ", ".join(['%s'] * len(row))
        print(row)
        analytics_cur.execute(
            f"INSERT INTO {table_name} VALUES ({placeholder})", row)


# Confirmando as alterações
analytics_cur.commit()

# Encerrando as Conexões
db_transactional_conn.close()
transactional_cur.close()
db_analytics_conn.close()
analytics_cur.close()
