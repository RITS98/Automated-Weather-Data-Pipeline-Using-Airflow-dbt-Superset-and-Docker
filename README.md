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



### Setup dbt (Data Build Tool)
1. The image for dbt postgres can be found at `https://github.com/dbt-labs/dbt-core/pkgs/container/dbt-postgres`
2. Create the docker compose file as shown below
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
           env_file:
               - .env
           volumes:
               - ./postgres/data:/var/lib/postgresql/data
               - ./postgres/airflow_init.sql:/docker-entrypoint-initdb.d/airflow_init.sql
           networks:
               - my_network
   
       airflow:
           container_name: airflow_container
           image: apache/airflow:3.0.0
           ports:
               - "8001:8080"
           environment:
               AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@db:5432/airflow_db
           env_file:
               - .env
           volumes:
               - ./airflow/dags:/opt/airflow/dags
               - ./airflow/logs:/opt/airflow/logs
               - ./airflow/plugins:/opt/airflow/plugins
               - ./code:/opt/airflow/code
           depends_on:
               - db
           networks:
               - my_network
           command: >
               bash -c "airflow db migrate && airflow standalone"
       
       dbt:
           container_name: dbt_container
           image:  ghcr.io/dbt-labs/dbt-postgres:1.9.latest
           platform: linux/amd64                               # if using macOS, Force the container to use the amd64 platform by adding this to your dbt service
           volumes:
               - ./dbt:/usr/app
           working_dir: /usr/app
           depends_on:
               - db
           networks:
               - my_network
           command: init my_project

   networks:
       my_network:
           driver: bridge
   ```
3. Start the container using this command `docker compose run dbt`
4. Add teh all the requred informations as required for dbt project setup.
<img width="820" height="703" alt="image" src="https://github.com/user-attachments/assets/24536771-2ad1-406f-bac1-42e6836cc23b" />

5. Change the command in dbt service of docker compose file to this. Keep rest of the services same as before
   
   ```
   dbt:
     container_name: dbt_container
     image:  ghcr.io/dbt-labs/dbt-postgres:1.9.latest
     platform: linux/amd64                               # if using macOS, Force the container to use the amd64 platform by adding this to your dbt service
     volumes:
         - ./dbt:/usr/app
     working_dir: /usr/app
     depends_on:
         - db
     networks:
         - my_network
     command: debug                                       # Change from init to debug to check database connection
   ```
6. We get error as profiles.yml file is not present and it is not properly mounted.
7. Create a profiles.yml as per the `/.dbt/profiles.yml` and modify the docker compose as below
   
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
           env_file:
               - .env
           volumes:
               - ./postgres/data:/var/lib/postgresql/data
               - ./postgres/airflow_init.sql:/docker-entrypoint-initdb.d/airflow_init.sql
           networks:
               - my_network
   
       airflow:
           container_name: airflow_container
           image: apache/airflow:3.0.0
           ports:
               - "8001:8080"
           environment:
               AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@db:5432/airflow_db
           env_file:
               - .env
           volumes:
               - ./airflow/dags:/opt/airflow/dags
               - ./airflow/logs:/opt/airflow/logs
               - ./airflow/plugins:/opt/airflow/plugins
               - ./code:/opt/airflow/code
           depends_on:
               - db
           networks:
               - my_network
           command: >
               bash -c "airflow db migrate && airflow standalone"
       
       dbt:
           container_name: dbt_container
           image:  ghcr.io/dbt-labs/dbt-postgres:1.9.latest
           platform: linux/amd64                               # if using macOS, Force the container to use the amd64 platform by adding this to your dbt service
           volumes:
               - ./dbt/my_project:/usr/app
               - ./dbt:/root/.dbt
           working_dir: /usr/app
           depends_on:
               - db
           networks:
               - my_network
           command: run
   
   networks:
       my_network:
           driver: bridge
   ```
   
8. Keep the folder structure as below given
   
<img width="293" height="723" alt="image" src="https://github.com/user-attachments/assets/88a176a5-7d56-4bc3-b8d7-54d0078d3c20" />

### Create dbt code
1. Setup sources in models folder of dbt
2. Setup staging layer
3. Setup mart layer
4. All the sql data transformation files can be found in the `dbt` folder
5. To mock execute, run `docker compose up dbt`

