import duckdb

con = duckdb.connect()

print("Top 10 cities with the most clients:")
result = con.execute("""
    SELECT 
        customer_state,
        COUNT(*) as total_customers
    FROM read_parquet('lakehouse/warehouse/olist_customers_dataset.parquet')
    GROUP BY customer_state
    ORDER BY total_customers DESC
    LIMIT 10
""").fetchdf()
print(result)

print("\n=== Total and average revenue for each order status:")
result2 = con.execute("""
    SELECT
        o.order_status,
        COUNT(*) as total_orders,
        ROUND(SUM(oi.price), 2) as total_revenue, 
        ROUND(AVG(oi.price), 2) as avg_order_value
    FROM read_parquet('lakehouse/warehouse/olist_orders_dataset.parquet') o
    JOIN read_parquet('lakehouse/warehouse/olist_order_items_dataset.parquet') oi
        ON o.order_id = oi.order_id
    GROUP BY o.order_status
    ORDER BY total_revenue DESC
""").fetchdf()
print(result2)

con.close()