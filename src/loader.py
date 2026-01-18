import os
import json
import glob
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 1. Load Environment Variables (but use hardcoded defaults as backup)
load_dotenv()

# FORCE defaults to match your hardcoded Docker setup
DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "medical_warehouse")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "10academy_password")

def connect_db():
    """Create a database connection engine."""
    # Print credentials to verify what Python is seeing
    print(f"🔌 Connecting to: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)

def load_raw_data(base_path="data"):
    """Read JSON files and load them into PostgreSQL."""
    
    # 2. Find JSON files
    json_pattern = os.path.join(base_path, "raw", "telegram_messages", "*", "*.json")
    files = glob.glob(json_pattern)
    
    if not files:
        print("⚠️ No JSON files found! Check your 'data/raw' folder.")
        return

    print(f"📦 Found {len(files)} JSON files. Processing...")

    all_messages = []
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_messages.extend(data)
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")

    if not all_messages:
        print("⚠️ Files found, but they were empty.")
        return

    # 3. Convert to DataFrame
    df = pd.DataFrame(all_messages)
    print(f"📊 Ready to load {len(df)} rows into Database...")

    # 4. Connect and Load
    try:
        engine = connect_db()
        
        # Create schema 'raw' if not exists
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
            conn.commit()

        # Load data to table
        df.to_sql(
            name='telegram_messages',
            con=engine,
            schema='raw',
            if_exists='replace', 
            index=False
        )
        print("✅ SUCCESS! Data loaded into 'raw.telegram_messages'.")
        
    except Exception as e:
        print("\n❌ CONNECTION ERROR:")
        print(e)
        print("\n💡 TIP: Ensure Docker is running via 'docker compose up -d'")

if __name__ == "__main__":
    load_raw_data()