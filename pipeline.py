import subprocess
import os
import sys
from dagster import asset, Definitions

# Get absolute path to project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@asset
def telegram_data():
    """Task 1: Scrape Telegram Data from src/scraper.py"""
    script_path = os.path.join(BASE_DIR, "src", "scraper.py")
    subprocess.run([sys.executable, script_path], check=True)

@asset(deps=[telegram_data])
def yolo_enrichment():
    """Task 3: Run YOLOv8 Detection from src/yolo_detect.py"""
    script_path = os.path.join(BASE_DIR, "src", "yolo_detect.py")
    subprocess.run([sys.executable, script_path], check=True)

@asset(deps=[yolo_enrichment])
def load_to_postgres():
    """Task 3: Load YOLO CSV to DB from scripts/load_yolo_to_db.py"""
    script_path = os.path.join(BASE_DIR, "scripts", "load_yolo_to_db.py")
    subprocess.run([sys.executable, script_path], check=True)

@asset(deps=[load_to_postgres])
def dbt_transformations():
    """Task 2 & 3: Run dbt models in medical_warehouse folder"""
    dbt_dir = os.path.join(BASE_DIR, "medical_warehouse")
    subprocess.run(["dbt", "run", "--project-dir", dbt_dir], check=True)

defs = Definitions(
    assets=[
        telegram_data, 
        yolo_enrichment, 
        load_to_postgres, 
        dbt_transformations
    ]
)