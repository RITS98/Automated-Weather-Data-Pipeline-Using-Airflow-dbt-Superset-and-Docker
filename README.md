# Dockerized Weather Data Pipeline Using Airflow, dbt, PostgreSQL and Apache Superset

This project is a Dockerized pipeline that fetches weather data from an API, processes it using Apache Airflow and dbt, stores it in a PostgreSQL database, and visualizes it with Apache Superset. The pipeline is designed to be modular and scalable, allowing for easy integration of additional data sources or processing steps.

## Technologies Used
- **Docker**: For containerization of the entire pipeline.
- **Apache Airflow**: For orchestrating the data pipeline.
- **dbt (data build tool)**: For transforming the data.
- **PostgreSQL**: For storing the processed data.
- **Apache Superset**: For data visualization.

## Architecture Overview
The architecture consists of several components:
- **Weather Data API**: The source of weather data.
- **Airflow**: Manages the workflow of fetching, processing, and storing data.
- **dbt**: Transforms the raw data into a structured format.
- **PostgreSQL**: The database where the processed data is stored.
- **Superset**: Provides a user interface for visualizing the data.






