EthioMed: AI-Enriched Medical Data Warehouse
Author: Maireg
Role: Data Engineer at Kara Solutions
Status: Final Submission (Completed Task 1–5)
📌 Project Overview
EthioMed is a production-grade data engineering pipeline that transforms unstructured data from Ethiopian medical Telegram channels into a structured, AI-enriched analytical warehouse.
By integrating Computer Vision (YOLOv8), dbt for dimensional modeling, and Dagster for orchestration, the platform provides actionable insights into medical product trends, promotional strategies, and channel activity across Ethiopia.
🏗️ Technical Architecture
The project follows a modern ELT (Extract, Load, Transform) architecture:
Ingestion (Extract): Telethon-based scrapers extract raw messages and images from channels like @CheMed123 and @tikvahpharma.
Enrichment (AI/CV): YOLOv8 processes images to categorize content into Product Display, Promotional, or Lifestyle categories.
Storage (Load): Raw data (JSON) and YOLO results (CSV) are loaded into a PostgreSQL Data Warehouse.
Transformation (Transform): dbt models raw data into a cleaned Star Schema.
Serving (API): FastAPI serves analytical endpoints for business reporting.
Orchestration: Dagster manages the entire end-to-end lineage and execution.
📂 Project Structure
Telegram-Medical-Pipeline/
├── api/                        # FastAPI Application
│   ├── main.py                 # API Endpoints
│   ├── database.py             # SQLAlchemy Connection
│   └── schemas.py              # Pydantic Models
├── data/                       # Local Data Lake (GitIgnored)
│   ├── raw/images/             # Scraped Media
│   └── yolo_results.csv        # Detection Metadata
├── medical_warehouse/          # dbt Project
│   ├── models/
│   │   ├── staging/            # Data Cleaning & Standardizing
│   │   └── marts/              # Fact & Dimension Tables
├── scripts/                    # Maintenance & Loading Scripts
│   └── load_yolo_to_db.py      # AI Metadata Database Loader
├── src/                        # Data Acquisition & Enrichment
│   ├── scraper.py              # Telegram Extraction
│   └── yolo_detect.py          # YOLOv8 Object Detection
├── pipeline.py                 # Dagster Orchestration Definition
├── docker-compose.yml          # PostgreSQL Orchestration
└── requirements.txt            # Project Dependencies
🚀 Installation & Setup
1. Prerequisites
Docker & Docker Compose
Python 3.10+
Telegram API Credentials (API ID & Hash)
2. Installation
code
Bash
git clone https://github.com/Maireg789/Telegram-Medical-Pipeline.git
cd Telegram-Medical-Pipeline
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
3. Environment Setup
Create a .env file in the root directory:
code
Ini
# Telegram API
TG_API_ID=your_id
TG_API_HASH=your_hash
PHONE_NUMBER=your_phone

# Database (PostgreSQL)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=medical_warehouse
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
⚙️ Running the Pipeline
Step 1: Start Database
code
Bash
docker compose up -d
Step 2: Automated Orchestration (Dagster)
The entire pipeline (Scraping -> YOLO -> Loading -> dbt) is orchestrated via Dagster.
code
Bash
dagster dev -f pipeline.py
Navigate to http://localhost:3000.
Click Lineage -> Materialize All to run the full workflow.
Step 3: Serve the API
Expose the data warehouse insights:
code
Bash
uvicorn api.main:app --reload
Access the interactive documentation at http://127.0.0.1:8000/docs.
📊 Data Insights & Enrichment
AI-Enrichment with YOLOv8
The pipeline utilizes a pre-trained YOLOv8 model to analyze image content.
Lifestyle: Images featuring people/lifestyle contexts.
Product Display: Close-ups of medical bottles, boxes, or equipment.
Promotional: Combined person and product images (influencer/sales style).
Analytical Endpoints
GET /api/reports/top-products: Most frequently mentioned terms.
GET /api/reports/visual-content: Summary of image classifications from YOLO.
GET /api/channels/{name}/activity: Daily message volume trends.
🛡️ Data Quality & Testing
Data integrity is maintained through dbt tests:
Unique/Not Null: Applied to message_id and channel_key.
Relationships: Ensures fct_messages correctly maps to dim_channels.
Custom Tests: Logic to ensure no future-dated messages or negative view counts.
📝 License
This project is part of the 10 Academy Data Engineering program. All data used is from public Telegram channels for educational purposes.
Author Maireg
January 20, 2026