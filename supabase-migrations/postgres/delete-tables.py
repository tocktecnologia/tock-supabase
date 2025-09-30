import os
import psycopg2
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()  # procura automaticamente um arquivo .env na raiz

# Pegue a connection string completa do .env, por exemplo:

DB_NAME= os.getenv("POSTGRES_DB")
POOLER_TENANT_ID= os.getenv("POOLER_TENANT_ID")
POSTGRES_PASSWORD= os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT= os.getenv("POSTGRES_PORT")
POSTGRES_HOST= "0.0.0.0" #os.getenv("POSTGRES_HOST")
POSTGRES_DB= os.getenv("POSTGRES_DB")
DATABASE_URL=f"postgres://{DB_NAME}.{POOLER_TENANT_ID}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


# Conecta ao PostgreSQL usando a URL completa
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

public_tables = ['app_configs','donors','accounts','credentials','employees','entities','invoices','root']

for table in public_tables:
  print(f"droping table  {table} ...")

  # cur.execute(f"DELETE  FROM public.{table}")
  cur.execute(f"DROP TABLE IF EXISTS public.{table} CASCADE;")
  conn.commit()

cur.execute("SELECT id, email FROM auth.users;")
rows = cur.fetchall()
for row in rows:
    user_id, email = row
    
    print(f"deleting ... UUID: {user_id} | Email: {email}")
    # Substitua pelo UUID do usuário que quer deletar
    user_uuid = user_id
    
    # Depois, deletar o usuário
    cur.execute("DELETE FROM auth.users WHERE id = %s;", (user_uuid,))

    conn.commit()

        
cur.close()
conn.close()


