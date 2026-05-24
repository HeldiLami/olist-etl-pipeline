import duckdb
import os

RAW = "data/raw"
WAREHOUSE = "lakehouse/warehouse"

os.makedirs(WAREHOUSE, exist_ok=True)

con = duckdb.connect()

tables = [
    "olist_customers_dataset",
    "olist_orders_dataset",
    "olist_order_items_dataset",
    "olist_order_payments_dataset",
    "olist_order_reviews_dataset",
    "olist_products_dataset",
    "olist_sellers_dataset",
    "olist_geolocation_dataset",
    "product_category_name_translation",
]

for table in tables:
    csv_path = f"{RAW}/{table}.csv"
    out_path = f"{WAREHOUSE}/{table}.parquet"
    con.execute(f"""
        COPY (SELECT * FROM read_csv_auto('{csv_path}'))
        TO '{out_path}' (FORMAT PARQUET)
    """)
    print(f"✓ {table} → parquet")

con.close()
print("\nDone. Të gjitha tabelat u konvertuan në Parquet.")