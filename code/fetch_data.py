import requests
import os
from dotenv import load_dotenv
from pprint import pprint

class WeatherDataFetcher:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = os.getenv('WEATHER_BASE_URL')
    
    def fetch_weather_data(self, location):
        if not self.api_key or not self.base_url:
            raise ValueError("API key or base URL is not set in the environment variables.")
        
        url = f"{self.base_url}/current.json?key={self.api_key}&q={location}"
        try:

            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                print(f"Successfully fetched weather data for {location}.")
                return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching weather data: {e}")
            raise 

if __name__ == "__main__":
    fetcher = WeatherDataFetcher()
    location = "London"
    weather_data = fetcher.fetch_weather_data(location)
    pprint(weather_data)
    