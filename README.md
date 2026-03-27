# Olist E-Commerce ETL Pipeline

A production-style ETL pipeline that processes 100k+ Brazilian e-commerce
records through automated extraction, cleaning, validation, and reporting
stages — built with Python, Pandas, and NumPy.

---

## Architecture

```
data/raw/          →    extract.py    →    transform.py
(4 CSV files)           (load & check)     (clean & merge)
                                                ↓
logs/pipeline_runs.csv  ←   load.py   ←   validate.py
output/olist_clean.csv      (export)       (12 quality checks)
```

**Each module has a single responsibility:**

- `extract.py` — reads raw CSVs, fails fast if files are missing
- `transform.py` — applies cleaning rules and business logic
- `validate.py` — runs 3-layer data quality framework
- `load.py` — exports results and maintains pipeline run history

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/HeldiLami/olist-etl-pipeline.git
cd olist-etl-pipeline

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add raw data
# Download from: kaggle.com/datasets/olistbr/brazilian-ecommerce
# Place all CSV files in data/raw/

# 5. Run the full pipeline
python main.py
```

---

## Key Findings

After processing **111,715 records** across **99,441 orders**:

| Metric                  | Value               |
| ----------------------- | ------------------- |
| Total revenue processed | $15,805,788         |
| Average delivery time   | 12.1 days           |
| Late delivery rate      | 7.3%                |
| Data quality score      | 10/11 checks passed |
| Price outliers detected | 7.5% of products    |

**Price distribution:**

- 53% of products fall in the mid tier ($50–$200)
- Only 3% reach luxury pricing (>$500)

![Price Distribution](images/price_distribution.png)

---

## Data Quality Framework

Validation runs automatically after every transform and covers three layers:

- **Completeness** — critical columns checked for null thresholds
- **Consistency** — business rules enforced (no negative prices,
  no delivery before purchase date)
- **Distribution** — statistical outlier detection using IQR method

Every run is logged to `logs/pipeline_runs.csv` with timestamp,
duration, rows processed, and quality score — providing full audit
trail across executions.

---

## Tech Stack

| Tool        | Purpose                                            |
| ----------- | -------------------------------------------------- |
| Python 3.11 | Core language                                      |
| Pandas      | Data manipulation and ETL logic                    |
| NumPy       | Statistical computations and vectorized operations |
| Pathlib     | Cross-platform file handling                       |
| Jupyter     | Exploratory data analysis                          |

---

## Project Structure

```
olist-etl-pipeline/
├── data/raw/              ← source CSV files (not tracked in git)
├── notebooks/
│   └── exploration.ipynb  ← EDA and pre-transform experiments
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   └── load.py
├── output/                ← cleaned data and summary reports
├── logs/                  ← validation reports and run history
├── main.py
├── requirements.txt
└── README.md
```
