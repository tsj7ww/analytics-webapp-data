# Analytics Webapp - Airflow

Airflow instance to generate data for analytics web app.

### Instance Management

##### Init & Startup
```
mkdir airflow
cd ./airflow

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.0/docker-compose.yaml'

mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env

docker compose up airflow-init
docker compose up
```

##### Cleanup
```
docker compose down --volumes --remove-orphans
docker compose down --volumes --rmi all
```