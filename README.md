# EthioMed: AI-Enriched Medical Data Warehouse

**Author:** Maireg  
**Role:** Data Engineer at Kara Solutions  
**Status:** Final Submission (Completed Task 1–5)

---

## 📌 Project Overview
EthioMed is a production-ready data engineering pipeline that transforms unstructured data from Ethiopian medical Telegram channels into a structured, AI-enriched analytical warehouse. 

By integrating **Computer Vision (YOLOv8)**, **dbt for dimensional modeling**, and **Dagster for orchestration**, the platform provides actionable insights into medical product trends, promotional strategies, and channel activity across Ethiopia.

---

## 🏗️ Technical Architecture
The project follows a modern **ELT (Extract, Load, Transform)** architecture:

*   **Ingestion (Extract):** Telethon-based scrapers extract raw messages and images from channels like `@CheMed123` and `@tikvahpharma`.
*   **Enrichment (AI/CV):** **YOLOv8** processes images to categorize content into *Product Display*, *Promotional*, or *Lifestyle*.
*   **Storage (Load):** Raw data (JSON) and YOLO results (CSV) are loaded into a **PostgreSQL** Data Warehouse.
*   **Transformation (Transform):** **dbt** models raw data into a cleaned **Star Schema** with robust data quality tests.
*   **Serving (API):** **FastAPI** serves analytical endpoints for business reporting.
*   **Orchestration:** **Dagster** manages the end-to-end lineage, scheduling, and error handling.

---

## 📂 Project Structure
```text
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
├── pipeline.py                 # Dagster Orchestration & Scheduling
├── docker-compose.yml          # PostgreSQL Orchestration
└── requirements.txt            # Project Dependencies
⚙️ Running the Pipeline
1. Start Database
code
Bash
docker compose up -d

2. Automated Orchestration (Dagster)
The entire pipeline is orchestrated via Dagster.
code
Bash
dagster dev -f pipeline.py
Access the UI at http://localhost:3000.
Hardening: The pipeline includes an automated Daily Schedule (midnight) and integrated dbt tests to ensure data quality.

3. Serve the API
Expose the data warehouse insights:
code
Bash
uvicorn api.main:app --reload
Interactive Documentation: http://127.0.0.1:8000/docs

📊 AI Enrichment & API Analytics
The pipeline utilizes YOLOv8 to analyze image content, providing the following insights via the API:
Lifestyle Detection: Identifies brand-building lifestyle posts.
Product Display: Tracks how often raw products are showcased.
Promotional: Identifies high-value sales content featuring people and products.
Analytical Endpoints:
GET /api/reports/top-products
GET /api/reports/visual-content
GET /api/channels/{name}/activity

🛡️ Production Hardening
To move beyond a prototype, the following features were implemented:
Automated Scheduling: Configured Dagster schedules for daily data refreshes.
Integrated Testing: Automated dbt test execution within the pipeline to prevent data regression.
CI/CD Foundation: Organized project structure for automated deployment.
Author Maireg
January 20, 2026