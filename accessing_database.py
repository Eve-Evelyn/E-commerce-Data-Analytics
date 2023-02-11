import sqlite3 as db
import pandas as pd

conn = db.connect('olist.db')

cur = conn.cursor()

table = cur.execute("SELECT name FROM sqlite_master WHERE type= 'table'")
# print(f'The table names are: {table.fetchall()}')

data_customer = pd.read_sql_query(
    """
    SELECT * FROM olist_order_customer_dataset;
    """, conn)

data_order_items = pd.read_sql_query(
    """
    SELECT * FROM olist_order_items_dataset;
    """, conn)

data_order = pd.read_sql_query(
    """
    SELECT * FROM olist_order_dataset;
    """, conn)

data_products = pd.read_sql_query(
    """
    SELECT * FROM olist_products_dataset;
    """, conn)

data_sellers = pd.read_sql_query(
    """
    SELECT * FROM olist_sellers_dataset;
    """, conn)

data_category = pd.read_sql_query(
    """
    SELECT * FROM product_category_name_translation;
    """, conn)


# checking on duplicates for a few data that should not have duplicates, uncomment to use
# def check_duplicate(data, column):
#     print(data[column].duplicated().any())
# 
# 
# check_duplicate(data_customer, "customer_id")
# check_duplicate(data_order, "order_id")
# check_duplicate(data_products, "product_id")
# check_duplicate(data_sellers, "seller_id")
# check_duplicate(data_category, "product_category_name")
# no duplicates were found, all good

# obtain the product description length and photos quantity for the most sold item
max_sold_item = pd.read_sql_query(
    """
    WITH item_qty AS (
    SELECT order_id, MAX(order_item_id) AS qty, product_id
    FROM olist_order_items_dataset
    GROUP BY order_id, product_id)    

    SELECT item_qty.product_id, SUM(qty) AS total_sold_qty, product_description_lenght, product_photos_qty
    FROM item_qty
    LEFT JOIN olist_products_dataset AS prod
    on item_qty.product_id = prod.product_id
    GROUP BY item_qty.product_id
    ORDER BY total_sold_qty DESC;
    """, conn)

# obtain the best seller product categories
max_sold_category = pd.read_sql_query(
    """
    WITH item_qty AS (
    SELECT order_id, MAX(order_item_id) AS qty, ordit.product_id, product_category_name
    FROM olist_order_items_dataset AS ordit
    LEFT JOIN olist_products_dataset AS prod
    on ordit.product_id = prod.product_id
    GROUP BY order_id, ordit.product_id)    

    SELECT product_id, SUM(qty) AS total_qty, item_qty.product_category_name, product_category_name_english
    FROM item_qty
    LEFT JOIN product_category_name_translation AS trans
    on item_qty.product_category_name = trans.product_category_name
    GROUP BY item_qty.product_category_name
    ORDER BY total_qty DESC;
    """, conn)

# obtain the total number of order per customer
max_order_customer = pd.read_sql_query(
    """
    SELECT COUNT(order_id) AS order_count, customer_unique_id
    FROM olist_order_dataset AS ord
    LEFT JOIN olist_order_customer_dataset AS cust
    on ord.customer_id =cust.customer_id
    GROUP BY customer_unique_id
    ORDER BY order_count DESC;
    """, conn)

# obtain the city where the most number of orders comes from
max_customer_city = pd.read_sql_query(
    """
    SELECT customer_city, COUNT(order_id) AS order_count
    FROM olist_order_dataset
    LEFT JOIN olist_order_customer_dataset
    on olist_order_dataset.customer_id = olist_order_customer_dataset.customer_id
    GROUP BY customer_city
    ORDER BY order_count DESC;
    """, conn)

# obtain the state where the most number of orders comes from
max_customer_state = pd.read_sql_query(
    """
    SELECT customer_state, COUNT(order_id) AS order_count
    FROM olist_order_dataset
    LEFT JOIN olist_order_customer_dataset
    on olist_order_dataset.customer_id = olist_order_customer_dataset.customer_id
    GROUP BY customer_state
    ORDER BY order_count DESC;
    """, conn)

# obtain the city where the most number of products are sold from
max_seller_city = pd.read_sql_query(
    """
    WITH seller_item_qty AS (
    SELECT order_id, MAX(order_item_id) AS qty, product_id, ordit.seller_id, seller_city
    FROM olist_order_items_dataset AS ordit
    LEFT JOIN olist_sellers_dataset AS seller
    on ordit.seller_id = seller.seller_id
    GROUP BY order_id, product_id)

    SELECT SUM(qty) AS total_item_sold, seller_city
    FROM seller_item_qty
    GROUP BY seller_city
    ORDER BY total_item_sold DESC;
    """, conn)

# obtain the state where the most number of products are sold from
max_seller_state = pd.read_sql_query(
    """
    WITH seller_item_qty AS (
    SELECT order_id, MAX(order_item_id) AS qty, product_id, ordit.seller_id, seller_state
    FROM olist_order_items_dataset AS ordit
    LEFT JOIN olist_sellers_dataset AS seller
    on ordit.seller_id = seller.seller_id
    GROUP BY order_id, product_id)

    SELECT SUM(qty) AS total_item_sold, seller_state
    FROM seller_item_qty
    GROUP BY seller_state
    ORDER BY total_item_sold DESC;
    """, conn)