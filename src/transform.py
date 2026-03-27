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

  return df 

def clean_items(df: pd.DataFrame) -> pd.DataFrame:
  """
  Cleans the product dataset.
  1. Removes the negative/0 prices
  2. creates new column: total revenue for each item
  """
  df = df.copy()
  invalid_prices = (df['price']<=0).sum()
  df = df[df['price']>0]

  invalid_freight = (df['freight_value']<= 0).sum() #cost of transport
  df = df[df['freight_value'] > 0]

  #total revenue ->
  df['total_revenue'] = df['price'] + df['freight_value']

  df['price_tier']= pd.cut( #pd.cut for vectorization (better than using if else for 100,000 rows)
    df['price'],
    bins=[0,50,200,500, np.inf],
    labels =['budget','mid','premium','luxury']
  )

  print(f"Invalid prices: {invalid_prices + invalid_freight} removed.")
  print(f"Total revenue: ${df['total_revenue'].sum():,.2f}")
  print("Distribution of price tiers:")
  print(df['price_tier'].value_counts().to_string(index=True))
  return df

def merge_datasets(
    orders: pd.DataFrame,
    items: pd.DataFrame,
    customers: pd.DataFrame,
    payments: pd.DataFrame
) -> pd.DataFrame:
  """
  joins all 4 datasets altogether in an analytical table
  each row -> a product with all its details  
  """

  df = orders.merge(items, on ="order_id", how="inner") #inner to get only the rows that exist in both tables
  df = df.merge(customers, on="customer_id", how="left")

  payments_agg = payments.groupby("order_id").agg(
    total_payment = ("payment_value", "sum"),
    payment_installments = ("payment_installments", "max"),
    payment_type = ("payment_type", "first")
  ).reset_index()     # one to many 

  df = df.merge(payments_agg, on="order_id", how="left")

  df['delivery_days']=(
    df['order_delivered_customer_date']-
    df['order_purchase_timestamp']
  ).dt.days #how many days it took to deliver

  df["is_late"] = df["delivery_days"] > (
        df["order_estimated_delivery_date"] - 
        df["order_purchase_timestamp"]
    ).dt.days # number of days late
  
  print(f"Final Dataset: {df.shape[0]} rows, and {df.shape[1]} columns")
  print(f"Orders Delayed: {df['is_late'].sum()}, in percentage: {df['is_late'].mean() *100:,.2f}%")
  return df


def transform_all(datasets: dict) -> pd.DataFrame:
  """
  Exectues all the transformations
  """
  orders = clean_orders(datasets['orders'])
  items = clean_items(datasets['items'])
  customers = datasets['customers'].copy()
  payments = datasets['payments'].copy()

  df_final = merge_datasets(orders,items,customers,payments)
  return df_final

if __name__ == "__main__":
  from extract import extract_all

  datasets = extract_all()
  df = transform_all(datasets)

  print("\nFinal Column:")
  print(df.columns.tolist())
  print("\nExample:")
  print(df.head(3))