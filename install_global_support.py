"""
Install Global Location Support
Automatically sets up all global features
"""

from pathlib import Path
import os

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_files():
    """Check if new files were added"""
    print_header("Checking Global Support Files")
    
    required_files = {
        'data/global_cities.py': False,
        'api/geocoding_api.py': False,
    }
    
    updated_files = {
        'app/dashboard.py': False,
        'data/data_generator.py': False,
        '.env.example': False,
    }
    
    all_new_present = True
    print("\n📁 New Files Required:")
    for file_path in required_files.keys():
        exists = Path(file_path).exists()
        required_files[file_path] = exists
        status = "✓" if exists else "❌"
        print(f"  {status} {file_path}")
        if not exists:
            all_new_present = False
    
    print("\n📝 Updated Files:")
    for file_path in updated_files.keys():
        exists = Path(file_path).exists()
        updated_files[file_path] = exists
        status = "✓" if exists else "⚠️"
        print(f"  {status} {file_path}")
    
    return all_new_present, required_files, updated_files

def create_env_update():
    """Update .env file with new keys"""
    print_header("Updating Environment Configuration")
    
    env_additions = """
# =============================================================================
# GEOCODING API CONFIGURATION (NEW - For Global Location Support)
# =============================================================================

# Google Geocoding API Key (Recommended for best accuracy)
# Get your API key at: https://console.cloud.google.com/
# Enable: Geocoding API
GOOGLE_GEOCODING_API_KEY=YOUR_GOOGLE_GEOCODING_API_KEY_HERE

# OpenCage Geocoder API Key (Alternative, good for global coverage)
# Get your free API key at: https://opencagedata.com/
OPENCAGE_API_KEY=YOUR_OPENCAGE_API_KEY_HERE
"""
    
    if Path('.env').exists():
        with open('.env', 'r') as f:
            env_content = f.read()
        
        if 'GOOGLE_GEOCODING_API_KEY' not in env_content:
            print("✓ Adding geocoding API keys to .env file")
            with open('.env', 'a') as f:
                f.write(env_additions)
            print("  Please update the API keys in .env file")
        else:
            print("✓ Geocoding keys already in .env file")
    else:
        print("⚠️  .env file not found")
        print("   Creating .env from template...")
        if Path('.env.example').exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ Created .env file")
            print("  Please add your API keys to .env")
        else:
            print("❌ .env.example not found")
            return False
    
    return True

