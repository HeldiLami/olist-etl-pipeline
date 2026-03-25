import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"

def load_csv(filename:str) -> pd.DataFrame:
  """
  Reads a CSV file from data/raw and returns it as a DataFrame
  Stops the program if the file doesnt exist.
  """
  filepath = RAW_DATA_PATH / filename
  
  if not filepath.exists():
    raise FileNotFoundError(
      f"file {filename} was not found  in {RAW_DATA_PATH}"
      f"check if it is in data/raw/ or not"
    )
  df = pd.read_csv(filepath)
  print(f"file '{filename}' loaded: {df.shape[0]} rows and {df.shape[1]} columns")
  
  return df

def extract_all() -> dict[str, pd.DataFrame]:
  """
  This loads the dataset and returns it as a dictionary,
  where the key is the name of the dataset and the value is the dataframe.
  """
  datasets = {
    "orders": load_csv("olist_orders_dataset.csv"),
    "items": load_csv("olist_order_items_dataset.csv"),
    "costumers": load_csv("olist_customers_dataset.csv"),
    "payments": load_csv("olist_order_payments_dataset.csv"),
  }
  print(f"loaded {len(datasets)} successfully")
  
  return datasets

if __name__ == "__main__":
  data = extract_all()
  for name, df in data.items():
    print(f"\n{name.upper()}")
    print(df.dtypes)
    print(df.head(2))