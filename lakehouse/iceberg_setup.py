import duckdb
import os

os.makedirs("lakehouse/catalog", exist_ok=True)

con = duckdb.connect("lakehouse/catalog/olist.duckdb")

con.execute("INSTALL iceberg")
con.execute("LOAD iceberg")

con.execute("""
    CREATE OR REPLACE TABLE orders AS
    SELECT * FROM read_parquet('lakehouse/warehouse/olist_orders_dataset.parquet')
""")

con.execute("""
    CREATE OR REPLACE TABLE order_items AS
    SELECT * FROM read_parquet('lakehouse/warehouse/olist_order_items_dataset.parquet')
""")

con.execute("""
    CREATE OR REPLACE TABLE customers AS
    SELECT * FROM read_parquet('lakehouse/warehouse/olist_customers_dataset.parquet')
""")

print("Tabels Created")
result = con.execute("SHOW TABLES").fetchdf()
print(result)

con.close()