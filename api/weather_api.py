"""
Weather API Integration Module
Fetches real-time weather data from OpenWeather API
"""

import requests
import os
from datetime import datetime
import json

class WeatherAPI:
    """
    Weather API client for fetching real-time weather data
    Uses OpenWeather API (requires API key)
    """
    
    def __init__(self, api_key=None):
        """
        Initialize Weather API client
        
        Args:
            api_key: OpenWeather API key (can also be set via environment variable)
        """
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY', 'YOUR_OPENWEATHER_API_KEY_HERE')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.enabled = self.api_key != 'YOUR_OPENWEATHER_API_KEY_HERE'
        
        if not self.enabled:
            print("Weather API not configured. Using simulated data.")
            print("To enable: Set OPENWEATHER_API_KEY environment variable")
    
    def get_current_weather(self, latitude, longitude):
        """
        Get current weather conditions for a location
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
        
        Returns:
            dict: Weather data including temperature, humidity, wind speed, etc.
        """
        if not self.enabled:
            return self._get_simulated_weather(latitude, longitude)
        
        try:
            # API endpoint for current weather
            url = f"{self.base_url}/weather"
            
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'  # Use Celsius
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract relevant weather information
                weather_data = {
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind'].get('deg', 0),
                    'cloudiness': data['clouds']['all'],
                    'precipitation': data.get('rain', {}).get('1h', 0),  # Rain in last hour
                    'weather_main': data['weather'][0]['main'],
                    'weather_description': data['weather'][0]['description'],
                    'visibility': data.get('visibility', 10000),
                    'timestamp': datetime.fromtimestamp(data['dt']).isoformat()
                }
                
                return weather_data
            else:
                print(f"Weather API error: {response.status_code}")
                return self._get_simulated_weather(latitude, longitude)
                
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return self._get_simulated_weather(latitude, longitude)
    
    def get_forecast(self, latitude, longitude, days=5):
        """
        Get weather forecast for a location
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            days: Number of days to forecast (max 5 for free tier)
        
        Returns:
            list: List of forecast data points
        """
        if not self.enabled:
            return self._get_simulated_forecast(latitude, longitude, days)
        
        try:
            url = f"{self.base_url}/forecast"
            
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                forecast_list = []
                for item in data['list'][:days * 8]:  # 8 forecasts per day (3-hour intervals)
                    forecast_data = {
                        'datetime': datetime.fromtimestamp(item['dt']).isoformat(),
                        'temperature': item['main']['temp'],
                        'humidity': item['main']['humidity'],
                        'pressure': item['main']['pressure'],
                        'wind_speed': item['wind']['speed'],
                        'precipitation': item.get('rain', {}).get('3h', 0),
                        'weather_main': item['weather'][0]['main'],
                        'weather_description': item['weather'][0]['description']
                    }
                    forecast_list.append(forecast_data)
                
                return forecast_list
            else:
                print(f"Forecast API error: {response.status_code}")
                return self._get_simulated_forecast(latitude, longitude, days)
                
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return self._get_simulated_forecast(latitude, longitude, days)
    
    def _get_simulated_weather(self, latitude, longitude):
        """
        Generate simulated weather data when API is not available
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
        
        Returns:
            dict: Simulated weather data
        """
        import random
        import math
        
        # Use location to seed random for consistency
        seed = int((latitude + 90) * 1000 + (longitude + 180) * 1000)
        random.seed(seed + int(datetime.now().timestamp()) // 3600)
        
        # Base temperature varies by latitude
        base_temp = 25 - abs(latitude) * 0.4
        
        # Add some randomness
        temp_variation = random.uniform(-5, 5)
        temperature = base_temp + temp_variation
        
        # Generate other weather parameters
        weather_conditions = ['Clear', 'Clouds', 'Rain', 'Drizzle', 'Thunderstorm', 'Snow']
        weights = [0.4, 0.3, 0.15, 0.1, 0.03, 0.02]
        weather_main = random.choices(weather_conditions, weights=weights)[0]
        
        # Precipitation based on weather type
        if weather_main == 'Rain':
            precipitation = random.uniform(2, 15)
        elif weather_main == 'Drizzle':
            precipitation = random.uniform(0.5, 2)
        elif weather_main == 'Thunderstorm':
            precipitation = random.uniform(10, 30)
        else:
            precipitation = 0
        
        weather_data = {
            'temperature': round(temperature, 1),
            'feels_like': round(temperature + random.uniform(-2, 2), 1),
            'humidity': random.randint(40, 90),
            'pressure': random.randint(1000, 1025),
            'wind_speed': round(random.uniform(0, 20), 1),
            'wind_direction': random.randint(0, 360),
            'cloudiness': random.randint(0, 100),
            'precipitation': round(precipitation, 1),
            'weather_main': weather_main,
            'weather_description': weather_main.lower(),
            'visibility': random.randint(5000, 10000),
            'timestamp': datetime.now().isoformat(),
            'simulated': True
        }
        
        return weather_data
    
    def _get_simulated_forecast(self, latitude, longitude, days):
        """Generate simulated weather forecast"""
        forecast = []
        
        for i in range(days * 8):
            hour_offset = i * 3
            forecast_time = datetime.now().timestamp() + (hour_offset * 3600)
            
            # Simulate temperature variation over time
            import random
            seed = int((latitude + 90) * 1000 + (longitude + 180) * 1000 + i)
            random.seed(seed)
            
            base_temp = 25 - abs(latitude) * 0.4
            temp_variation = random.uniform(-5, 5)
            
            forecast_data = {
                'datetime': datetime.fromtimestamp(forecast_time).isoformat(),
                'temperature': round(base_temp + temp_variation, 1),
                'humidity': random.randint(40, 90),
                'pressure': random.randint(1000, 1025),
                'wind_speed': round(random.uniform(0, 20), 1),
                'precipitation': round(random.uniform(0, 5), 1),
                'weather_main': random.choice(['Clear', 'Clouds', 'Rain']),
                'weather_description': 'simulated',
                'simulated': True
            }
            forecast.append(forecast_data)
        
        return forecast
    
    def get_air_quality(self, latitude, longitude):
        """
        Get air quality data for a location
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
        
        Returns:
            dict: Air quality index and components
        """
        if not self.enabled:
            return self._get_simulated_air_quality()
        
        try:
            url = f"{self.base_url}/air_pollution"
            
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                air_quality = {
                    'aqi': data['list'][0]['main']['aqi'],  # 1-5 scale
                    'co': data['list'][0]['components']['co'],
                    'no2': data['list'][0]['components']['no2'],
                    'o3': data['list'][0]['components']['o3'],
                    'pm2_5': data['list'][0]['components']['pm2_5'],
                    'pm10': data['list'][0]['components']['pm10']
                }
                
                return air_quality
            else:
                return self._get_simulated_air_quality()
                
        except Exception as e:
            print(f"Error fetching air quality: {e}")
            return self._get_simulated_air_quality()
    
    def _get_simulated_air_quality(self):
        """Generate simulated air quality data"""
        import random
        
        return {
            'aqi': random.randint(1, 5),
            'co': random.uniform(200, 400),
            'no2': random.uniform(10, 50),
            'o3': random.uniform(20, 80),
            'pm2_5': random.uniform(5, 35),
            'pm10': random.uniform(10, 50),
            'simulated': True
        }

if __name__ == "__main__":
    # Test the Weather API
    weather_api = WeatherAPI()
    
    # Test location: New York City
    lat, lon = 40.7128, -74.0060
    
    print("Testing Weather API...")
    print("\nCurrent Weather:")
    current = weather_api.get_current_weather(lat, lon)
    print(json.dumps(current, indent=2))
    
    print("\n5-Day Forecast:")
    forecast = weather_api.get_forecast(lat, lon, days=2)
    print(f"Retrieved {len(forecast)} forecast data points")
    
    print("\nAir Quality:")
    air_quality = weather_api.get_air_quality(lat, lon)
    print(json.dumps(air_quality, indent=2))