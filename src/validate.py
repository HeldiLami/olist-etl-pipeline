import numpy as np
import pandas as pd
import pathlib as Path
import datetime as datetime


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
    "time": datetime().now().strftime("%Y-%m-%d %H:%M:%S")
  }

def check_completeness(df: pd.DataFrame) -> list[dict]:
  """
  Checks if critical columns are not empty at a certain threshold
  """
  results = []

  critical_columns = {
    "order_id": 0.0,
    "costumer_id": 0.0,
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
    null_pct = df['col'].isnull().mean() * 100
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

  negative_prices = (df['price'] < 0)
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
    large_discrepancy = (discrepancy>1).mean * 100
    results.append(_make_result(
      "consistency_payment_vs_revenue",
      large_discrepancy <5.0, #if less than 5% of the orders have a discrepancy of 1% test is PASSED
      f"{large_discrepancy:.1f}% porosive kanë diferencë pagese > $1"
    ))

  return results

