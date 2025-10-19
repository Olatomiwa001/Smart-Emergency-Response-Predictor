# 🌍 Global Location Support

The Smart Emergency Response Predictor now supports **worldwide locations** with special focus on **Nigeria, Ghana, Kenya, South Africa**, and other African countries.

## 📍 Supported Regions

### Comprehensive Coverage

#### Africa (Primary Focus)
- **Nigeria**: Lagos, Kano, Ibadan, Abuja, Port Harcourt, Benin City, Kaduna, Onitsha, Aba, Ilorin, Jos, Enugu, Warri, Calabar, Sokoto
- **Ghana**: Accra, Kumasi, Tema, Tamale, Takoradi
- **Kenya**: Nairobi, Mombasa, Kisumu, Nakuru, Eldoret
- **South Africa**: Johannesburg, Cape Town, Durban, Pretoria, Port Elizabeth
- **Egypt**: Cairo, Alexandria, Giza
- **Ethiopia**: Addis Ababa, Dire Dawa, Mekele
- **Tanzania**: Dar es Salaam, Mwanza, Arusha
- **Uganda**: Kampala
- **Rwanda**: Kigali
- **Senegal**: Dakar
- **Morocco**: Casablanca, Rabat
- **Algeria**: Algiers
- **Zimbabwe**: Harare
- **Cameroon**: Douala, Yaoundé

#### Other Continents
- **North America**: USA (10+ major cities), Canada (5+ cities)
- **Europe**: United Kingdom (5+ cities)
- **Asia**: India (6+ major cities)

### Plus ANY Location Worldwide
Even if a city isn't in our database, the geocoding API will find it!

---

## 🔧 How It Works

### Three-Layer Location Resolution

1. **Local Database** (Fastest)
   - 100+ pre-loaded cities with population data
   - Instant lookup, no API calls needed
   - Optimized for African cities

2. **Geocoding APIs** (Global Coverage)
   - Google Geocoding API (best accuracy)
   - OpenCage Geocoder (excellent global coverage)
   - Nominatim/OpenStreetMap (free fallback)
   
3. **Manual Coordinates** (Universal)
   - Direct latitude/longitude input
   - Works anywhere on Earth

### Automatic Fallback System

```
User enters "Ibadan, Nigeria"
    ↓
1. Check local database → Found? ✓ Use it!
    ↓
2. If not found → Try Google Geocoding API
    ↓
3. If Google fails → Try OpenCage API
    ↓
4. If OpenCage fails → Try Nominatim (free)
    ↓
5. All failed? → Ask user for manual coordinates
```

---

## 🚀 Setup Instructions

### Step 1: Update Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure API Keys

Copy the environment template:
```bash
copy .env.example .env
```

Edit `.env` and add your API keys:

```env
# For best global coverage, add at least one geocoding API key:

# Option 1: Google Geocoding (Recommended)
GOOGLE_GEOCODING_API_KEY=your_google_key_here

# Option 2: OpenCage (Good alternative)
OPENCAGE_API_KEY=your_opencage_key_here

# Note: System works without API keys using free Nominatim,
# but with lower rate limits and accuracy
```

### Step 3: Get API Keys

#### Google Geocoding API (Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Geocoding API"
4. Go to Credentials → Create API Key
5. Copy key to `.env` file

**Free Tier**: $200/month credit (≈40,000 requests)

#### OpenCage Geocoder (Alternative)

