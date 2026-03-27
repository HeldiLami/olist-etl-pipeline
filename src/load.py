import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

OUTPUT_PATH = Path(__file__).parent.parent / "output"
LOGS_PATH = Path(__file__).parent.parent / "logs"

def save_clean_data(df: pd.DataFrame) -> None:
  """
  Saves final dataset in random formats
  """
  csv_path = OUTPUT_PATH / "olist_clean.csv"
  df.to_csv(csv_path, index=False)
  print(f"CSV: {csv_path}")

  summary = df.groupby("order_status").agg(
    total_orders = ("order_id", "nunique"),
    total_revenue = ("total_revenue", "sum"),
    avg_price = ("price", "mean"),
    avg_delivery = ("delivery_days", "mean")
  ).round(2)

  summary_path = OUTPUT_PATH / "summary_by_status.csv"
  df.to_csv(summary_path)
  print(f"Summary: {summary_path}")

def save_pipeline_report(
    df: pd.DataFrame,
    validation: pd.DataFrame,
    start_time: datetime
    ) -> None:
  """
  Creates a full report of the pipeline execution
  time it took; rows completed; controls done.
  """
  end_time= datetime.now()
  duration_sec = (end_time - start_time ).total_seconds()

  passed = (validation["status"] == "PASS").sum()
  failed = (validation["status"] == "FAIL").sum()
  total = len(validation)

  report ={
    "pipeline_run_date" : end_time.strftime("%Y-%m-%d %H:%M:%S"),
    "duration_seconds" : round(duration_sec,2),
    "rows_processed": len(df),
    "columns_produced" : df.shape[1],
    "validation_passed" : passed,
    "validation_failed" : failed,
    "validation_total" : total,
    "quality_score_pct" : round((passed/total) *100,1),
    "total_revenue": round(df['total_revenue'].sum(),2),
    "avg_delivery_days": round(df['delivery_days'].mean(),2),
    "late_orders_pct": round(df['is_late'].mean()*100,2)
  }

  report_df = pd.DataFrame([report])
  report_path = LOGS_PATH / "pipeline_runs.csv"

  if report_path.exists():
    existing = pd.read_csv(report_path)
    report_df = pd.concat([existing,report_df], ignore_index = True)

  report_df.to_csv(report_path, index=False)
  print(f"  Pipeline report: {report_path}")


def load_all(
    df: pd.DataFrame,
    validation: pd.DataFrame,
    datetime: datetime
) -> None:
    """
    Executes all save functs
    """

    print("=" * 50)
    print("LOAD — Exporting results...")
    print("=" * 50)

    save_clean_data(df)
    save_pipeline_report(df,validation,datetime)
    print("LOAD completed")

if __name__ == "__main__":
   from extract import extract_all
   from transform import transform_all
   from validate  import run_validation
   
   start = datetime.now()

   datasets = extract_all()
   df = transform_all(datasets)
   validation = run_validation(df)
   load_all(df,validation,start)

