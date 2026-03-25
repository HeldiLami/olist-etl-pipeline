import pandas as pd
import numpy as np
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "output"
OUTPUT_PATH.mkdir(exist_ok = True)

def clean_orders(df:pd.DataFrame)->pd.DataFrame:
  """
  cleans the orders dataset 
  1. converts the date from string to date format
  2.removes the rows without a proper status
  3.removes duplicates
  """

  df = df.copy()
  
  date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
  ]

  for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors = "coerce") 
    # errors coerce => in case there isnt a proper date format or maybe NA,
    #  it will make those values -> NaT
  
  null_count_before = df.isnull().sum().sum()
  valid_status = [
    "delivered",
    "shipped",
    "processing",
    "invoiced"
  ]
  df = df[df['order_status'].isin(valid_status)]
  df = df.dropna(subset=["order_purchase_timestamp"]) # removes the rows where we dont have a purchase date

  duplicates = df.duplicated(subset = ["order_id"]).sum() #counts the duplicates
  df = df.drop_duplicates(subset=["order_id"])

  null_count_after = df.isnull().sum().sum()

  print(f"Duplicates: {duplicates}")
  print(f"Null Count before -> {null_count_before}, Null Count after -> {null_count_after}")
  print(f"Final number of rows: {len(df)}")

