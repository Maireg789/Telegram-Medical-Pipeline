import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# This points to the .env file in your root folder
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Match the names exactly from your screenshot
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')

# Construct the connection string
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

def load_yolo_results():
    csv_path = 'data/yolo_results.csv'
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found! Run 'python src/yolo_detect.py' first.")
        return

    # Load the CSV
    df = pd.read_csv(csv_path)
    
    # Push to Postgres (into the 'raw' schema)
    try:
        df.to_sql('yolo_results', engine, schema='raw', if_exists='replace', index=False)
        print("✅ YOLO results successfully loaded to table: raw.yolo_results")
    except Exception as e:
        print(f"❌ Error loading to database: {e}")

if __name__ == "__main__":
    load_yolo_results()