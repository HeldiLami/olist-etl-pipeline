import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

LOGS_PATH = Path(__file__).parent.parent / "logs"
LOGS_PATH.mkdir(exist_ok =True)


def _make_result(check_name:str, passed:bool, detail:str):
  """
  Each control returns a same format dictionary, so it is easier to make logs.

  """
  return {
    "check": check_name,
    "status": "pass" if passed else "fail",
    "detail": detail,
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  }

def check_completeness(df: pd.DataFrame) -> list[dict]:
  """
  Checks if critical columns are not empty at a certain threshold
  """
  results = []

  critical_columns = {
    "order_id": 0.0,
    "customer_id": 0.0,
    "order_purchase_timestamp":  0.0,
    "price": 0.0,   
    "order_status": 0.5,   
    "delivery_days": 15.0,
  }

  for col, max_null_pct in critical_columns.items():
    if col not in df.columns: 
      results.append(_make_result(
        f"completeness_{col}",
        False,
        f"Kolona '{col} nuk ekziston fare"
      ))
      continue
    null_pct = df[col ].isnull().mean() * 100
    passed   = null_pct <= max_null_pct
        
    results.append(_make_result(
      f"completeness_{col}",
      passed,
      f"{null_pct:.2f}% null (max i lejuar: {max_null_pct}%)"
    ))
    
  return results


def check_consistency(df: pd.DataFrame) -> list[dict]:
  """
  Checks if values have a logical sense
  """

  results = []

  negative_prices = (df['price'] < 0).sum()
  results.append(_make_result(
    "consistency_prices",
    negative_prices == 0,
    f"{negative_prices:,} çmime negative"
    ))
  
  if "delivery_days" in df.columns:
    impossible_delivery = (df['delivery_days']<0).sum()
    results.append(_make_result(
      "consistency_delivery_dates",
      impossible_delivery == 0,
      f"{impossible_delivery:,} delivery before purchase — impossible"
  ))
    
  duplicate_orders = df.duplicated(subset=['order_id']).sum()
  results.append(_make_result(
    "consistency_uniqe_orders",
    duplicate_orders == 0,
    f"{duplicate_orders:,} order_id të duplifikuara"
  ))

  if "total_payments" in df.columns:
    discrepancy = np.abs(
      df["total_payment"] - df["tota_revenue"]
    )
    large_discrepancy = (discrepancy>1).mean() * 100
    results.append(_make_result(
      "consistency_payment_vs_revenue",
      large_discrepancy <5.0, #if less than 5% of the orders have a discrepancy of 1% test is PASSED
      f"{large_discrepancy:.1f}% porosive kanë diferencë pagese > $1"
    ))

  return results

def check_distribution(df: pd.DataFrame)-> list[dict]:
  """
  Checks if the statistics are inside the norm, using mostly numpy.
  
  """
  results = []
  prices = df['price'].dropna().values #so we can use the np functions

  q1 = np.percentile(prices, 25)
  q3 = np.percentile(prices,75)

  iqr = q3 - q1
  lower_bound = q1 - 1.5*iqr
  upper_bound = q3 + 1.5*iqr

  outliers = np.sum((prices <lower_bound) | (prices > upper_bound))
  outlier_pct = (outliers/len(prices)) * 100

  results.append(_make_result(
    "distribution_price_outliers",
    outlier_pct < 10.0,
    f"{outlier_pct:.1f}% outliers (Q1={q1:.2f}, Q3={q3:.2f}, IQR={iqr:.2f})"
  ))

#average days to deliver
  if "deliver_days" in df.columns: 
    delivery = df['delivery_days'].dropna().values
    mean_days = np.mean(delivery)
    median_days = np.median(delivery)
    std_days = np.std(delivery)

    results.append(_make_result(
      "distribution_delivery_days",
      1 <= mean_days <= 60,
      f"mean: {mean_days:.1f} days, median:{median_days:.1f} days, std: {std_days:.1f} days"
    ))
#total_revenue

  if "total_revenue" in df.columns:
    revenue = df['total_revenue'].dropna().values
    
    results.append(_make_result(
      "distribution_revenue",
      np.all(revenue>=0),
      f"min revenue: ${np.min(revenue):.2f}, max revenue: ${np.max(revenue):.2f}, mean revenue: ${np.mean(revenue):.2f}"
    ))
  return results

def run_validation(df: pd.DataFrame)-> pd.DataFrame:
  """
  Executess all the validations made above
  """
  print("=" * 50)
  print("VALIDATE — Duke kontrolluar cilësinë...")
  print("=" * 50)

  all_results= (
    check_completeness(df)+
    check_consistency(df)+
    check_distribution(df)
  )
  report = pd.DataFrame(all_results)

  total = len(report)
  passed = (report["status"] == "pass").sum()
  failed = (report["status"] == "fail").sum()   
  for _, row in report.iterrows():
        icon = "✓" if row["status"] == "pass" else "✗"
        print(f"{icon} {row['check']:<38} {row['status']:<8} {row['detail']}")
    
  #printing was taken from claude
  print("-" * 90)
  print(f"\nRezultati: {passed}/{total} kontrolle kaluan")
  
  if failed > 0:
      print(f"⚠ {failed} number of controls failed — look at the report for details")
  else:
      print("✓ All controls passed successfully")
  
  log_file = LOGS_PATH / f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
  report.to_csv(log_file, index=False)
  print(f"\n✓ Raporti u ruajt: {log_file}")
  
  return report


if __name__ == "__main__":
    from extract import extract_all
    from transform import transform_all
    
    datasets = extract_all()
    df       = transform_all(datasets)
    report   = run_validation(df)