import psycopg2

postgres_db = "user=postgres password=twister00"
db_name = 'anton_question'

conn = psycopg2.connect(postgres_db)
cur = conn.cursor()

cur.execute('CREATE DATABASE ' + db_name)
