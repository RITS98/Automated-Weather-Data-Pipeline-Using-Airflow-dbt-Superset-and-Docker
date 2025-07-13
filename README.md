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
- **Docker**: Each component runs in its own Docker container, allowing for easy deployment and management.


<img width="730" height="263" alt="image" src="https://github.com/user-attachments/assets/73cfc309-cce0-481f-bc51-58e62d013a71" />


## Project Building Steps

### Setup Database
1. Write a PostgreSQL Database Container in `docker-compose.yml`

   ```
    services:
    db:
        container_name: postgres_container        # name of the container
        image: postgres:14                        # postgres image containing version 14
        ports:
            - "5001:5432"                         # local_port:container_port
        environment:  
            POSTGRES_USER: postgres               # database credentials
            POSTGRES_PASSWORD: postgres            
            POSTGRES_DB: weather_db
        volumes:
            - ./postgres/data:/var/lib/postgresql/data         # local_folder which will be mounted as data storage folder in the container for persistant storage
   ```
2. Create the container is created by running `docker-compose up`
3. Check the container whether it is running or not by running this command `docker ps`
4. Check the database `weather_db` is created or not as shown below
<img width="998" height="482" alt="image" src="https://github.com/user-attachments/assets/c438a9ee-2d07-4a22-9c47-5eeebc3b42b1" />


### Setup Airflow
1. Create a `airflow_init.sql` file with following command and move it to `./postgres/airflow_init.sql`. It contains the below sql commands:
  ```
   CREATE USER airflow WITH PASSWORD 'airflow';
   CREATE DATABASE airflow_db OWNER airflow;
   ```
   This airflow db stores the metadata about the dags.
2. Create `\dags`, `\logs` and `\plugins` folder in the local as shown below.
   <img width="645" height="792" alt="image" src="https://github.com/user-attachments/assets/57c63c0b-6fc5-4480-ab37-599d0c64dbed" />

   To change permission: ```sudo chmod -R g+rw /postgres```

3. Change the docker compose file as follows:
   ```
   services:
       db:
           container_name: postgres_container
           image: postgres:14
           ports:
               - "5001:5432"
           environment:
               POSTGRES_USER: postgres
               POSTGRES_PASSWORD: postgres
               POSTGRES_DB: weather_db
           env_file:                              # Loads the environment variable to container shell
               - .env
           volumes:
               - ./postgres/data:/var/lib/postgresql/data
               - ./postgres/airflow_init.sql:/docker-entrypoint-initdb.d/airflow_init.sql               # This creates the airflow user for the database airflow
           networks:
               - my_network

       airflow:
           container_name: airflow_container
           image: apache/airflow:3.0.0
           ports:
               - "8001:8080"
           environment:
               AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@db:5432/airflow_db
           env_file:                                                     # Loads the environment variable to container shell
               - .env
           volumes:                                                      # this folders in the volume are shared between local and container for persistant storage
               - ./airflow/dags:/opt/airflow/dags                        # mount this folders to store dags into the container
               - ./airflow/logs:/opt/airflow/logs
               - ./airflow/plugins:/opt/airflow/plugins
               - ./code:/opt/airflow/code
           depends_on:
               - db
           networks:
               - my_network
           command: >
               bash -c "airflow db migrate && airflow standalone"         # to migrate the metadata to postgres database


   # common network to allow commumnication between containers
   networks:
       my_network:
           driver: bridge
   ```
4.  If containers are up, use `docker compose down` to remove the containers and restart using `docker compose up`
5.  Takes around 2 minutes to start with all services in the container
6.  Search for Password and copy it and login at `localhost:8001`
<img width="1233" height="350" alt="image" src="https://github.com/user-attachments/assets/6411c8e0-5c9e-418e-8563-23540581888c" />

<img width="1180" height="450" alt="image" src="https://github.com/user-attachments/assets/011a392f-82c1-42e2-ba1c-a680f76a2107" />

<img width="853" height="692" alt="image" src="https://github.com/user-attachments/assets/38572bbb-8061-4499-87bb-269460e6226e" />




### Try a Mock Run of the code
1. Keep the files as per the below picture:
<img width="290" height="440" alt="image" src="https://github.com/user-attachments/assets/70c2d00f-f852-4569-8269-fcd8c5b89448" />

2. The docker compose must be same as above.
3. See the Airflow Run as shown below
   <img width="1684" height="854" alt="image" src="https://github.com/user-attachments/assets/829ab17e-58db-49fd-b01c-b62750ff801b" />
4. Check the database
<img width="732" height="236" alt="image" src="https://github.com/user-attachments/assets/9b874062-ce8e-489f-b2f1-3059b9509c3e" />

<img width="1387" height="407" alt="image" src="https://github.com/user-attachments/assets/d6e4a85c-4d95-4ca1-974b-54097c97db59" />