### Orchestrate DBT container using Docker Operator
1. Rewrite the docker file as shown delow.
2. We need to give docker socker access to airflow. That is why we need to mount the docker.sock
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
           env_file:
               - .env
           volumes:
               - ./postgres/data:/var/lib/postgresql/data
               - ./postgres/airflow_init.sql:/docker-entrypoint-initdb.d/airflow_init.sql
           networks:
               - my_network
   
       airflow:
           container_name: airflow_container
           image: apache/airflow:3.0.0
           ports:
               - "8001:8080"
           environment:
               AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@db:5432/airflow_db
           env_file:
               - .env
           volumes:
               - ./airflow/dags:/opt/airflow/dags
               - ./airflow/logs:/opt/airflow/logs
               - ./airflow/plugins:/opt/airflow/plugins
               - ./code:/opt/airflow/code
               - /var/run/docker.sock:/var/run/docker.sock
           depends_on:
               - db
           networks:
               - my_network
           command: >
               bash -c "airflow db migrate && airflow standalone"
       
       dbt:
           container_name: dbt_container
           image:  ghcr.io/dbt-labs/dbt-postgres:1.9.latest
           platform: linux/amd64                               # if using macOS, Force the container to use the amd64 platform by adding this to your dbt service
           volumes:
               - ./dbt/my_project:/usr/app
               - ./dbt:/root/.dbt
           working_dir: /usr/app
           depends_on:
               - db
           networks:
               - my_network
           command: run
   
   networks:
       my_network:
           driver: bridge
   ```

4. In the dag file `dbt_orchestrator`, use a DockerOperator to run the container
5. Every time airflow, runs the container, it created a separate network. We need to add that network instead of docker-compose yml network confirguration.
6. Check the dag file for details on how to mount specific folders using DockerOperator.
7. Check the mock results below.
   <img width="1705" height="457" alt="image" src="https://github.com/user-attachments/assets/ca7d820a-1a03-41c8-9bf8-bd31af86b7df" />

   <img width="1696" height="683" alt="image" src="https://github.com/user-attachments/assets/6fcf72d6-2a08-4276-8858-995adb007dd1" />



### Setup Apache Superset for visualization
1. Go to the docker-compose file apache superset at this link `https://github.com/apache/superset/blob/master/docker-compose.yml`  
2. I am only taking the essential componenets of the Apache Superset.
3. Check the docker compose as shown below
   ```
   x-superset-user: &superset-user root
   x-superset-volumes: &superset-volumes
     # /app/pythonpath_docker will be appended to the PYTHONPATH in the final container
     - ./docker:/app/docker
     - ./docker/superset_config.py:/app/pythonpath/superset_config.py
   
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
           env_file:
               - .env
           volumes:
               - ./postgres/data:/var/lib/postgresql/data
               - ./postgres/airflow_init.sql:/docker-entrypoint-initdb.d/airflow_init.sql
               - ./postgres/superset_init.sql:/docker-entrypoint-initdb.d/superset_init.sql
           networks:
               - my_network
   
       airflow:
           container_name: airflow_container
           image: apache/airflow:3.0.0
           ports:
               - "8001:8080"
           environment:
               AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@db:5432/airflow_db
           env_file:
               - .env
           volumes:
               - ./airflow/dags:/opt/airflow/dags
               - ./airflow/logs:/opt/airflow/logs
               - ./airflow/plugins:/opt/airflow/plugins
               - ./code:/opt/airflow/code
               - /var/run/docker.sock:/var/run/docker.sock
           depends_on:
               - db
           networks:
               - my_network
           command: >
               bash -c "airflow db migrate && airflow standalone"
       
       dbt:
           container_name: dbt_container
           image:  ghcr.io/dbt-labs/dbt-postgres:1.9.latest
           platform: linux/amd64                               # if using macOS, Force the container to use the amd64 platform by adding this to your dbt service
           volumes:
               - ./dbt/my_project:/usr/app
               - ./dbt:/root/.dbt
           working_dir: /usr/app
           depends_on:
               - db
           networks:
               - my_network
           command: run
   
       superset:
           env_file:
           - path: docker/.env # default
             required: true
           image: apache/superset:3.0.0-py310
           container_name: superset_app
           command: ["/app/docker/docker-bootstrap.sh", "app"]
           restart: unless-stopped
           ports:
               - 8088:8088
           extra_hosts:
               - "host.docker.internal:host-gateway"
           user: *superset-user
           environment:
               SUPERSET__LOG_LEVEL: "${SUPERSET__LOG_LEVEL:-INFO}"
               DATABASE_DB: "superset_db"
           depends_on:
               superset-init:
                   condition: service_completed_successfully
           volumes: *superset-volumes
           networks:
               - my_network
       
       redis:
           image: redis:7
           container_name: superset_cache
           restart: unless-stopped
           ports:
               - "127.0.0.1:6379:6379"
           volumes:
               - redis:/data
           networks:
               - my_network
   
       
   
       superset-init:
           image: apache/superset:3.0.0-py310
           container_name: superset_init
           command: ["/app/docker/docker-init.sh"]
           env_file:
           - path: docker/.env # default
             required: true
           depends_on:
               db:
                   condition: service_started
               redis:
                   condition: service_started
           user: *superset-user
           volumes: *superset-volumes
           environment:
               SUPERSET__LOAD_EXAMPLES: "no"
               SUPERSET__LOG_LEVEL: "${SUPERSET__LOG_LEVEL:-INFO}"
               DATABASE_DB: "superset_db"
           healthcheck:
               disable: true
           networks:
               - my_network
   
   networks:
       my_network:
           driver: bridge
   
   volumes:
       redis:
           external: false
   ```

5. Create a docker folder in the base path as shown below and copy the following files from docker folder of github repo
  - `docker-init.sh`
  - `docker-bootstrap.sh`
  - `.env`
  - `pythonpath_dev\superset_config.py`

5. Create Postgres Apache Superset User and password using the `superset_init.sql` file inside the `postgres` folder

6. Make the changes in .env file as given in the repo to match the user credentials with that of postgres user credentials as mentioned in `superset_init.sql`

7. This the how it looks and it is loaded with examples datasets.
<img width="1685" height="597" alt="image" src="https://github.com/user-attachments/assets/4b86aa20-0d45-4dda-9ef9-74fc212f4054" />

8. Create a Database connection to `weather_db` by clicking on the plus button on top right corner.
9. Create a dataset.
<img width="1707" height="785" alt="image" src="https://github.com/user-attachments/assets/07288172-36e7-435d-a136-c96c4b4b8c21" />
10. Select a chart type.
<img width="865" height="846" alt="image" src="https://github.com/user-attachments/assets/68db76b1-6dda-4661-897e-711591d090a2" />

11. Create a Visualization
<img width="1708" height="861" alt="image" src="https://github.com/user-attachments/assets/844266c8-69d9-45fe-9335-82a7782f890a" />

<img width="763" height="488" alt="image" src="https://github.com/user-attachments/assets/ad551c4b-48e4-4e65-bd8a-b9dc1aff0ca3" />




