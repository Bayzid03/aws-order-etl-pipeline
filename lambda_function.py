"""
AWS Lambda function for processing and transforming order data from JSON to a flattened structure.

This Lambda function is triggered by S3 events and performs the following operations:
1. Reads JSON order data from an S3 bucket
2. Flattens the nested JSON structure (orders, customers, products) into a denormalized format
3. Converts the data into a pandas DataFrame for further processing
4. Prepares the data for loading into a data warehouse or analytics system

The function is designed to handle order data where each order contains:
- Order details (ID, date, total amount)
- Customer information (ID, name, email, address)
- One or more products (ID, name, category, price, quantity)

Example input JSON structure:
[
    {
        "order_id": 1,
        "order_date": "2024-01-10",
        "total_amount": 200.50,
        "customer": {
            "customer_id": 101,
            "name": "John Doe",
            "email": "johndoe@example.com",
            "address": "123 Main St"
        },
        "products": [
            {
                "product_id": "P01",
                "name": "Wireless Mouse",
                "category": "Electronics",
                "price": 25.00,
                "quantity": 2
            }
        ]
    }
]

Dependencies:
- boto3: For AWS services interaction
- pandas: For data manipulation and transformation
"""

import json
import boto3
import pandas as pd
import io
from datetime import datetime

def flatten(data):
    orders_data=[]
    for order in data:
        for product in order['products']:  
                    row_orders = {
                        "order_id" : order["order_id"],
                        "order_date" : order["order_date"],
                        "total_amount" : order["total_amount"],
                        "customer_id" : order["customer"]["customer_id"],
                        "customer_name" : order["customer"]["name"],
                        "email" : order["customer"]["email"],
                        "address" : order["customer"]["address"],
                        "product_id" : product["product_id"],
                        "product_name" : product["name"],
                        "category" : product["category"],
                        "price" : product["price"],
                        "quantity" : product["quantity"]
                    } 
                    orders_data.append(row_orders)   
    df_orders = pd.DataFrame(orders_data)
    return df_orders

def lambda_handler(event, context):
    # TODO implement
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key=event['Records'][0]['s3']['object']['key']

    s3 = boto3.client('s3') # Initialize S3 client
    response = s3.get_object(Bucket=bucket_name, Key=key) # Get the object from S3

    # Read and parse JSON content
    content = response['Body'].read().decode('utf-8')
    data = json.loads(content)
    df = flatten(data)
    
    # in-memory binary buffer to hold data like a file, but without writing to disk.
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False, engine='pyarrow')

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S") 

    key_staging=f'orders_parquet_datalake/orders_ETL_{timestamp}.parquet' # Staging key
    

    s3.put_object(Bucket=bucket_name, Key=key_staging, Body=parquet_buffer.getvalue()) # Upload to S3

    # Start Glue Crawler
    crawler_name = 'etl_pipeline_crawler'
    glue = boto3.client('glue') # Initialize Glue client
    response = glue.start_crawler(Name=crawler_name) # Start the crawler
