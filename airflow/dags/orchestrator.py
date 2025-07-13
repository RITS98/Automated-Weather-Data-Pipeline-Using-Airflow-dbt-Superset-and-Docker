from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow/code')
from insert_records import main


default_args = {
    'owner': 'Ritayan Patra',
    'description': 'Orchestrator DAG for Weather API data pipeline',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 13),
    'catchup': False,

}


with DAG(
    dag_id='weather-api-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=5),
) as dag:
    
    task1 = PythonOperator(
        task_id = 'fetch_weather_data',
        python_callable=main
    )