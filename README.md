# 📦 AWS Order ETL Pipeline

> **Serverless data engineering with Lambda, S3, Glue, and Athena for e-commerce analytics**

[![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-Serverless-FF9900?style=flat-square&logo=aws-lambda)](https://aws.amazon.com/lambda/)
[![Amazon S3](https://img.shields.io/badge/Amazon%20S3-Storage-569A31?style=flat-square&logo=amazon-s3)](https://aws.amazon.com/s3/)
[![AWS Glue](https://img.shields.io/badge/AWS%20Glue-ETL-FF9900?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/glue/)
[![Athena](https://img.shields.io/badge/Athena-Analytics-FF9900?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/athena/)

## 🎯 Overview

A **serverless ETL pipeline** processing e-commerce order data using AWS native services. Automatically flattens nested JSON orders into Parquet format, catalogs data with Glue, and enables SQL analytics through Athena - all with zero infrastructure management.

### ✨ Key Features

- **⚡ Event-Driven Processing** - S3 triggers Lambda on JSON file upload
- **🔄 Data Transformation** - Nested JSON flattening (orders → customers → products)
- **💾 Parquet Conversion** - Optimized columnar storage format
- **📊 Auto-Cataloging** - Glue Crawler for automatic schema discovery
- **🔍 SQL Analytics** - Athena queries on transformed data
- **💰 Cost-Effective** - Pay-per-use serverless architecture
- **🚀 Scalable** - Auto-scaling with AWS managed services

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   DATA SOURCE                                │
├──────────────────────────────────────────────────────────────┤
│  📄 E-commerce Order Data (JSON)                            │
│  • Nested structure: Orders → Customers → Products          │
│  • Files: orders_etl.json, incremental_data.json            │
│  • Upload trigger: Manual or automated ingestion            │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   INGESTION LAYER                            │
├──────────────────────────────────────────────────────────────┤
│  📦 Amazon S3 - Raw Data Bucket                             │
│  • Event: s3:ObjectCreated:*                                │
│  • Trigger: Invokes Lambda function on upload               │
│  • Path: s3://bucket-name/orders_*.json                     │
└──────────────────────────────────────────────────────────────┘
                            ↓
                   🔔 S3 Event Notification
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   TRANSFORMATION LAYER                       │
├──────────────────────────────────────────────────────────────┤
│  ⚡ AWS Lambda Function                                     │
│  • Runtime: Python 3.x                                       │
│  • Dependencies: boto3, pandas, pyarrow                      │
│  • Processing:                                               │
│    1. Read JSON from S3                                      │
│    2. Flatten nested structure                               │
│    3. Convert to DataFrame                                   │
│    4. Write Parquet to S3                                    │
│    5. Trigger Glue Crawler                                   │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   DATA LAKE LAYER                            │
├──────────────────────────────────────────────────────────────┤
│  💾 Amazon S3 - Transformed Data (Parquet)                  │
│  • Path: s3://bucket/orders_parquet_datalake/               │
│  • Format: orders_ETL_YYYYMMDD_HHMMSS.parquet               │
│  • Columnar storage with Snappy compression                  │
└──────────────────────────────────────────────────────────────┘
                            ↓
                  🤖 Lambda triggers Glue Crawler
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   CATALOG LAYER                              │
├──────────────────────────────────────────────────────────────┤
│  🗄️ AWS Glue Data Catalog                                   │
│  • Crawler: etl_pipeline_crawler                             │
│  • Auto-discover schema from Parquet files                   │
│  • Create/update metadata tables                             │
│  • Register in Glue Database                                 │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   ANALYTICS LAYER                            │
├──────────────────────────────────────────────────────────────┤
│  🔍 Amazon Athena                                            │
│  • SQL queries on Glue Catalog tables                        │
│  • Serverless, pay-per-query analytics                       │
│  • Query results stored in S3                                │
│  • Integration with BI tools (QuickSight, Tableau)           │
└──────────────────────────────────────────────────────────────┘
```

## 🛠️ Technical Stack

### **Core AWS Services**
- **⚡ AWS Lambda** - Serverless compute for data transformation
- **📦 Amazon S3** - Object storage for raw and transformed data
- **🤖 AWS Glue** - Serverless ETL and data catalog
- **🔍 Amazon Athena** - Serverless SQL analytics engine

### **Data Processing**
- **🐍 Python 3.x** - Lambda runtime environment
- **🐼 pandas** - Data manipulation and transformation
- **🦅 PyArrow** - Parquet file generation
- **☁️ boto3** - AWS SDK for Python

### **Data Formats**
- **📄 JSON** - Input format (nested structure)
- **📊 Parquet** - Output format (columnar, compressed)

## 📊 Data Transformation

### **Input: Nested JSON Structure**
```json
{
  "order_id": 1,
  "order_date": "2024-01-10",
  "total_amount": 200.50,
  "customer": {
    "customer_id": 101,
    "name": "John Doe",
    "email": "johndoe@example.com",
    "address": "123 Main St, Springfield"
  },
  "products": [
    {
      "product_id": "P01",
      "name": "Wireless Mouse",
      "category": "Electronics",
      "price": 25.00,
      "quantity": 2
    },
    {
      "product_id": "P02",
      "name": "Bluetooth Keyboard",
      "category": "Electronics",
      "price": 45.00,
      "quantity": 1
    }
  ]
}
```

### **Output: Flattened Parquet Schema**
| Column | Type | Description |
|--------|------|-------------|
| `order_id` | int | Unique order identifier |
| `order_date` | string | Order placement date |
| `total_amount` | float | Total order value |
| `customer_id` | int | Customer identifier |
| `customer_name` | string | Customer full name |
| `email` | string | Customer email |
| `address` | string | Shipping address |
| `product_id` | string | Product SKU |
| `product_name` | string | Product name |
| `category` | string | Product category |
| `price` | float | Unit price |
| `quantity` | int | Quantity ordered |

**Note:** One order with multiple products generates multiple rows (denormalized)

## 🚀 Quick Start

### Prerequisites
- AWS Account with appropriate IAM permissions
- AWS CLI configured
- Python 3.8+ (for local testing)

### Setup Instructions

**1. Create S3 Bucket**
```bash
aws s3 mb s3://your-orders-bucket
```

**2. Create Lambda Execution Role**
```bash
# Create IAM role with policies:
# - AWSLambdaBasicExecutionRole
# - AmazonS3FullAccess
# - AWSGlueServiceRole
```

**3. Deploy Lambda Function**
```bash
# Package dependencies (pandas + pyarrow)
pip install pandas pyarrow -t ./package
cd package
zip -r ../lambda_deployment.zip .
cd ..
zip -g lambda_deployment.zip lambda_function.py

# Create Lambda function
aws lambda create-function \
  --function-name OrderETLProcessor \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-s3-glue-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda_deployment.zip \
  --timeout 300 \
  --memory-size 512
```

**4. Configure S3 Event Trigger**
```bash
aws s3api put-bucket-notification-configuration \
  --bucket your-orders-bucket \
  --notification-configuration file://s3-notification.json
```

**s3-notification.json:**
```json
{
  "LambdaFunctionConfigurations": [
    {
      "LambdaFunctionArn": "arn:aws:lambda:region:account:function:OrderETLProcessor",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [
            {"Name": "suffix", "Value": ".json"}
          ]
        }
      }
    }
  ]
}
```

**5. Create Glue Crawler**
```bash
aws glue create-crawler \
  --name etl_pipeline_crawler \
  --role AWSGlueServiceRole-YourRole \
  --database-name orders_db \
  --targets '{
    "S3Targets": [
      {"Path": "s3://your-orders-bucket/orders_parquet_datalake/"}
    ]
  }'
```

**6. Upload Test Data**
```bash
aws s3 cp orders_etl.json s3://your-orders-bucket/
```

**7. Query with Athena**
```sql
-- Total sales by category
SELECT 
    category,
    SUM(price * quantity) AS total_sales,
    COUNT(DISTINCT order_id) AS order_count
FROM orders_db.orders_parquet_datalake
GROUP BY category
ORDER BY total_sales DESC;
```

## 📁 Project Structure

```
aws-order-etl-pipeline/
├── lambda_function.py              # Lambda transformation logic
├── orders_etl.json                # Sample order data (12 orders)
├── incremental_data.json          # Additional test data (3 orders)
└── README.md
```

## 🔧 Lambda Function Logic

### **Core Transformation: `flatten()` Function**
```python
def flatten(data):
    """
    Flattens nested JSON orders into denormalized rows.
    
    For each order with N products, creates N rows with:
    - Order details (replicated)
    - Customer details (replicated)
    - Individual product details
    
    Returns: pandas DataFrame
    """
    orders_data = []
    for order in data:
        for product in order['products']:
            row = {
                "order_id": order["order_id"],
                "order_date": order["order_date"],
                "total_amount": order["total_amount"],
                "customer_id": order["customer"]["customer_id"],
                "customer_name": order["customer"]["name"],
                "email": order["customer"]["email"],
                "address": order["customer"]["address"],
                "product_id": product["product_id"],
                "product_name": product["name"],
                "category": product["category"],
                "price": product["price"],
                "quantity": product["quantity"]
            }
            orders_data.append(row)
    return pd.DataFrame(orders_data)
```

### **Event Handler: `lambda_handler()`**
1. **Extract** - Parse S3 event to get bucket & key
2. **Read** - Download JSON file from S3
3. **Transform** - Flatten nested structure using pandas
4. **Convert** - DataFrame → Parquet (in-memory buffer)
5. **Load** - Upload Parquet to S3 with timestamp
6. **Catalog** - Trigger Glue Crawler for schema discovery

## 📈 Sample Analytics Queries

### **Top Customers by Revenue**
```sql
SELECT 
    customer_name,
    customer_id,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(price * quantity) AS total_spent
FROM orders_db.orders_parquet_datalake
GROUP BY customer_name, customer_id
ORDER BY total_spent DESC
LIMIT 10;
```

### **Product Performance**
```sql
SELECT 
    product_name,
    category,
    SUM(quantity) AS units_sold,
    ROUND(AVG(price), 2) AS avg_price,
    SUM(price * quantity) AS revenue
FROM orders_db.orders_parquet_datalake
GROUP BY product_name, category
ORDER BY revenue DESC;
```

### **Daily Order Trends**
```sql
SELECT 
    order_date,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(total_amount) AS daily_revenue
FROM orders_db.orders_parquet_datalake
GROUP BY order_date
ORDER BY order_date;
```

## 🌟 Key Benefits

### **Serverless Advantages**
- ✅ **No Infrastructure Management** - AWS handles scaling, patching, availability
- ✅ **Cost-Effective** - Pay only for execution time and data scanned
- ✅ **Auto-Scaling** - Handles variable workloads automatically
- ✅ **High Availability** - Built-in redundancy across AZs

### **Performance Optimizations**
- **Parquet Format** - 10-100x faster queries vs JSON
- **Columnar Storage** - Efficient compression and column pruning
- **Partitioning Ready** - Easy to add date-based partitions
- **In-Memory Processing** - No disk I/O in Lambda

### **Data Quality**
- **Schema Evolution** - Glue Crawler adapts to new columns
- **Type Safety** - Pandas ensures data type consistency
- **Incremental Loading** - Timestamped files prevent overwrites
- **Idempotent** - Re-running Lambda on same file is safe

## 💰 Cost Estimation

**For 1,000 orders/month:**
- **Lambda**: ~$0.20/month (1M requests free tier)
- **S3**: ~$0.50/month (storage + requests)
- **Glue Crawler**: ~$0.44/month (hourly runs)
- **Athena**: ~$0.10/month (data scanned)

**Total: ~$1.24/month** (with free tier benefits)

## 🎯 Use Cases

- **📊 E-commerce Analytics** - Order and product insights
- **👥 Customer Analytics** - Purchase behavior and segmentation
- **📦 Inventory Management** - Product demand forecasting
- **💼 Business Intelligence** - Executive dashboards
- **🔍 Ad-hoc Analysis** - SQL queries for quick insights

## 🚀 Future Enhancements

- [ ] **🔔 EventBridge Integration** - Scheduled or event-driven processing
- [ ] **📊 QuickSight Dashboards** - Visual analytics and reports
- [ ] **🗂️ S3 Partitioning** - Optimize queries by date/category
- [ ] **🔄 Change Data Capture** - Track incremental updates
- [ ] **⚠️ Data Quality Checks** - Validation rules in Lambda
- [ ] **📈 CloudWatch Metrics** - Custom monitoring and alerts
- [ ] **🔐 Data Encryption** - KMS encryption at rest

## 🤝 Contributing

Contributions welcome! Focus areas:
- **🧪 Unit Tests** - Lambda function testing
- **📊 Additional Queries** - Analytics templates
- **🔧 Error Handling** - Enhanced logging and retries
- **📈 Performance** - Optimization for large files

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Serverless ETL made simple with AWS native services** ⚡📦
