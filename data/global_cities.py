"""
Global Cities Database
Comprehensive database of major cities worldwide with focus on African countries
Data source: Combination of GeoNames, SimpleMaps, and manual curation
"""

import pandas as pd
import json
from pathlib import Path

class GlobalCitiesDatabase:
    """
    Global cities database with extensive African coverage
    """
    
    def __init__(self):
        """Initialize with comprehensive city data"""
        self.cities = self._load_global_cities()
    
    def _load_global_cities(self):
        """
        Load comprehensive global cities database
        Includes major cities from all continents with special focus on Africa
        """
        cities_data = {
            # NIGERIA - Comprehensive coverage
            'Nigeria': [
                {'city': 'Lagos', 'lat': 6.5244, 'lon': 3.3792, 'population': 14000000},
                {'city': 'Kano', 'lat': 12.0022, 'lon': 8.5919, 'population': 3600000},
                {'city': 'Ibadan', 'lat': 7.3775, 'lon': 3.9470, 'population': 3565108},
                {'city': 'Abuja', 'lat': 9.0765, 'lon': 7.3986, 'population': 3000000},
                {'city': 'Port Harcourt', 'lat': 4.8156, 'lon': 7.0498, 'population': 1865000},
                {'city': 'Benin City', 'lat': 6.3350, 'lon': 5.6037, 'population': 1500000},
                {'city': 'Kaduna', 'lat': 10.5105, 'lon': 7.4165, 'population': 1400000},
                {'city': 'Onitsha', 'lat': 6.1670, 'lon': 6.7835, 'population': 1200000},
                {'city': 'Aba', 'lat': 5.1066, 'lon': 7.3667, 'population': 1100000},
                {'city': 'Ilorin', 'lat': 8.4967, 'lon': 4.5429, 'population': 1000000},
                {'city': 'Jos', 'lat': 9.9182, 'lon': 8.8919, 'population': 900000},
                {'city': 'Enugu', 'lat': 6.4403, 'lon': 7.4958, 'population': 820000},
                {'city': 'Warri', 'lat': 5.5160, 'lon': 5.7500, 'population': 750000},
                {'city': 'Calabar', 'lat': 4.9517, 'lon': 8.3417, 'population': 700000},
                {'city': 'Sokoto', 'lat': 13.0622, 'lon': 5.2339, 'population': 600000},
            ],
            
            # GHANA
            'Ghana': [
                {'city': 'Accra', 'lat': 5.6037, 'lon': -0.1870, 'population': 2291352},
                {'city': 'Kumasi', 'lat': 6.6885, 'lon': -1.6244, 'population': 2035064},
                {'city': 'Tema', 'lat': 5.6698, 'lon': -0.0167, 'population': 402637},
                {'city': 'Tamale', 'lat': 9.4008, 'lon': -0.8393, 'population': 371351},
                {'city': 'Takoradi', 'lat': 4.9000, 'lon': -1.7500, 'population': 250000},
            ],
            
            # KENYA
            'Kenya': [
                {'city': 'Nairobi', 'lat': -1.2864, 'lon': 36.8172, 'population': 4397073},
                {'city': 'Mombasa', 'lat': -4.0435, 'lon': 39.6682, 'population': 1208333},
                {'city': 'Kisumu', 'lat': -0.0917, 'lon': 34.7680, 'population': 409928},
                {'city': 'Nakuru', 'lat': -0.3031, 'lon': 36.0800, 'population': 307990},
                {'city': 'Eldoret', 'lat': 0.5143, 'lon': 35.2698, 'population': 289380},
            ],
            
            # SOUTH AFRICA
            'South Africa': [
                {'city': 'Johannesburg', 'lat': -26.2041, 'lon': 28.0473, 'population': 5635127},
                {'city': 'Cape Town', 'lat': -33.9249, 'lon': 18.4241, 'population': 4618000},
                {'city': 'Durban', 'lat': -29.8587, 'lon': 31.0218, 'population': 3442361},
                {'city': 'Pretoria', 'lat': -25.7479, 'lon': 28.2293, 'population': 2566000},
                {'city': 'Port Elizabeth', 'lat': -33.9608, 'lon': 25.6022, 'population': 1263051},
            ],
            
            # EGYPT
            'Egypt': [
                {'city': 'Cairo', 'lat': 30.0444, 'lon': 31.2357, 'population': 20900604},
                {'city': 'Alexandria', 'lat': 31.2001, 'lon': 29.9187, 'population': 5200000},
                {'city': 'Giza', 'lat': 30.0131, 'lon': 31.2089, 'population': 3628062},
            ],
            
            # ETHIOPIA
            'Ethiopia': [
                {'city': 'Addis Ababa', 'lat': 9.0320, 'lon': 38.7469, 'population': 3352000},
                {'city': 'Dire Dawa', 'lat': 9.5930, 'lon': 41.8661, 'population': 440000},
                {'city': 'Mekele', 'lat': 13.4967, 'lon': 39.4753, 'population': 340000},
            ],
            
            # TANZANIA
            'Tanzania': [
                {'city': 'Dar es Salaam', 'lat': -6.7924, 'lon': 39.2083, 'population': 5383728},
                {'city': 'Mwanza', 'lat': -2.5164, 'lon': 32.9175, 'population': 1120000},
                {'city': 'Arusha', 'lat': -3.3667, 'lon': 36.6833, 'population': 617631},
            ],
            
            # USA
            'USA': [
                {'city': 'New York', 'lat': 40.7128, 'lon': -74.0060, 'population': 8336817},
                {'city': 'Los Angeles', 'lat': 34.0522, 'lon': -118.2437, 'population': 3979576},
                {'city': 'Chicago', 'lat': 41.8781, 'lon': -87.6298, 'population': 2693976},
                {'city': 'Houston', 'lat': 29.7604, 'lon': -95.3698, 'population': 2320268},
                {'city': 'Phoenix', 'lat': 33.4484, 'lon': -112.0740, 'population': 1680992},
                {'city': 'Philadelphia', 'lat': 39.9526, 'lon': -75.1652, 'population': 1584064},
                {'city': 'San Antonio', 'lat': 29.4241, 'lon': -98.4936, 'population': 1547253},
                {'city': 'San Diego', 'lat': 32.7157, 'lon': -117.1611, 'population': 1423851},
                {'city': 'Dallas', 'lat': 32.7767, 'lon': -96.7970, 'population': 1343573},
                {'city': 'San Jose', 'lat': 37.3382, 'lon': -121.8863, 'population': 1021795},
            ],
            
            # UNITED KINGDOM
            'United Kingdom': [
                {'city': 'London', 'lat': 51.5074, 'lon': -0.1278, 'population': 9002488},
                {'city': 'Birmingham', 'lat': 52.4862, 'lon': -1.8904, 'population': 1141816},
                {'city': 'Manchester', 'lat': 53.4808, 'lon': -2.2426, 'population': 547627},
                {'city': 'Leeds', 'lat': 53.8008, 'lon': -1.5491, 'population': 793139},
                {'city': 'Glasgow', 'lat': 55.8642, 'lon': -4.2518, 'population': 633120},
            ],
            
            # CANADA
            'Canada': [
                {'city': 'Toronto', 'lat': 43.6532, 'lon': -79.3832, 'population': 2930000},
                {'city': 'Montreal', 'lat': 45.5017, 'lon': -73.5673, 'population': 1780000},
                {'city': 'Vancouver', 'lat': 49.2827, 'lon': -123.1207, 'population': 675218},
                {'city': 'Calgary', 'lat': 51.0447, 'lon': -114.0719, 'population': 1336000},
                {'city': 'Ottawa', 'lat': 45.4215, 'lon': -75.6972, 'population': 994837},
            ],
            
            # INDIA
            'India': [
                {'city': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'population': 20411000},
                {'city': 'Delhi', 'lat': 28.7041, 'lon': 77.1025, 'population': 16787941},
                {'city': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946, 'population': 12326532},
                {'city': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867, 'population': 10004144},
                {'city': 'Chennai', 'lat': 13.0827, 'lon': 80.2707, 'population': 7088000},
                {'city': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639, 'population': 4496694},
            ],
            
            # Additional African countries
            'Uganda': [
                {'city': 'Kampala', 'lat': 0.3476, 'lon': 32.5825, 'population': 1680000},
            ],
            'Rwanda': [
                {'city': 'Kigali', 'lat': -1.9706, 'lon': 30.1044, 'population': 1132686},
            ],
            'Senegal': [
                {'city': 'Dakar', 'lat': 14.6928, 'lon': -17.4467, 'population': 3137196},
            ],
            'Morocco': [
                {'city': 'Casablanca', 'lat': 33.5731, 'lon': -7.5898, 'population': 3751000},
                {'city': 'Rabat', 'lat': 34.0209, 'lon': -6.8416, 'population': 580000},
            ],
            'Algeria': [
                {'city': 'Algiers', 'lat': 36.7372, 'lon': 3.0865, 'population': 2694000},
            ],
            'Zimbabwe': [
                {'city': 'Harare', 'lat': -17.8292, 'lon': 31.0522, 'population': 2123132},
            ],
            'Cameroon': [
                {'city': 'Douala', 'lat': 4.0511, 'lon': 9.7679, 'population': 2768000},
                {'city': 'Yaoundé', 'lat': 3.8480, 'lon': 11.5021, 'population': 2440462},
            ],
        }
        
        # Flatten the dictionary into a list of all cities
        all_cities = []
        for country, cities in cities_data.items():
            for city in cities:
                city['country'] = country
                all_cities.append(city)
        
        return pd.DataFrame(all_cities)
    
    def search_city(self, city_name, country=None):
        """
        Search for a city in the database
        
        Args:
            city_name: Name of the city
            country: Optional country filter
        
        Returns:
            Dictionary with city information or None
        """
        # Case-insensitive search
        mask = self.cities['city'].str.lower() == city_name.lower()
        
        if country:
            mask = mask & (self.cities['country'].str.lower() == country.lower())
        
        results = self.cities[mask]
        
        if len(results) > 0:
            return results.iloc[0].to_dict()
        return None
    
    def get_all_countries(self):
        """Get list of all countries in database"""
        return sorted(self.cities['country'].unique().tolist())
    
    def get_cities_by_country(self, country):
        """Get all cities for a specific country"""
        return self.cities[self.cities['country'] == country].to_dict('records')
    
    def get_autocomplete_options(self, query, limit=10):
        """
        Get autocomplete suggestions for city search
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            List of matching city options
        """
        if not query or len(query) < 2:
            return []
        
        query_lower = query.lower()
        
        # Search in both city and country names
        mask = (
            self.cities['city'].str.lower().str.contains(query_lower) |
            self.cities['country'].str.lower().str.contains(query_lower)
        )
        
        results = self.cities[mask].head(limit)
        
        options = []
        for _, row in results.iterrows():
            options.append({
                'label': f"{row['city']}, {row['country']}",
                'city': row['city'],
                'country': row['country'],
                'lat': row['lat'],
                'lon': row['lon']
            })
        
        return options
    
    def save_to_csv(self, filepath='data/global_cities_database.csv'):
        """Save the database to CSV file"""
        self.cities.to_csv(filepath, index=False)
        print(f"✓ Saved {len(self.cities)} cities to {filepath}")

if __name__ == "__main__":
    # Test the database
    db = GlobalCitiesDatabase()
    
    print(f"Total cities in database: {len(db.cities)}")
    print(f"\nCountries covered: {', '.join(db.get_all_countries())}")
    
    # Test search
    print("\n--- Search Test ---")
    lagos = db.search_city("Lagos", "Nigeria")
    if lagos:
        print(f"Found: {lagos['city']}, {lagos['country']}")
        print(f"Coordinates: ({lagos['lat']}, {lagos['lon']})")
    
    # Test autocomplete
    print("\n--- Autocomplete Test ---")
    suggestions = db.get_autocomplete_options("Lag")
    for s in suggestions:
        print(f"  - {s['label']}")
    
    # Save to CSV
    db.save_to_csv()