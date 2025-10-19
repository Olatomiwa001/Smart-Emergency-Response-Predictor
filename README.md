# 🚨 Smart Emergency Response Predictor

An AI-powered web application that predicts where emergencies (like accidents, fires, or floods) are most likely to occur and recommends the fastest emergency response routes using real-time data.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Keys](#api-keys)
- [Model Training](#model-training)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality

1. **Emergency Risk Prediction**
   - Predicts high-risk zones for emergencies using ML models
   - Real-time weather integration for accurate predictions
   - Interactive risk visualization on maps
   - Historical trend analysis

2. **Route Optimization**
   - Calculates fastest routes for emergency responders
   - Real-time traffic consideration
   - Multiple route alternatives
   - ETA calculations

3. **Interactive Dashboard**
   - Real-time risk monitoring
   - Geographic heat maps
   - Analytics and reporting
   - Model performance metrics

4. **Data Analytics**
   - Historical emergency patterns
   - Time-based trend analysis
   - Weather correlation analysis
   - Performance dashboards

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3.8+
- **ML Framework**: scikit-learn, TensorFlow/PyTorch (optional)
- **Web Framework**: Streamlit
- **APIs**: OpenWeather API, Google Maps API, OpenRouteService API

### Data & Visualization
- **Data Processing**: pandas, numpy
- **Visualization**: Plotly, Folium, Matplotlib, Seaborn
- **Maps**: Folium, Streamlit-Folium

### Database (Optional)
- **Storage**: SQLite (default), PostgreSQL (production)

## 📁 Project Structure

```
smart-emergency-predictor/
│
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── README.md                  # This file
│
├── app/                       # Application modules
│   ├── __init__.py
│   └── dashboard.py          # Streamlit dashboard
│
├── models/                    # ML models
│   ├── __init__.py
│   ├── predictor.py          # Prediction logic
│   ├── train_model.py        # Model training
│   └── emergency_model.pkl   # Trained model (generated)
│
├── api/                       # API integrations
│   ├── __init__.py
│   ├── weather_api.py        # Weather data fetching
│   └── routing_api.py        # Route optimization
│
├── data/                      # Data storage
│   ├── __init__.py
│   ├── data_generator.py     # Sample data generation
│   └── emergency_data.csv    # Training data (generated)
│
└── tests/                     # Unit tests (optional)
    ├── __init__.py
    ├── test_predictor.py
    ├── test_apis.py
    └── test_training.py
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Virtual environment tool (venv, conda)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/smart-emergency-predictor.git
cd smart-emergency-predictor
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# OpenWeather API Key
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Google Maps API Key (optional)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# OpenRouteService API Key (alternative to Google Maps)
OPENROUTE_API_KEY=your_openroute_api_key_here

# Database Configuration (optional)
DATABASE_URL=sqlite:///emergency_data.db
```

## 🔑 API Keys

### OpenWeather API (Required for real weather data)

1. Visit [OpenWeather](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Add to `.env` file

**Free Tier**: 60 calls/minute, 1,000,000 calls/month

### Google Maps API (Optional - for routing)

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Directions API" and "Maps JavaScript API"
4. Generate API key
5. Add to `.env` file

**Free Tier**: $200 credit/month

### OpenRouteService API (Alternative routing)

1. Visit [OpenRouteService](https://openrouteservice.org/)
2. Sign up for free
3. Generate API key
4. Add to `.env` file

**Free Tier**: 2000 requests/day

## 📊 Model Training

### Generate Sample Data

```bash
python -m data.data_generator
```

This generates 1000 synthetic emergency records with realistic patterns.

### Train the Model

```bash
python -m models.train_model
```

Or use the dashboard interface:
1. Run the application
2. Navigate to "Model Training" page
3. Click "Generate Sample Data"
4. Click "Train Model"

### Model Performance

The trained model achieves:
- **Accuracy**: ~85-90%
- **Precision**: ~80-85%
- **Recall**: ~75-85%
- **F1 Score**: ~80-85%

Performance varies based on data quality and quantity.

## 🎯 Usage

### Run the Application

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Dashboard

#### 1. Risk Prediction Page
- Enter coordinates or city name
- View current weather conditions
- See predicted emergency risk level
- Explore risk zones on interactive map

#### 2. Route Optimization Page
- Enter responder location (start point)
- Enter emergency location (end point)
- View optimal route on map
- See distance and ETA

#### 3. Analytics Page
- View historical emergency trends
- Analyze patterns by time and location
- Explore weather correlations
- Monitor system performance

#### 4. Model Training Page
- Generate synthetic training data
- Train new models
- View model performance metrics
- Analyze feature importance

### Command Line Usage

```python
# Example: Predict risk for a location
from models.predictor import EmergencyPredictor
from api.weather_api import WeatherAPI

predictor = EmergencyPredictor()
weather_api = WeatherAPI()

# Get weather data
weather = weather_api.get_current_weather(40.7128, -74.0060)

# Predict risk
risk = predictor.predict_risk(40.7128, -74.0060, weather)
print(f"Emergency Risk: {risk:.1%}")
```

```python
# Example: Calculate optimal route
from api.routing_api import RoutingAPI

routing_api = RoutingAPI()

start = (40.7589, -73.9851)  # Responder location
end = (40.7128, -74.0060)    # Emergency location

route = routing_api.get_optimal_route(start, end)
print(f"Distance: {route['distance']:.2f} km")
print(f"Duration: {route['duration']:.1f} minutes")
```

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub repository
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Select repository and branch
5. Add environment variables (API keys)
6. Click "Deploy"

### Deploy to Render

1. Create `render.yaml`:

```yaml
services:
  - type: web
    name: emergency-predictor
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: OPENWEATHER_API_KEY
        sync: false
      - key: GOOGLE_MAPS_API_KEY
        sync: false
```

2. Push to GitHub
3. Connect Render to repository
4. Add environment variables
5. Deploy

### Deploy to AWS (Advanced)

Use AWS Elastic Beanstalk or EC2:

1. Install AWS CLI
2. Configure credentials
3. Create Elastic Beanstalk application
4. Deploy using `eb deploy`

See AWS documentation for detailed instructions.

## 📈 Performance Optimization

### Tips for Better Predictions

1. **More Training Data**: Collect real emergency data if available
2. **Feature Engineering**: Add more relevant features (e.g., day of year, holidays)
3. **Advanced Models**: Try Gradient Boosting, Neural Networks, or LSTM
4. **Hyperparameter Tuning**: Use GridSearchCV for optimal parameters
5. **Regular Retraining**: Update model monthly with new data

### API Rate Limiting

- Cache weather data for locations (5-10 minute refresh)
- Batch predictions to reduce API calls
- Use free tier limits wisely
- Consider paid tiers for production

## 🧪 Testing

Run unit tests (if implemented):

```bash
pytest tests/
```

Or test individual components:

```bash
python -m api.weather_api
python -m api.routing_api
python -m models.train_model
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions
- Write unit tests for new features
- Update README for significant changes

## 🐛 Troubleshooting

### Common Issues

**Issue**: Model file not found
```
Solution: Run model training first or generate sample data
```

**Issue**: API errors (weather/routing)
```
Solution: Check API keys in .env file, verify internet connection
```

**Issue**: Import errors
```
Solution: Ensure all dependencies installed: pip install -r requirements.txt
```

**Issue**: Streamlit port already in use
```
Solution: Run on different port: streamlit run main.py --server.port=8502
```

**Issue**: Low model accuracy
```
Solution: Generate more training data or try different model types
```

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 Smart Emergency Response Predictor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📧 Contact & Support

- **Issues**: Open an issue on GitHub
- **Email**: support@emergencypredictor.com
- **Documentation**: [Wiki](https://github.com/Olatomiwa001/Smart-Emergency-Response-Predictor/wiki)

## 🙏 Acknowledgments

- OpenWeather for weather data API
- Google Maps for routing services
- Streamlit for the amazing web framework
- scikit-learn for ML capabilities
- The open-source community

## 🔮 Future Enhancements

- [ ] Mobile app (iOS/Android)
- [ ] Real-time notifications via SMS/Email
- [ ] Integration with 911 dispatch systems
- [ ] Multi-language support
- [ ] Advanced LSTM models for time-series prediction
- [ ] Social media data integration
- [ ] Disaster severity prediction
- [ ] Resource allocation optimization
- [ ] Historical data import from CSV
- [ ] RESTful API for third-party integration

## 📊 Project Status

**Version**: 1.0.0  
**Status**: Active Development  
**Last Updated**: October 2025

---

Made with ❤️ for emergency responders and communities worldwide