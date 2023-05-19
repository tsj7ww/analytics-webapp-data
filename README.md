# Analytics Webapp - Data
Code to generate data for analytics web app.

### Init
Init.sh
- Prod / Test
    - Terraform creates AWS RDS PostgreSQL instance
- Dev
    - Generates a containerized PostgreSQL database using Docker
- Python downloads, processes, and saves data into PostgreSQL database

### Maintenance
Code to maintain and update data.
- Prod = Airflow + Docker
- Test = Lambda
- Dev = Python + Docker
