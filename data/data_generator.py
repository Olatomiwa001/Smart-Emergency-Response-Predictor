"""
Sample Data Generator Module
Generates synthetic emergency data for training and testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_sample_data(num_samples=1000, output_path='data/emergency_data.csv'):
    """
    Generate synthetic emergency incident data
    
    Args:
        num_samples: Number of data samples to generate
        output_path: Path to save the CSV file
    
    Returns:
        DataFrame: Generated emergency data
    """
    print(f"Generating {num_samples} emergency data samples...")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Define city centers (major US cities)
    city_centers = {
        'New York': (40.7128, -74.0060),
        'Los Angeles': (34.0522, -118.2437),
        'Chicago': (41.8781, -87.6298),
        'Houston': (29.7604, -95.3698),
        'Phoenix': (33.4484, -112.0740),
        'Philadelphia': (39.9526, -75.1652),
        'San Antonio': (29.4241, -98.4936),
        'San Diego': (32.7157, -117.1611),
        'Dallas': (32.7767, -96.7970),
        'San Jose': (37.3382, -121.8863)
    }
    
    # Emergency types and their base probabilities
    emergency_types = {
        'Traffic Accident': 0.35,
        'Fire': 0.15,
        'Medical Emergency': 0.25,
        'Flood': 0.08,
        'Gas Leak': 0.07,
        'Building Collapse': 0.03,
        'Other': 0.07
    }
    
    data = []
    
    # Generate data for the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    for i in range(num_samples):
        # Random timestamp within the past year
        random_days = random.randint(0, 365)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        timestamp = start_date + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
        
        # Select random city
        city_name = random.choice(list(city_centers.keys()))
        city_lat, city_lon = city_centers[city_name]
        
        # Add randomness to location (within ~10km radius)
        lat_offset = np.random.normal(0, 0.05)
        lon_offset = np.random.normal(0, 0.05)
        latitude = city_lat + lat_offset
        longitude = city_lon + lon_offset
        
        # Extract time features
        hour = timestamp.hour
        day_of_week = timestamp.weekday()
        month = timestamp.month
        
        # Generate weather data
        # Base temperature varies by location latitude and season
        base_temp = 15 + (40 - abs(latitude)) * 0.5
        seasonal_var = 10 * np.sin((month - 1) * np.pi / 6)
        temperature = base_temp + seasonal_var + np.random.normal(0, 5)
        
        humidity = max(20, min(100, np.random.normal(60, 15)))
        wind_speed = max(0, np.random.gamma(2, 3))
        
        # Precipitation (higher in certain months)
        if month in [4, 5, 6, 7]:  # Spring/Summer rain
            precipitation = max(0, np.random.gamma(1.5, 2))
        elif month in [11, 12, 1, 2]:  # Winter precipitation
            precipitation = max(0, np.random.gamma(1, 3))
        else:
            precipitation = max(0, np.random.gamma(0.5, 1))
        
        pressure = np.random.normal(1013, 10)
        
        # Traffic density (higher during rush hours and weekdays)
        if hour in [7, 8, 17, 18] and day_of_week < 5:
            traffic_density = np.random.uniform(70, 100)
        elif hour in [6, 9, 16, 19] and day_of_week < 5:
            traffic_density = np.random.uniform(50, 80)
        elif 9 <= hour <= 17 and day_of_week < 5:
            traffic_density = np.random.uniform(40, 70)
        elif day_of_week >= 5:  # Weekend
            traffic_density = np.random.uniform(20, 50)
        else:
            traffic_density = np.random.uniform(10, 30)
        
        # Population density (based on distance from city center)
        distance_from_center = np.sqrt(lat_offset**2 + lon_offset**2)
        population_density = max(0, 100 - (distance_from_center * 500))
        
        # Determine if emergency occurred
        # Higher probability with:
        # - Extreme weather
        # - High traffic
        # - Rush hours
        # - Weekend nights
        
        emergency_prob = 0.3  # Base probability
        
        # Weather factors
        if temperature < 0 or temperature > 35:
            emergency_prob += 0.15
        if humidity > 80:
            emergency_prob += 0.08
        if wind_speed > 15:
            emergency_prob += 0.12
        if precipitation > 10:
            emergency_prob += 0.15
        
        # Time factors
        if hour in [7, 8, 17, 18]:  # Rush hour
            emergency_prob += 0.1
        if 22 <= hour or hour <= 4:  # Late night
            emergency_prob += 0.08
        if day_of_week in [5, 6]:  # Weekend
            emergency_prob += 0.05
        
        # Traffic factor
        if traffic_density > 70:
            emergency_prob += 0.1
        
        # Population density factor
        emergency_prob += population_density / 1000
        
        # Cap probability
        emergency_prob = min(0.85, emergency_prob)
        
        # Determine if emergency occurred
        emergency_occurred = 1 if random.random() < emergency_prob else 0
        
        # If emergency occurred, select type
        if emergency_occurred:
            # Adjust probabilities based on conditions
            type_probs = emergency_types.copy()
            
            if precipitation > 10:
                type_probs['Flood'] *= 3
                type_probs['Traffic Accident'] *= 1.5
            if wind_speed > 15:
                type_probs['Fire'] *= 0.5
                type_probs['Building Collapse'] *= 2
            if traffic_density > 70:
                type_probs['Traffic Accident'] *= 2
            
            # Normalize probabilities
            total_prob = sum(type_probs.values())
            type_probs = {k: v/total_prob for k, v in type_probs.items()}
            
            emergency_type = random.choices(
                list(type_probs.keys()),
                weights=list(type_probs.values())
            )[0]
        else:
            emergency_type = None
        
        # Severity (1-5 scale, only if emergency occurred)
        if emergency_occurred:
            # More severe in extreme conditions
            base_severity = random.randint(1, 5)
            if precipitation > 15 or wind_speed > 20 or temperature < -5 or temperature > 40:
                base_severity = min(5, base_severity + 1)
            severity = base_severity
        else:
            severity = None
        
        # Response time (minutes, only if emergency occurred)
        if emergency_occurred:
            # Faster in high-density areas, slower in bad weather
            base_response = np.random.gamma(3, 2)  # Mean ~6 minutes
            
            if population_density < 30:
                base_response *= 1.5
            if precipitation > 10:
                base_response *= 1.3
            if traffic_density > 70:
                base_response *= 1.4
            
            response_time = round(base_response, 1)
        else:
            response_time = None
        
        # Create data record
        record = {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'city': city_name,
            'latitude': round(latitude, 6),
            'longitude': round(longitude, 6),
            'hour': hour,
            'day_of_week': day_of_week,
            'month': month,
            'temperature': round(temperature, 1),
            'humidity': round(humidity, 1),
            'wind_speed': round(wind_speed, 1),
            'precipitation': round(precipitation, 1),
            'pressure': round(pressure, 1),
            'traffic_density': round(traffic_density, 1),
            'population_density': round(population_density, 1),
            'emergency_occurred': emergency_occurred,
            'emergency_type': emergency_type,
            'severity': severity,
            'response_time': response_time
        }
        
        data.append(record)
        
        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1}/{num_samples} samples...")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Display statistics
    print("\n" + "="*60)
    print("DATA GENERATION COMPLETE")
    print("="*60)
    print(f"\nTotal samples: {len(df)}")
    print(f"Emergency incidents: {df['emergency_occurred'].sum()} ({df['emergency_occurred'].mean()*100:.1f}%)")
    print(f"Non-emergency samples: {(df['emergency_occurred']==0).sum()} ({(df['emergency_occurred']==0).mean()*100:.1f}%)")
    
    if df['emergency_occurred'].sum() > 0:
        print("\nEmergency Type Distribution:")
        type_counts = df[df['emergency_occurred']==1]['emergency_type'].value_counts()
        for etype, count in type_counts.items():
            print(f"  {etype}: {count} ({count/df['emergency_occurred'].sum()*100:.1f}%)")
    
    print(f"\nData saved to: {output_path}")
    print("="*60)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    return df

def generate_realtime_test_data(num_locations=50):
    """
    Generate real-time test data for current conditions
    
    Args:
        num_locations: Number of test locations to generate
    
    Returns:
        DataFrame: Current test data
    """
    # Use current time
    current_time = datetime.now()
    
    # Generate random locations around major cities
    city_centers = [
        (40.7128, -74.0060),  # NYC
        (34.0522, -118.2437),  # LA
        (41.8781, -87.6298)   # Chicago
    ]
    
    data = []
    
    for i in range(num_locations):
        city_lat, city_lon = random.choice(city_centers)
        
        # Random offset
        lat = city_lat + np.random.normal(0, 0.05)
        lon = city_lon + np.random.normal(0, 0.05)
        
        record = {
            'latitude': round(lat, 6),
            'longitude': round(lon, 6),
            'timestamp': current_time.isoformat()
        }
        
        data.append(record)
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generate sample data
    df = generate_sample_data(num_samples=1000)
    
    # Display first few rows
    print("\nSample data preview:")
    print(df.head())