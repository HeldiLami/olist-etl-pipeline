with source as (
  SELECT * FROM {{source('olist', 'orders')}}
),


renamed as (
  SELECT
    order_id,
    customer_id,
    order_status,
    cast(order_purchase_timestamp as timestamp) as purchased_at,
    cast(order_delivered_customer_date as timestamp) as delivered_at,
    cast(order_estimated_delivery_date as timestamp) as estimated_delivery_at
  FROM source
)

SELECT * FROM renamed