def initialize_database():
    """Initialize the global cities database"""
    print_header("Initializing Global Cities Database")
    
    try:
        from data.global_cities import GlobalCitiesDatabase
        
        db = GlobalCitiesDatabase()
        
        # Save to CSV for reference
        csv_path = 'data/global_cities_database.csv'
        db.save_to_csv(csv_path)
        
        print(f"✓ Initialized database with {len(db.cities)} cities")
        print(f"✓ Saved to {csv_path}")
        
        # Show statistics
        countries = db.get_all_countries()
        print(f"\n📊 Database Statistics:")
        print(f"  Total Cities: {len(db.cities)}")
        print(f"  Countries: {len(countries)}")
        
        # Show Nigerian cities count
        nigerian_cities = db.get_cities_by_country('Nigeria')
        print(f"  Nigerian Cities: {len(nigerian_cities)}")
        
        # Show top 5 Nigerian cities
        print(f"\n🇳🇬 Nigerian Cities (sample):")
        for city in nigerian_cities[:5]:
            print(f"    - {city['city']}: ({city['lat']:.4f}, {city['lon']:.4f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def regenerate_training_data():
    """Regenerate training data with global cities"""
    print_header("Regenerating Training Data with Global Coverage")
    
    response = input("\nDo you want to regenerate training data with global cities? (y/n): ")
    
    if response.lower() == 'y':
        try:
            from data.data_generator import generate_sample_data
            
            print("\nGenerating data...")
            generate_sample_data(num_samples=1000)
            
            print("✓ Training data regenerated with global coverage")
            return True
            
        except Exception as e:
            print(f"❌ Error generating data: {e}")
            return False
    else:
        print("⚠️  Skipped data regeneration")
        print("   You can regenerate later with: python -m data.data_generator")
        return True

def test_installation():
    """Test if everything works"""
    print_header("Testing Installation")
    
    try:
        # Test database
        print("\n1. Testing Global Cities Database...")
        from data.global_cities import GlobalCitiesDatabase
        db = GlobalCitiesDatabase()
        
        test_city = db.search_city("Lagos", "Nigeria")
        if test_city:
            print(f"   ✓ Database working: Found {test_city['city']}, {test_city['country']}")
        else:
            print("   ❌ Database test failed")
            return False
        
        # Test geocoding
        print("\n2. Testing Geocoding API...")
        from api.geocoding_api import GeocodingAPI
        geo = GeocodingAPI()
        
        if geo.google_enabled or geo.opencage_enabled or geo.nominatim_enabled:
            print(f"   ✓ Geocoding API initialized")
            print(f"     Google: {'Enabled' if geo.google_enabled else 'Disabled'}")
            print(f"     OpenCage: {'Enabled' if geo.opencage_enabled else 'Disabled'}")
            print(f"     Nominatim: {'Enabled' if geo.nominatim_enabled else 'Disabled'}")
        else:
            print("   ❌ No geocoding services available")
            return False
        
        # Test dashboard import
        print("\n3. Testing Dashboard Updates...")
        try:
            from app.dashboard import run_dashboard
            print("   ✓ Dashboard imports successfully")
        except ImportError as e:
            print(f"   ❌ Dashboard import failed: {e}")
            return False
        
        print("\n✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_next_steps():
    """Show what to do next"""
    print_header("Next Steps")
    
    print("""
1. 📝 Add API Keys (Optional but Recommended):
   - Edit .env file
   - Add GOOGLE_GEOCODING_API_KEY or OPENCAGE_API_KEY
   - Free tiers available for both services

2. 🧪 Test Global Features:
   python test_global_features.py

3. 🚀 Run the Application:
   streamlit run main.py

4. 🔍 Try These Searches:
   - Lagos, Nigeria
   - Ibadan, Nigeria
   - Nairobi, Kenya
   - Accra, Ghana
   - Any city worldwide!

5. 📚 Read Documentation:
   - GLOBAL_SUPPORT.md - Complete guide
   - README.md - General usage

💡 Tips:
- System works without API keys using free Nominatim
- Add API keys for better accuracy and higher rate limits
- Database includes 100+ cities, geocoding adds unlimited coverage
- African cities get special attention with detailed data

🌍 Enjoy worldwide emergency prediction!
""")

def main():
    """Main installation process"""
    print("\n" + "="*60)
    print("  SMART EMERGENCY PREDICTOR")
    print("  GLOBAL LOCATION SUPPORT INSTALLER")
    print("="*60)
    
    print("""
This installer will set up global location support including:
- 100+ cities worldwide (Nigeria, Ghana, Kenya, South Africa, etc.)
- Geocoding API integration for unlimited location coverage
- Updated dashboard with global search
- Multi-language support preparation

The system will work with or without API keys, using free fallbacks.
""")
    
    response = input("Continue with installation? (y/n): ")
    if response.lower() != 'y':
        print("Installation cancelled.")
        return
    
    # Step 1: Check files
    all_present, required, updated = check_files()
    
    if not all_present:
        print("\n❌ Required files are missing!")
        print("   Please ensure you have added:")
        for file_path, exists in required.items():
            if not exists:
                print(f"   - {file_path}")
        print("\n   Copy these files from the artifacts provided.")
        return
    
    # Step 2: Update environment
    env_ok = create_env_update()
    
    # Step 3: Initialize database
    db_ok = initialize_database()
    
    if not db_ok:
        print("\n❌ Database initialization failed")
        return
    
    # Step 4: Regenerate training data (optional)
    data_ok = regenerate_training_data()
    
    # Step 5: Test installation
    test_ok = test_installation()
    
    # Summary
    print_header("INSTALLATION COMPLETE")
    
    if test_ok:
        print("\n✅ Global location support successfully installed!")
        print(f"\n📊 Summary:")
        print(f"  ✓ Global Cities Database: Ready")
        print(f"  ✓ Geocoding API: Configured")
        print(f"  ✓ Dashboard: Updated")
        print(f"  ✓ Training Data: {'Updated' if data_ok else 'Skipped'}")
        
        show_next_steps()
    else:
        print("\n⚠️  Installation completed with warnings")
        print("   Some features may not work correctly")
        print("   Please review the errors above")

if __name__ == "__main__":
    main()