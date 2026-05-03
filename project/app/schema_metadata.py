SCHEMA_METADATA = """
Tables:

1. fact_events(
    event_time TIMESTAMP,
    visitor_id BIGINT,
    item_id BIGINT,
    event_type TEXT,        -- 'view', 'addtocart', 'transaction'
    transaction_id BIGINT
)

2. dim_item(
    item_id BIGINT,
    product_name TEXT,
    category_id BIGINT,
    price NUMERIC,
    is_available BOOLEAN
)

3. dim_category(
    category_id BIGINT,
    parent_category_id BIGINT,
    category_path TEXT
)

4. dim_time(
    date_id DATE,
    day_of_week INT,
    week INT,
    month INT,
    year INT
)
"""