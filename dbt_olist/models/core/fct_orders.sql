with orders AS (
SELECT * FROM {{ ref('stg_orders') }}
),
order_items AS (
SELECT * FROM {{ ref('stg_order_items') }}
),

customers AS (
SELECT * FROM {{ ref('stg_customers') }}
),

joined AS(
  SELECT 
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchased_at,
    o.delivered_at,
    c.customer_state,
    c.customer_city,
    sum(oi.price) as total_price,
    sum(oi.freight_value) as total_freight,
    count(oi.order_item_id) as total_items
  FROM orders o
  LEFT JOIN order_items oi on o.order_id = oi.order_id
  LEFT JOIN customers c on o.customer_id = c.customer_id
  GROUP BY 1,2,3,4,5,6,7
)

SELECT * FROM joined