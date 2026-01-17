# EthioMed: Telegram Medical Data Warehouse

**Author:** Maireg  
**Status:** Interim Submission (Tasks 1 & 2 Completed)  

## 📌 Project Overview
EthioMed is an end-to-end data engineering pipeline designed to extract, transform, and analyze real-time data from Ethiopian medical business channels on Telegram.

The goal is to answer key business questions regarding pharmaceutical trends, pricing, and channel activity by leveraging a modern **ELT (Extract, Load, Transform)** architecture.

## 🏗️ Architecture
The pipeline follows a Data Lakehouse approach:
1.  **Extract:** Python scripts (`Telethon`) scrape messages and images from public channels.
2.  **Load:** Raw data is stored in a local Data Lake (JSON) and loaded into **PostgreSQL**.
3.  **Transform:** **dbt** cleans and models the data into a Star Schema.
4.  **Enrich:** (In Progress) YOLOv8 performs object detection on product images.
5.  **Serve:** (In Progress) FastAPI exposes analytics to the frontend.
📂 Project Structure
Telegram-Medical-Pipeline/
├── data/                       # Data Lake (GitIgnored)
│   ├── raw/telegram_messages/  # JSON partitions
│   └── raw/images/             # Downloaded media
├── medical_warehouse/          # dbt Project
│   ├── models/
│   │   ├── staging/            # Cleaning views
│   │   └── marts/              # Star Schema (Dimensions & Facts)
├── src/                        # Source Code
│   ├── scraper.py              # Telegram Data Extraction
│   ├── loader.py               # JSON to Postgres Loader
│   └── datalake.py             # File system management
├── .env                        # API Keys & Secrets (GitIgnored)
├── docker-compose.yml          # Database Orchestration
├── requirements.txt            # Python Dependencies
🚀 Setup & Usage
1. Prerequisites
Docker Desktop
Python 3.10+
Git
2. Installation
code
Bash
# Clone the repository
git clone https://github.com/Maireg789/Telegram-Medical-Pipeline.git
cd Telegram-Medical-Pipeline

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
3. Environment Configuration
Create a .env file in the root directory:
code
Ini
TG_API_ID=your_telegram_api_id
TG_API_HASH=your_telegram_api_hash
PHONE_NUMBER=+251911234567
POSTGRES_USER=postgres
POSTGRES_PASSWORD=10academy_password
POSTGRES_DB=medical_warehouse
4. Running the Pipeline
Step 1: Start the Database
code
Bash
docker compose up -d
Step 2: Scrape Data
Extracts messages from channels like @CheMed123 and @tikvahpharma.
code
Bash
python -m src.scraper
Step 3: Load to Warehouse
Loads raw JSON files into the raw.telegram_messages table.
code
Bash
python src/loader.py
Step 4: Transform (dbt)
Builds the Star Schema and runs data quality tests.
code
Bash
cd medical_warehouse
dbt deps
dbt run
dbt test
📊 Data Quality
The pipeline implements strict quality checks using dbt:
Uniqueness: Ensures no duplicate messages in fct_messages.
NotNull: Enforces valid IDs and timestamps.
Referential Integrity: Validates links between Facts and Dimensions.
🔜 Next Steps
Implement YOLOv8 object detection pipeline.
Develop FastAPI endpoints for external access.
