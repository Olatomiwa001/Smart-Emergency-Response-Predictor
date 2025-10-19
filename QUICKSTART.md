# 🚀 Quick Start Guide

Get the Smart Emergency Response Predictor running in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- Internet connection
- (Optional) API keys for real-time data

## Step-by-Step Setup

### 1. Download and Extract

Download the project and extract to a folder.

### 2. Open Terminal/Command Prompt

Navigate to the project directory:

```bash
cd path/to/smart-emergency-predictor
```

### 3. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will take 2-3 minutes to install all required packages.

### 5. Set Up Environment Variables (Optional)

For simulated data (works without API keys):
```bash
# No setup needed! The app works out of the box with simulated data
```

For real-time data (requires API keys):
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
# Get free keys from:
# - OpenWeather: https://openweathermap.org/api
# - Google Maps: https://console.cloud.google.com/
```

### 6. Generate Sample Data

```bash
python -m data.data_generator
```

This creates 1000 synthetic emergency records in `data/emergency_data.csv`

### 7. Train the Model

```bash
python -m models.train_model
```

This trains the ML model and saves it to `models/emergency_model.pkl`

### 8. Run the Application

```bash
streamlit run main.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## 🎉 You're Ready!

### What to Try First:

1. **Risk Prediction Page**
   - Try coordinates: 40.7128, -74.0060 (New York)
   - Click "Get Current Weather & Risk"
   - See the risk map with predicted zones

2. **Route Optimization Page**
   - Start: 40.7589, -73.9851
   - End: 40.7128, -74.0060
   - Click "Calculate Optimal Route"

3. **Analytics Page**
   - View historical emergency patterns
   - Explore charts and trends

4. **Model Training Page**
   - Try different model types
   - View performance metrics

## Common Issues

**Issue: Port already in use**
```bash
# Solution: Use a different port
streamlit run main.py --server.port=8502
```

**Issue: Module not found**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Issue: Permission denied (macOS/Linux)**
```bash
# Solution: Use sudo or check permissions
chmod +x main.py
```

## Next Steps

- Add your API keys to `.env` for real-time weather and routing
- Collect real emergency data for better predictions
- Customize the dashboard for your needs
- Deploy to Streamlit Cloud for public access

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Open an issue on GitHub
- Read the code comments for understanding

## Pro Tips

1. **Start with simulated data** - The app works great without API keys for testing
2. **Use free API tiers** - OpenWeather and Google Maps offer free tiers
3. **Train regularly** - Retrain the model when you have new data
4. **Explore the code** - Everything is well-commented and modular

Happy Predicting! 🚨