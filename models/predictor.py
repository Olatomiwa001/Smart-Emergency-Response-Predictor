"""
Emergency Predictor Module
Handles real-time emergency risk prediction using trained models
"""

import numpy as np
import pandas as pd
import pickle
import os
from datetime import datetime

class EmergencyPredictor:
    """
    Emergency risk prediction class
    Loads trained model and makes predictions based on location and weather data
    """
    
    def __init__(self, model_path='models/emergency_model.pkl'):
        """Initialize predictor with trained model"""
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = None
        
        self.load_model()
    
    def load_model(self):
        """Load the trained model and preprocessing components"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    self.model = model_data['model']
                    self.scaler = model_data.get('scaler')
                    self.feature_names = model_data.get('feature_names', [])
                print("Model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
        else:
            print(f"Model file not found at {self.model_path}")
            print("Using fallback heuristic prediction")
    
    def predict_risk(self, latitude, longitude, weather_data):
        """
        Predict emergency risk for a given location and weather conditions
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            weather_data: Dictionary containing weather information
        
        Returns:
            float: Risk probability (0-1)
        """
        if self.model is None:
            # Fallback to heuristic prediction if model not available
            return self._heuristic_prediction(latitude, longitude, weather_data)
        
        try:
            # Prepare features
            features = self._prepare_features(latitude, longitude, weather_data)
            
            # Make prediction
            if self.scaler:
                features_scaled = self.scaler.transform([features])
            else:
                features_scaled = [features]
            
            # Get probability of emergency
            if hasattr(self.model, 'predict_proba'):
                risk_probability = self.model.predict_proba(features_scaled)[0][1]
            else:
                # For models without predict_proba, use decision function
                risk_score = self.model.predict(features_scaled)[0]
                risk_probability = float(risk_score)
            
            return float(risk_probability)
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._heuristic_prediction(latitude, longitude, weather_data)
    
    def _prepare_features(self, latitude, longitude, weather_data):
        """
        Prepare feature vector for prediction
        
        Features include:
        - Location (latitude, longitude)
        - Time features (hour, day_of_week, month)
        - Weather features (temperature, humidity, wind_speed, precipitation)
        - Traffic density (simulated or from API)
        """
        now = datetime.now()
        
        features = [
            latitude,
            longitude,
            now.hour,
            now.weekday(),
            now.month,
            weather_data.get('temperature', 20.0),
            weather_data.get('humidity', 50.0),
            weather_data.get('wind_speed', 5.0),
            weather_data.get('precipitation', 0.0),
            weather_data.get('pressure', 1013.0),
            self._estimate_traffic_density(now.hour, now.weekday()),
            self._estimate_population_density(latitude, longitude)
        ]
        
        return features
    
    def _estimate_traffic_density(self, hour, day_of_week):
        """
        Estimate traffic density based on time
        Higher during rush hours and weekdays
        
        Returns:
            float: Traffic density score (0-100)
        """
        # Rush hour traffic (7-9 AM, 5-7 PM)
        if hour in [7, 8, 17, 18]:
            base_traffic = 80
        elif hour in [6, 9, 16, 19]:
            base_traffic = 60
        elif 10 <= hour <= 15:
            base_traffic = 40
        elif 20 <= hour <= 23:
            base_traffic = 30
        else:
            base_traffic = 10
        
        # Weekday multiplier
        if day_of_week < 5:  # Monday-Friday
            multiplier = 1.0
        elif day_of_week == 5:  # Saturday
            multiplier = 0.7
        else:  # Sunday
            multiplier = 0.5
        
        return base_traffic * multiplier
    
    def _estimate_population_density(self, latitude, longitude):
        """
        Estimate population density based on location
        Simplified: uses distance from city center
        
        Returns:
            float: Population density score (0-100)
        """
        # Major city centers (simplified)
        city_centers = {
            'NYC': (40.7128, -74.0060),
            'LA': (34.0522, -118.2437),
            'Chicago': (41.8781, -87.6298),
            'Houston': (29.7604, -95.3698)
        }
        
        # Find closest city and calculate distance
        min_distance = float('inf')
        for city, (city_lat, city_lon) in city_centers.items():
            distance = np.sqrt((latitude - city_lat)**2 + (longitude - city_lon)**2)
            min_distance = min(min_distance, distance)
        
        # Convert distance to density (closer = denser)
        # Distance in degrees, roughly 0.01 degree = 1km
        density = max(0, 100 - (min_distance * 1000))
        
        return density
    
    def _heuristic_prediction(self, latitude, longitude, weather_data):
        """
        Fallback heuristic prediction when model is not available
        Based on simple rules combining weather and time factors
        
        Returns:
            float: Risk probability (0-1)
        """
        risk_score = 0.3  # Base risk
        
        # Weather factors
        temp = weather_data.get('temperature', 20)
        humidity = weather_data.get('humidity', 50)
        wind_speed = weather_data.get('wind_speed', 5)
        precipitation = weather_data.get('precipitation', 0)
        
        # Extreme temperature increases risk
        if temp < 0 or temp > 35:
            risk_score += 0.15
        
        # High humidity increases risk
        if humidity > 80:
            risk_score += 0.1
        
        # High wind speed increases risk
        if wind_speed > 15:
            risk_score += 0.15
        
        # Precipitation increases risk
        if precipitation > 5:
            risk_score += 0.2
        elif precipitation > 0:
            risk_score += 0.1
        
        # Time factors
        now = datetime.now()
        hour = now.hour
        
        # Late night/early morning slightly higher risk
        if 0 <= hour <= 4:
            risk_score += 0.1
        
        # Rush hour higher risk
        if hour in [7, 8, 17, 18]:
            risk_score += 0.05
        
        # Population density factor
        density = self._estimate_population_density(latitude, longitude)
        risk_score += (density / 1000)  # Small addition based on density
        
        # Cap at 0.95
        return min(0.95, risk_score)
    
    def predict_batch(self, locations_weather_data):
        """
        Predict risk for multiple locations
        
        Args:
            locations_weather_data: List of dicts with 'latitude', 'longitude', 'weather_data'
        
        Returns:
            list: Risk probabilities for each location
        """
        predictions = []
        
        for location_data in locations_weather_data:
            risk = self.predict_risk(
                location_data['latitude'],
                location_data['longitude'],
                location_data['weather_data']
            )
            predictions.append(risk)
        
        return predictions
    
    def get_high_risk_zones(self, grid_bounds, grid_resolution=10, risk_threshold=0.7):
        """
        Identify high-risk zones in a geographic grid
        
        Args:
            grid_bounds: Tuple of (min_lat, max_lat, min_lon, max_lon)
            grid_resolution: Number of grid points per dimension
            risk_threshold: Minimum risk level to be considered high-risk
        
        Returns:
            DataFrame: High-risk locations with coordinates and risk scores
        """
        min_lat, max_lat, min_lon, max_lon = grid_bounds
        
        # Create grid
        lats = np.linspace(min_lat, max_lat, grid_resolution)
        lons = np.linspace(min_lon, max_lon, grid_resolution)
        
        high_risk_zones = []
        
        for lat in lats:
            for lon in lons:
                # Simulate weather data (in production, fetch from API)
                weather_data = {
                    'temperature': np.random.uniform(15, 30),
                    'humidity': np.random.uniform(40, 80),
                    'wind_speed': np.random.uniform(0, 15),
                    'precipitation': np.random.uniform(0, 10),
                    'pressure': 1013.0
                }
                
                risk = self.predict_risk(lat, lon, weather_data)
                
                if risk >= risk_threshold:
                    high_risk_zones.append({
                        'latitude': lat,
                        'longitude': lon,
                        'risk_probability': risk,
                        **weather_data
                    })
        
        return pd.DataFrame(high_risk_zones)