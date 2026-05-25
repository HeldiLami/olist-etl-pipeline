from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType
import pyarrow.parquet as pq
import pyarrow.compute as pc

catalog = SqlCatalog("olist_catalog", uri="sqlite:///lakehouse/catalog/iceberg_catalog.db", warehouse="lakehouse/iceberg_warehouse")


schema = Schema(
    NestedField(1, "order_id", StringType(), False),
    NestedField(2, "customer_id", StringType(), False),
    NestedField(3, "order_status", StringType(), False),
)

try: catalog.create_namespace("olist")
except Exception: pass
try: catalog.drop_table("olist.orders")
except Exception: pass

table = catalog.create_table("olist.orders", schema=schema)

orders = pq.read_table("lakehouse/warehouse/olist_orders_dataset.parquet").select(["order_id", "customer_id", "order_status"])
table.append(orders)
snap_1 = table.current_snapshot().snapshot_id
print(f"Snapshot 1 — all orders: {len(table.scan().to_arrow())} records")

delivered_only = orders.filter(pc.equal(orders["order_status"], "delivered"))
table.overwrite(delivered_only)
total_2 = len(table.scan().to_arrow())
print(f"Snapshot 2 — only delivered: {total_2} records")

old_data_len = len(table.scan(snapshot_id=snap_1).to_arrow())
print(f"\n--- TIME TRAVEL in Snapshot 1 ---")
print(f"Snapshot 1 records: {old_data_len} (Difference: {old_data_len - total_2} orders recovered)")
