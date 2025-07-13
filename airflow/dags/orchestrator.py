from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

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
    dag_id='weather-api-dbt-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=1),
) as dag:
    
    task1 = PythonOperator(
        task_id = 'fetch_weather_data',
        python_callable=main
    )

    task2 = DockerOperator(
        task_id='transform_data',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(
                source='/Users/ritayanpatra/Projects/Grow Data Skill/Weather Data Pipeline/dbt/my_project',
                target='/usr/app',
                type='bind'
            ),
            Mount(
                source='/Users/ritayanpatra/Projects/Grow Data Skill/Weather Data Pipeline/dbt/profiles.yml',
                target='/root/.dbt/profiles.yml',
                type='bind'
            )
        ],
        # check the network name by running `docker network ls`
        network_mode='weatherdatapipeline_my_network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success'
    )

    task1 >> task2