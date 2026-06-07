Flight Operations Analytics Data Pipeline
This project is an end-to-end data engineering pipeline that automates the ingestion, transformation, and analysis of live global flight data using Apache Airflow and the Medallion Architecture.

🚀 Project Overview
Designed to simulate real-world aviation analytics, this pipeline pulls live data from the OpenSky Network API, processes it through Bronze, Silver, and Gold layers, and delivers analytics-ready data for business intelligence.

Ingestion: Pulls real-time flight data every 30 minutes.
Architecture: Implements a Medallion structure (Bronze → Silver → Gold) for clean data lifecycle management.
Orchestration: Built using Apache Airflow for scheduling, dependency management, and error handling.
Storage & Delivery: Supports both local CSV storage and automated ingestion into Snowflake for advanced BI dashboards.
🛠 Tech Stack
Orchestration: Apache Airflow
Data Processing: Python (Pandas)
Data Source: OpenSky Network API
Environment: Docker & Docker Compose
Warehouse (Optional): Snowflake
