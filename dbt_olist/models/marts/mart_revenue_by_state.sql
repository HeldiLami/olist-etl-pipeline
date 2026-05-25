with fct_orders as(
  SELECT * FROM {{ ref('fct_orders') }}
)

SELECT
    customer_state,
    count(distinct order_id)        as total_orders,
    sum(total_price)                as total_revenue,
    round(avg(total_price), 2)      as avg_order_value,
    sum(total_items)                as total_items_sold
FROM fct_orders
WHERE order_status = 'delivered'
GROUP BY customer_state
ORDER BY total_revenue DESC