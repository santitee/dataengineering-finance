# Supercell Data Engineering: Financial Pipeline

This repository contains a demo data pipeline for financial month-end closing, 
designed based on Supercell's data domain requirements.

## 📈 Key Features
- **Multi-Frequency Processing:** Supporting NRT (30m), Daily, and Monthly closing.
- **Revenue Recognition:** Automated calculation of Deferred vs Recognized revenue.
- **Signal-Based Architecture:** Ensuring data integrity by checking upstream signals before batch runs.
- **Whale Analysis:** Identifying top spending users for LTV insights.

## 🛠 Tech Stack
- **Language:** Python / PySpark
- **Concepts:** ETL, FX Conversion, Idempotency, Data Validation.

## 🚀 Execution
```bash
python src/pipeline.py nrt     # For Near Real-Time monitoring
python src/pipeline.py daily   # For Daily revenue summary
python src/pipeline.py monthly # For Month-end financial closing

install

`python3 -m venv venv`

source venv/bin/activate
pip install -r requirements.txt