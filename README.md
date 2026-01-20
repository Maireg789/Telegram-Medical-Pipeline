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

*   **Ingestion (Extract):** Telethon-based scrapers extract raw messages and images.
*   **Enrichment (AI/CV):** **YOLOv8** processes images to categorize content.
*   **Storage (Load):** Raw data (JSON) and YOLO results (CSV) are loaded into **PostgreSQL**.
*   **Transformation (Transform):** **dbt** models raw data into a cleaned **Star Schema** with quality tests.
*   **Serving (API):** **FastAPI** serves analytical endpoints for business reporting.
*   **Orchestration:** **Dagster** manages lineage, daily scheduling, and automated testing.

---

## 📂 Project Structure
```text
Telegram-Medical-Pipeline/
├── api/                        # FastAPI Application
├── data/                       # Local Data Lake (GitIgnored)
├── medical_warehouse/          # dbt Project
├── scripts/                    # Maintenance & Loading Scripts
├── src/                        # Data Acquisition & Enrichment
├── pipeline.py                 # Dagster Orchestration & Scheduling
├── docker-compose.yml          # PostgreSQL Orchestration
└── requirements.txt            # Project Dependencies

⚙️ Running the Pipeline

1. Automated Orchestration (Dagster)
The entire pipeline is orchestrated via Dagster.
code
Bash
dagster dev -f pipeline.py
Hardening: Includes an automated Daily Schedule and integrated dbt tests.

2. Serve the API
Expose the data warehouse insights:
code
Bash
uvicorn api.main:app --reload
Interactive Documentation: http://127.0.0.1:8000/docs

🛡️ Production Hardening (Final Deliverables)

Automated Scheduling: Configured Dagster schedules for daily data refreshes.
Integrated Testing: Automated dbt test execution within the pipeline.
Analytical API: 4 endpoints providing real-time warehouse insights.
Author Maireg
January 20, 2026