with source as (
  SELECT * FROM {{source('olist', 'order_items')}}
),


renamed as (
  SELECT 
    order_id,
    order_item_id,
    product_id,
    seller_id,
    cast(shipping_limit_date as timestamp) as shipping_limit_at,
    price,
    freight_value,
  FROM source
)

SELECT * FROM renamed