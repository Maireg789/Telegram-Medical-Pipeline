import os
import json
import glob
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "medical_warehouse")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "10academy_password")

def connect_db():
    """Create a database connection engine."""
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)

def load_raw_data(base_path="data"):
    """Read JSON files and load them into PostgreSQL."""
    engine = connect_db()
    
    # 2. Create the 'raw' schema if it doesn't exist
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()
        print("✅ Schema 'raw' ensures.")

    # 3. Find all JSON files (recursively)
    # Pattern: data/raw/telegram_messages/YYYY-MM-DD/*.json
    json_pattern = os.path.join(base_path, "raw", "telegram_messages", "*", "*.json")
    files = glob.glob(json_pattern)
    
    if not files:
        print("⚠️ No JSON files found! Did you run the scraper?")
        return

    print(f"📦 Found {len(files)} JSON files to load.")

    all_messages = []

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # The scraper saves a list of dicts. Extend our master list.
            if isinstance(data, list):
                all_messages.extend(data)
    
    if not all_messages:
        print("⚠️ Files found, but they were empty.")
        return

    # 4. Convert to Pandas DataFrame
    df = pd.DataFrame(all_messages)
    
    # Basic cleaning to ensure it fits into DB
    # Rename columns to match standard SQL conventions if needed
    # The scraper uses: message_id, channel_name, message_date, message_text...
    
    print(f"📊 Loaded {len(df)} rows into DataFrame.")

    # 5. Write to PostgreSQL
    # if_exists='replace' means it will DROP the table and re-create it every time you run this.
    # This is good for development. For production, you'd use 'append'.
    try:
        df.to_sql(
            name='telegram_messages',
            con=engine,
            schema='raw',
            if_exists='replace', 
            index=False
        )
        print("✅ Success! Data loaded into table 'raw.telegram_messages'.")
    except Exception as e:
        print(f"❌ Error loading data to Postgres: {e}")

if __name__ == "__main__":
    load_raw_data()