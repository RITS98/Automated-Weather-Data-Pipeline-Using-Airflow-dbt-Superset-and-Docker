from fetch_data import WeatherDataFetcher
from dotenv import load_dotenv
import os
from pprint import pprint
import psycopg2
from psycopg2 import sql

class WeatherDataInserter:
    def __init__(self):
        load_dotenv()
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        print(f"Connecting to database at {self.db_host}:{self.db_port} with user {self.db_user}")
        
        self.connection = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )

    def create_table(self):
        try:
            with self.connection.cursor() as cursor:
                query = """
                CREATE SCHEMA IF NOT EXISTS dev;
                CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                    id SERIAL PRIMARY KEY,
                    city TEXT,
                    latitude FLOAT,
                    longitude FLOAT,
                    temperature_cel FLOAT,
                    wind_speed FLOAT,
                    humidity INT,
                    weather_description TEXT,
                    time TIMESTAMP,
                    inserted_at TIMESTAMP DEFAULT NOW(),
                    utc_offset TEXT
                );
                """
                cursor.execute(query)
                self.connection.commit()
                print("Table created successfully.")
        except psycopg2.Error as e:
            print(f"An error occurred while creating the table: {e}")
            self.connection.rollback()
            raise

    def insert_weather_data(self, weather_data):
        city = weather_data.get('location', {}).get('name')
        latitude = float(weather_data.get('location', {}).get('lat'))
        longitude = float(weather_data.get('location', {}).get('lon'))
        temperature_cel = float(weather_data.get('current', {}).get('temp_c'))
        wind_speed = float(weather_data.get('current', {}).get('wind_kph'))
        humidity = int(weather_data.get('current', {}).get('humidity'))
        weather_description = weather_data.get('current', {}).get('condition', {}).get('text')
        time = weather_data.get('location', {}).get('localtime')
        utc_offset = weather_data.get('location', {}).get('tz_id')

        print(city, latitude, longitude, temperature_cel, wind_speed, humidity, weather_description, time, utc_offset, sep=', ')

        try:
            with self.connection.cursor() as cursor:
                query = sql.SQL("""
                INSERT INTO dev.raw_weather_data (
                    city, latitude, longitude, temperature_cel, wind_speed, humidity, weather_description, time, inserted_at, utc_offset
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s
                )
                """)
                cursor.execute(query, (
                    city, latitude, longitude, temperature_cel,
                    wind_speed, humidity, weather_description,
                    time, utc_offset
                ))
                self.connection.commit()
                print("Weather data inserted successfully.")
        except psycopg2.Error as e:
            print(f"An error occurred while inserting data: {e}")
            self.connection.rollback()
            raise
        finally:    
            self.connection.close()
            print("Database connection closed.")
        pass
        


def main():
    fetcher = WeatherDataFetcher()
    inserter = WeatherDataInserter()
    location = "New York"

    inserter.create_table()
    weather_data = fetcher.fetch_weather_data(location=location)
    print("Fetched Weather Data for:", location)
    pprint(weather_data)
    if weather_data:
        inserter.insert_weather_data(weather_data)
        print(f"Weather data for {location} has been inserted into the database.")
    else:
        print("No data to insert.")
