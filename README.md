# Olist E-Commerce ETL Pipeline 📊

This project implements a robust **ETL (Extract, Transform, Load)** pipeline to process and analyze the Olist E-commerce dataset from Brazil. The goal is to clean raw transactional data and prepare it for financial and operational insights.

## 🚀 Project Structure

- `data/raw/`: Contains the original, unmodified CSV datasets.
- `src/`: Core Python scripts for data processing.
  - `extract.py`: Automated loading of multiple datasets using dynamic paths.
  - `transform.py`: Data cleaning, datetime conversion, and duplicate removal logic.
- `output/`: Storage for cleaned, analysis-ready datasets.
- `logs/`: (Planned) Execution logs for monitoring pipeline health.

## 🛠️ Tech Stack

- **Python 3.x**
- **Pandas & Numpy**: For high-performance data manipulation.
- **Pathlib**: For platform-independent (Windows/Linux) path management.
