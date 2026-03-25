
# Olist ETL Pipeline

A Python-based ETL pipeline designed to process the Olist E-commerce dataset. This project handles data extraction, cleaning, and preparation for downstream analysis.

## Project Structure

- `data/raw/`: Original CSV files (Source of truth).
- `src/`: Python source code.
  - `extract.py`: Logic for dynamic data loading using `pathlib`.
  - `transform.py`: Data cleaning, type conversion, and deduplication.
- `output/`: Cleaned datasets exported as CSVs.
- `notebooks/`: Interactive data exploration and prototyping.

## Key Features

- **Dynamic Path Management**: Uses `pathlib` to ensure the project runs on any OS without hardcoded paths.
- **Robust Extraction**: Centralized loading mechanism that maps multiple CSVs into a single Python dictionary for easy access.
- **Data Cleaning**:
  - Converts date-related strings into proper `datetime` objects.
  - Filters records based on valid business statuses (delivered, shipped, etc.).
  - Removes duplicate entries based on `order_id`.
- **Validation**: Tracks null counts before and after transformation to monitor data integrity.

## Usage

1. Clone the repository.
2. Install dependencies:

   ```bash
   pip install pandas numpy
   ```


3. Run the pipeline:
   ```bash
   python src/extract.py
   ```


## Requirements

* Python 3.x
* Pandas
* Numpy