1. Visit [OpenCage Data](https://opencagedata.com/)
2. Sign up for free account
3. Get API key from dashboard
4. Copy key to `.env` file

**Free Tier**: 2,500 requests/day

#### Nominatim (Automatic Fallback)

- No API key needed!
- Free OpenStreetMap service
- Rate limited to 1 request/second
- Automatically used if no other keys provided

---

## 💡 Usage Examples

### In the Dashboard

#### Example 1: Nigerian City
```
Input Method: City Name
Country Filter: Nigeria
City Name: Ibadan

Result: ✓ Found in database
Coordinates: (7.3775, 3.9470)
```

#### Example 2: Any Global City
```
Input Method: City Name
Country Filter: Any
City Name: Nairobi

Result: ✓ Found in database
Coordinates: (-1.2864, 36.8172)
```

#### Example 3: City Not in Database
```
Input Method: City Name
City Name: Abeokuta, Nigeria

Result: ✓ Found via geocoding
Coordinates: (7.1595, 3.3470)
Provider: Google Geocoding
⚠️ New location - predictions may be less accurate
```

#### Example 4: Small Town
```
Input Method: City Name
City Name: Osogbo, Nigeria

Result: ✓ Found via geocoding
Provider: Nominatim
```

### Using Python API

```python
from data.global_cities import GlobalCitiesDatabase
from api.geocoding_api import GeocodingAPI

# Initialize
cities_db = GlobalCitiesDatabase()
geo_api = GeocodingAPI()

# Search in database
lagos = cities_db.search_city("Lagos", "Nigeria")
print(f"{lagos['city']}: ({lagos['lat']}, {lagos['lon']})")

# Geocode any location
result = geo_api.geocode("Abeokuta, Nigeria")
print(f"Found: {result['formatted_address']}")
print(f"Coordinates: ({result['latitude']}, {result['longitude']})")

# Get autocomplete suggestions
suggestions = cities_db.get_autocomplete_options("Lag")
for s in suggestions:
    print(f"  - {s['label']}")
```

---

## 📊 Database Statistics

```python
from data.global_cities import GlobalCitiesDatabase

db = GlobalCitiesDatabase()
print(f"Total cities: {len(db.cities)}")
print(f"Countries: {len(db.get_all_countries())}")
print(f"Nigerian cities: {len(db.get_cities_by_country('Nigeria'))}")
```

**Current Coverage:**
- Total Cities: 100+
- Countries: 20+
- Nigerian Cities: 15
- African Cities: 50+

---

## 🔍 Features

### 1. Smart City Search
- Case-insensitive search
- Country filtering
- Autocomplete suggestions
- Fuzzy matching (via geocoding)

### 2. Multiple Input Methods
- City name only ("Lagos")
- City with country ("Lagos, Nigeria")
- Full address ("123 Main St, Accra, Ghana")
- Direct coordinates (6.5244, 3.3792)

### 3. Intelligent Fallbacks
- Database → Geocoding → Manual
- Multiple geocoding providers
- Graceful error handling
- User-friendly messages

### 4. Data Quality
- Population data included
- Accurate coordinates (verified)
- Regular updates supported
- Community contributions welcome

---

## 🌟 Best Practices

### For Accurate Results

1. **Include Country Name**
   - ✓ Good: "Ibadan, Nigeria"
   - ✗ Less Accurate: "Ibadan"

2. **Use Official City Names**
   - ✓ Good: "Johannesburg"
   - ✗ May Fail: "Joburg"

3. **Check Autocomplete**
   - System suggests similar cities
   - Helps catch spelling errors

4. **Verify Coordinates**
   - Map shows selected location
   - Ensure it's correct before prediction

### For Developers

1. **Add New Cities**
   ```python
   # Edit data/global_cities.py
   # Add to cities_data dictionary
   ```

2. **Custom Geocoding Provider**
   ```python
   # Extend api/geocoding_api.py
   # Add new _geocode_custom() method
   ```

3. **Update Database**
   ```python
   from data.global_cities import GlobalCitiesDatabase
   
   db = GlobalCitiesDatabase()
   db.save_to_csv('data/global_cities_database.csv')
   ```

---

## 🐛 Troubleshooting

### "City not found in database"
**Solution**: System will automatically try geocoding. If that fails:
- Check spelling
- Include country name
- Try coordinates instead

### "Geocoding API quota exceeded"
**Solution**: 
- Add alternative API key (OpenCage/Google)
- Use Nominatim (free, automatic fallback)
- Wait for quota reset

### "Predictions may be less accurate"
**Explanation**: This is normal for new locations not in training data.
**Impact**: Predictions use general patterns, not local historical data.
**Improvement**: Collect local data and retrain model.

### Slow Response
**Cause**: Geocoding API calls take time
**Solutions**:
- Use database cities (instant)
- Cache frequently used locations
- Consider local geocoding server

---

## 📈 Future Enhancements

- [ ] Add more African cities (100+ target)
- [ ] Support for postal codes
- [ ] Offline geocoding (local database)
- [ ] Custom location aliases
- [ ] Historical data per region
- [ ] Climate zone classification
- [ ] Regional emergency patterns

---

## 🤝 Contributing

### Add Your City

1. Fork the repository
2. Edit `data/global_cities.py`
3. Add city to appropriate country section
4. Include: name, lat, lon, population
5. Submit pull request

Example:
```python
'Nigeria': [
    {'city': 'Your City', 'lat': 0.0000, 'lon': 0.0000, 'population': 100000},
]
```

### Report Issues

- City coordinates incorrect?
- Geocoding not working?
- New city needed?

Open an issue on GitHub with details!

---

## 📧 Support

- **Documentation**: See main README.md
- **Issues**: GitHub Issues
- **Email**: princeola2004@gmail.com

---

Made with ❤️ for global emergency response

Special focus on serving **Nigeria** 🇳🇬 and **Africa** 🌍