# Analytics Webapp - Data

Code to generate data for analytics web app.

### Init

Create AWS resources required for storing and maintaining data using Terraform.

Required Resources:

- RDS PostgreSQL (data)
- Lambda (maintenance)

### Base

Download data, process, and load into AWS RDS PostgreSQL database.

### Maintenance

##### Lambda

Lambda functions on AWS to maintain and update data.

##### Airflow

Containerized Airflow instance using Docker to maintain and update data.