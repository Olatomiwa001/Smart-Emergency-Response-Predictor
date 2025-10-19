"""Quick script to create geocoding_api.py"""
from pathlib import Path

# The full geocoding_api.py content
content = '''"""
Geocoding API Integration
Converts addresses/city names to coordinates using multiple providers
Supports: Google Geocoding API, OpenCage Geocoder, and Nominatim (free fallback)
"""

import requests
import os
from typing import Dict, Optional, Tuple
import time

class GeocodingAPI:
    """
    Multi-provider geocoding service
    Automatically falls back to alternative providers if primary fails
    """
    
    def __init__(self, google_key=None, opencage_key=None):
        """
        Initialize geocoding API with multiple provider support
        
        Args:
            google_key: Google Geocoding API key (optional)
            opencage_key: OpenCage Geocoder API key (optional)
        """
        # API Keys from environment or parameters
        self.google_key = google_key or os.getenv('GOOGLE_GEOCODING_API_KEY', 'YOUR_GOOGLE_GEOCODING_API_KEY_HERE')
        self.opencage_key = opencage_key or os.getenv('OPENCAGE_API_KEY', 'YOUR_OPENCAGE_API_KEY_HERE')
        
        # Check which services are enabled
        self.google_enabled = self.google_key not in ['YOUR_GOOGLE_GEOCODING_API_KEY_HERE', None, '']
        self.opencage_enabled = self.opencage_key not in ['YOUR_OPENCAGE_API_KEY_HERE', None, '']
        self.nominatim_enabled = True  # Free service, always available
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds between requests
        
        # Service status
        if not any([self.google_enabled, self.opencage_enabled]):
            print("⚠ No geocoding API keys configured. Using Nominatim (free) only.")
            print("For better accuracy, add GOOGLE_GEOCODING_API_KEY or OPENCAGE_API_KEY to .env")
    
    def geocode(self, location_query: str, country_hint: Optional[str] = None) -> Optional[Dict]:
        """
        Geocode a location query (city, address, etc.) to coordinates
        Tries multiple providers in order: Google → OpenCage → Nominatim
        
        Args:
            location_query: Location string (e.g., "Lagos, Nigeria")
            country_hint: Optional country code for better accuracy
        
        Returns:
            Dictionary with location data or None if not found
        """
        # Respect rate limiting
        self._rate_limit()
        
        # Try providers in order of preference
        providers = []
        if self.google_enabled:
            providers.append(('google', self._geocode_google))
        if self.opencage_enabled:
            providers.append(('opencage', self._geocode_opencage))
        if self.nominatim_enabled:
            providers.append(('nominatim', self._geocode_nominatim))
        
        for provider_name, geocode_func in providers:
            try:
                result = geocode_func(location_query, country_hint)
                if result:
                    result['provider'] = provider_name
                    return result
            except Exception as e:
                print(f"  {provider_name} geocoding failed: {e}")
                continue
        
        print(f"❌ Could not geocode: {location_query}")
        return None
    
    def reverse_geocode(self, latitude: float, longitude: float) -> Optional[Dict]:
        """Reverse geocode coordinates to location name"""
        self._rate_limit()
        
        if self.google_enabled:
            try:
                return self._reverse_geocode_google(latitude, longitude)
            except: pass
        
        if self.opencage_enabled:
            try:
                return self._reverse_geocode_opencage(latitude, longitude)
            except: pass
        
        try:
            return self._reverse_geocode_nominatim(latitude, longitude)
        except: pass
        
        return None
    
    def _geocode_nominatim(self, location_query: str, country_hint: Optional[str]) -> Optional[Dict]:
        """Geocode using Nominatim (OpenStreetMap)"""
        url = "https://nominatim.openstreetmap.org/search"
        
        params = {
            'q': location_query,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        
        if country_hint:
            params['countrycodes'] = country_hint.lower()
        
        headers = {'User-Agent': 'SmartEmergencyPredictor/1.0'}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                result = data[0]
                address = result.get('address', {})
                
                return {
                    'latitude': float(result['lat']),
                    'longitude': float(result['lon']),
                    'formatted_address': result.get('display_name', ''),
                    'city': address.get('city', address.get('town', address.get('village', ''))),
                    'country': address.get('country', ''),
                    'country_code': address.get('country_code', '').upper(),
                    'confidence': 'medium'
                }
        
        return None
    
    def _geocode_google(self, location_query: str, country_hint: Optional[str]) -> Optional[Dict]:
        """Geocode using Google Geocoding API"""
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        
        params = {
            'address': location_query,
            'key': self.google_key
        }
        
        if country_hint:
            params['components'] = f'country:{country_hint}'
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                result = data['results'][0]
                location = result['geometry']['location']
                address_components = {c['types'][0]: c['long_name'] for c in result['address_components']}
                
                return {
                    'latitude': location['lat'],
                    'longitude': location['lng'],
                    'formatted_address': result['formatted_address'],
                    'city': address_components.get('locality', ''),
                    'country': address_components.get('country', ''),
                    'country_code': address_components.get('country', '')[:2],
                    'confidence': 'high'
                }
        
        return None
    
    def _geocode_opencage(self, location_query: str, country_hint: Optional[str]) -> Optional[Dict]:
        """Geocode using OpenCage Geocoder API"""
        url = "https://api.opencagedata.com/geocode/v1/json"
        
        params = {
            'q': location_query,
            'key': self.opencage_key,
            'limit': 1
        }
        
        if country_hint:
            params['countrycode'] = country_hint
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['results']:
                result = data['results'][0]
                geometry = result['geometry']
                components = result['components']
                
                return {
                    'latitude': geometry['lat'],
                    'longitude': geometry['lng'],
                    'formatted_address': result['formatted'],
                    'city': components.get('city', components.get('town', '')),
                    'country': components.get('country', ''),
                    'country_code': components.get('country_code', '').upper(),
                    'confidence': result.get('confidence', 5)
                }
        
        return None
    
    def _reverse_geocode_nominatim(self, latitude: float, longitude: float) -> Optional[Dict]:
        """Reverse geocode using Nominatim"""
        url = "https://nominatim.openstreetmap.org/reverse"
        
        params = {
            'lat': latitude,
            'lon': longitude,
            'format': 'json',
            'addressdetails': 1
        }
        
        headers = {'User-Agent': 'SmartEmergencyPredictor/1.0'}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            address = data.get('address', {})
            
            return {
                'formatted_address': data.get('display_name', ''),
                'city': address.get('city', address.get('town', '')),
                'country': address.get('country', '')
            }
        
        return None
    
    def _reverse_geocode_google(self, latitude: float, longitude: float) -> Optional[Dict]:
        """Reverse geocode using Google"""
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        
        params = {
            'latlng': f'{latitude},{longitude}',
            'key': self.google_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                result = data['results'][0]
                address_components = {c['types'][0]: c['long_name'] for c in result['address_components']}
                
                return {
                    'formatted_address': result['formatted_address'],
                    'city': address_components.get('locality', ''),
                    'country': address_components.get('country', '')
                }
        
        return None
    
    def _reverse_geocode_opencage(self, latitude: float, longitude: float) -> Optional[Dict]:
        """Reverse geocode using OpenCage"""
        url = "https://api.opencagedata.com/geocode/v1/json"
        
        params = {
            'q': f'{latitude},{longitude}',
            'key': self.opencage_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['results']:
                result = data['results'][0]
                components = result['components']
                
                return {
                    'formatted_address': result['formatted'],
                    'city': components.get('city', components.get('town', '')),
                    'country': components.get('country', '')
                }
        
        return None
    
    def _rate_limit(self):
        """Implement rate limiting to respect API policies"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()

if __name__ == "__main__":
    geo = GeocodingAPI()
    print("Testing geocoding...")
    result = geo.geocode("Lagos, Nigeria")
    if result:
        print(f"Found: {result['formatted_address']}")
'''

# Create the file
file_path = Path('api/geocoding_api.py')
file_path.parent.mkdir(exist_ok=True)
file_path.write_text(content, encoding='utf-8')

print(f"✓ Created: {file_path}")
print("\nNow run: python install_global_support.py")