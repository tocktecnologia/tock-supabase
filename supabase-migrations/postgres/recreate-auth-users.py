import os
import csv

from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Replace with your Supabase self-hosted URL and service_role key
SUPABASE_URL = os.getenv("API_EXTERNAL_URL")
SERVICE_ROLE_KEY = os.getenv("SERVICE_ROLE_KEY")
FOLDER_TABLES="./tables"

try:
    supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
    supabase = create_client(
        SUPABASE_URL,
        SERVICE_ROLE_KEY,
        options=ClientOptions(
            auto_refresh_token=False,
            persist_session=False,
        )
    )
    auth = supabase.auth.admin
    
    table_name = 'users'
    path_csv_file = Path(f"{FOLDER_TABLES}/{table_name}_rows.csv")
    print(f"\nExecuting for table {path_csv_file}:")
    response={}  
    with open(path_csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)  # reads rows as dictionaries
        for row in reader:
            password=row['email'].split('@')[0]+'123'
            
            print(f"Creating user {row['email']} ...")
            user_json =   {
                    "email": row['email'],
                    "password": password,
                    "user_metadata":{'email_verified': True},
                    "app_metadata":{'provider': 'email', 'providers': ['email']},
                    "id":row['id'],
                    "email_confirm": True
                }
            # print(f"user json:{user_json} ")
            response = auth.create_user(user_json)
    print(f"response:{response}")
except Exception as e:
    print("Connection failed:", e)
