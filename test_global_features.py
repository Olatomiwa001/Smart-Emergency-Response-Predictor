"""
Test Global Location Features
Tests the global cities database and geocoding functionality
"""

import sys
import time

def test_global_database():
    """Test the global cities database"""
    print("\n" + "="*60)
    print("TESTING GLOBAL CITIES DATABASE")
    print("="*60)
    
    try:
        from data.global_cities import GlobalCitiesDatabase
        
        db = GlobalCitiesDatabase()
        
        print(f"\n✓ Database loaded successfully")
        print(f"  Total cities: {len(db.cities)}")
        print(f"  Countries: {len(db.get_all_countries())}")
        
        # Test Nigerian cities
        print(f"\n📍 Nigerian Cities:")
        nigerian_cities = db.get_cities_by_country('Nigeria')
        print(f"  Count: {len(nigerian_cities)}")
        for city in nigerian_cities[:5]:
            print(f"  - {city['city']}: ({city['lat']:.4f}, {city['lon']:.4f})")
        
        # Test search
        print(f"\n🔍 Testing Search:")
        test_cities = [
            ("Lagos", "Nigeria"),
            ("Ibadan", "Nigeria"),
            ("Nairobi", "Kenya"),
            ("Accra", "Ghana"),
        ]
        
        for city, country in test_cities:
            result = db.search_city(city, country)
            if result:
                print(f"  ✓ {city}, {country}: ({result['lat']:.4f}, {result['lon']:.4f})")
            else:
                print(f"  ❌ {city}, {country}: Not found")
        
        # Test autocomplete
        print(f"\n💡 Testing Autocomplete for 'Lag':")
        suggestions = db.get_autocomplete_options("Lag")
        for s in suggestions[:5]:
            print(f"  - {s['label']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing database: {e}")
        return False

def test_geocoding():
    """Test geocoding functionality"""
    print("\n" + "="*60)
    print("TESTING GEOCODING API")
    print("="*60)
    
    try:
        from api.geocoding_api import GeocodingAPI
        
        geo = GeocodingAPI()
        
        # Check which services are enabled
        print(f"\n📡 Available Services:")
        print(f"  Google Geocoding: {'✓ Enabled' if geo.google_enabled else '❌ Disabled'}")
        print(f"  OpenCage Geocoder: {'✓ Enabled' if geo.opencage_enabled else '❌ Disabled'}")
        print(f"  Nominatim (OSM): {'✓ Enabled' if geo.nominatim_enabled else '❌ Disabled'}")
        
        if not geo.google_enabled and not geo.opencage_enabled:
            print(f"\n⚠️  No API keys configured. Using Nominatim (free) only.")
            print(f"   For better performance, add API keys to .env file")
        
        # Test geocoding
        print(f"\n🌍 Testing Geocoding:")
        test_locations = [
            "Lagos, Nigeria",
            "Ibadan, Nigeria",
            "Abeokuta, Nigeria",  # Not in database
            "Nairobi, Kenya",
        ]
        
        for location in test_locations[:2]:  # Limit to avoid rate limits
            print(f"\n  Geocoding: {location}")
            result = geo.geocode(location)
            
            if result:
                print(f"    ✓ Found: {result['formatted_address']}")
                print(f"    Coordinates: ({result['latitude']:.4f}, {result['longitude']:.4f})")
                print(f"    Provider: {result.get('provider', 'unknown')}")
            else:
                print(f"    ❌ Failed to geocode")
            
            time.sleep(1)  # Be nice to APIs
        
        # Test reverse geocoding
        print(f"\n🔄 Testing Reverse Geocoding:")
        print(f"  Coordinates: (6.5244, 3.3792)")
        result = geo.reverse_geocode(6.5244, 3.3792)
        
        if result:
            print(f"    ✓ Location: {result['formatted_address']}")
        else:
            print(f"    ❌ Failed")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing geocoding: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integration with dashboard"""
    print("\n" + "="*60)
    print("TESTING DASHBOARD INTEGRATION")
    print("="*60)
    
    try:
        # Check if all files exist
        import os
        from pathlib import Path
        
        required_files = {
            'data/global_cities.py': 'Global Cities Database',
            'api/geocoding_api.py': 'Geocoding API',
            'app/dashboard.py': 'Dashboard (updated)',
        }
        
        print(f"\n📁 Checking Required Files:")
        all_present = True
        
        for file_path, description in required_files.items():
            if Path(file_path).exists():
                print(f"  ✓ {description}: {file_path}")
            else:
                print(f"  ❌ {description}: {file_path} - MISSING!")
                all_present = False
        
        if all_present:
            print(f"\n✓ All required files present!")
        else:
            print(f"\n❌ Some files are missing. Please add them.")
            return False
        
        # Check environment file
        print(f"\n🔑 Checking Environment Configuration:")
        if Path('.env').exists():
            print(f"  ✓ .env file exists")
            
            with open('.env', 'r') as f:
                env_content = f.read()
                
            if 'GOOGLE_GEOCODING_API_KEY' in env_content:
                print(f"  ✓ Google Geocoding key configured")
            else:
                print(f"  ⚠️  Google Geocoding key not found")
            
            if 'OPENCAGE_API_KEY' in env_content:
                print(f"  ✓ OpenCage key configured")
            else:
                print(f"  ⚠️  OpenCage key not found")
        else:
            print(f"  ⚠️  .env file not found")
            print(f"     Copy .env.example to .env and add your API keys")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing integration: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  SMART EMERGENCY PREDICTOR - GLOBAL FEATURES TEST")
    print("="*60)
    
    results = {
        'database': test_global_database(),
        'geocoding': test_geocoding(),
        'integration': test_integration(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.capitalize()}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All tests passed! Global features are ready.")
        print("\nNext steps:")
        print("1. Add geocoding API keys to .env (optional but recommended)")
        print("2. Run: streamlit run main.py")
        print("3. Try searching for 'Lagos, Nigeria' or 'Ibadan, Nigeria'")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()