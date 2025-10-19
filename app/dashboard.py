"""
Dashboard module for Smart Emergency Response Predictor
Provides interactive visualization and prediction interface
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pickle
import os

from models.predictor import EmergencyPredictor
from api.weather_api import WeatherAPI
from api.routing_api import RoutingAPI

def load_model():
    """Load the trained emergency prediction model"""
    model_path = 'models/emergency_model.pkl'
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    else:
        st.warning("Model not found. Please train the model first.")
        return None

def create_risk_map(predictions_df, center_lat=40.7128, center_lon=-74.0060):
    """Create an interactive map with risk zones"""
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Add risk zone markers
    for idx, row in predictions_df.iterrows():
        risk_level = row['risk_probability']
        
        # Determine color based on risk level
        if risk_level >= 0.7:
            color = 'red'
            icon = 'exclamation-triangle'
        elif risk_level >= 0.4:
            color = 'orange'
            icon = 'exclamation-circle'
        else:
            color = 'green'
            icon = 'check-circle'
        
        # Create popup content
        popup_html = f"""
        <div style="width: 200px;">
            <h4>Risk Level: {risk_level:.2%}</h4>
            <p><b>Location:</b> ({row['latitude']:.4f}, {row['longitude']:.4f})</p>
            <p><b>Temperature:</b> {row.get('temperature', 'N/A')}°C</p>
            <p><b>Humidity:</b> {row.get('humidity', 'N/A')}%</p>
        </div>
        """
        
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=color, icon=icon, prefix='fa'),
            tooltip=f"Risk: {risk_level:.1%}"
        ).add_to(m)
        
        # Add circle to represent risk zone
        folium.Circle(
            location=[row['latitude'], row['longitude']],
            radius=risk_level * 500,  # Radius proportional to risk
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.3,
            popup=f"Risk: {risk_level:.1%}"
        ).add_to(m)
    
    return m

def create_route_map(start_coords, end_coords, route_coords=None):
    """Create a map showing the optimal route"""
    # Calculate center point
    center_lat = (start_coords[0] + end_coords[0]) / 2
    center_lon = (start_coords[1] + end_coords[1]) / 2
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12
    )
    
    # Add start marker (responder location)
    folium.Marker(
        location=start_coords,
        popup="Emergency Responder",
        icon=folium.Icon(color='blue', icon='ambulance', prefix='fa'),
        tooltip="Start Location"
    ).add_to(m)
    
    # Add end marker (emergency location)
    folium.Marker(
        location=end_coords,
        popup="Emergency Location",
        icon=folium.Icon(color='red', icon='fire', prefix='fa'),
        tooltip="Emergency Site"
    ).add_to(m)
    
    # Add route if available
    if route_coords:
        folium.PolyLine(
            locations=route_coords,
            color='blue',
            weight=5,
            opacity=0.7,
            tooltip="Optimal Route"
        ).add_to(m)
    else:
        # Simple line between start and end
        folium.PolyLine(
            locations=[start_coords, end_coords],
            color='red',
            weight=3,
            opacity=0.5,
            dash_array='10'
        ).add_to(m)
    
    return m

def run_dashboard():
    """Main dashboard function"""
    
    # Header
    st.markdown('<p class="main-header">🚨 Smart Emergency Response Predictor</p>', unsafe_allow_html=True)
    st.markdown("AI-powered emergency prediction and response optimization system")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", 
                            ["Risk Prediction", "Route Optimization", "Analytics", "Model Training"])
    
    # Initialize APIs
    weather_api = WeatherAPI()
    routing_api = RoutingAPI()
    
    if page == "Risk Prediction":
        show_risk_prediction(weather_api)
    elif page == "Route Optimization":
        show_route_optimization(routing_api)
    elif page == "Analytics":
        show_analytics()
    elif page == "Model Training":
        show_model_training()

def show_risk_prediction(weather_api):
    """Display risk prediction interface"""
    st.header("📍 Emergency Risk Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Location Input")
        
        # Input method selection
        input_method = st.radio("Choose input method:", ["Coordinates", "City Name"])
        
        if input_method == "Coordinates":
            lat = st.number_input("Latitude", value=40.7128, format="%.4f")
            lon = st.number_input("Longitude", value=-74.0060, format="%.4f")
        else:
            city = st.text_input("City Name", value="New York")
            # Simple coordinate mapping (in production, use geocoding API)
            city_coords = {
                "New York": (40.7128, -74.0060),
                "Los Angeles": (34.0522, -118.2437),
                "Chicago": (41.8781, -87.6298),
                "Houston": (29.7604, -95.3698),
                "Phoenix": (33.4484, -112.0740)
            }
            if city in city_coords:
                lat, lon = city_coords[city]
            else:
                st.warning("City not found in database. Using default coordinates.")
                lat, lon = 40.7128, -74.0060
        
        st.write(f"Selected Location: ({lat:.4f}, {lon:.4f})")
        
        # Get weather data
        if st.button("Get Current Weather & Risk"):
            with st.spinner("Fetching weather data..."):
                weather_data = weather_api.get_current_weather(lat, lon)
                
                if weather_data:
                    st.success("Weather data retrieved!")
                    st.json(weather_data)
                    
                    # Make prediction
                    predictor = EmergencyPredictor()
                    risk_score = predictor.predict_risk(lat, lon, weather_data)
                    
                    # Display risk level
                    st.markdown("---")
                    st.subheader("Risk Assessment")
                    
                    if risk_score >= 0.7:
                        st.markdown(f'<p class="risk-high">HIGH RISK: {risk_score:.1%}</p>', unsafe_allow_html=True)
                        st.error("⚠️ High probability of emergency. Recommend increasing patrol.")
                    elif risk_score >= 0.4:
                        st.markdown(f'<p class="risk-medium">MEDIUM RISK: {risk_score:.1%}</p>', unsafe_allow_html=True)
                        st.warning("⚡ Moderate risk level. Monitor conditions.")
                    else:
                        st.markdown(f'<p class="risk-low">LOW RISK: {risk_score:.1%}</p>', unsafe_allow_html=True)
                        st.info("✓ Low risk level. Normal operations.")
    
    with col2:
        st.subheader("Risk Map")
        
        # Generate sample predictions for surrounding area
        num_points = 20
        lat_range = np.random.uniform(lat - 0.05, lat + 0.05, num_points)
        lon_range = np.random.uniform(lon - 0.05, lon + 0.05, num_points)
        
        predictions_data = []
        predictor = EmergencyPredictor()
        
        for i in range(num_points):
            weather_data = weather_api.get_current_weather(lat_range[i], lon_range[i])
            if weather_data:
                risk = predictor.predict_risk(lat_range[i], lon_range[i], weather_data)
                predictions_data.append({
                    'latitude': lat_range[i],
                    'longitude': lon_range[i],
                    'risk_probability': risk,
                    'temperature': weather_data.get('temperature', 0),
                    'humidity': weather_data.get('humidity', 0)
                })
        
        if predictions_data:
            predictions_df = pd.DataFrame(predictions_data)
            risk_map = create_risk_map(predictions_df, lat, lon)
            folium_static(risk_map, width=600, height=500)
        else:
            st.info("Enable weather API to see risk map")

def show_route_optimization(routing_api):
    """Display route optimization interface"""
    st.header("🚑 Emergency Route Optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Responder Location")
        start_lat = st.number_input("Start Latitude", value=40.7589, format="%.4f", key="start_lat")
        start_lon = st.number_input("Start Longitude", value=-73.9851, format="%.4f", key="start_lon")
    
    with col2:
        st.subheader("Emergency Location")
        end_lat = st.number_input("End Latitude", value=40.7128, format="%.4f", key="end_lat")
        end_lon = st.number_input("End Longitude", value=-74.0060, format="%.4f", key="end_lon")
    
    if st.button("Calculate Optimal Route"):
        with st.spinner("Calculating fastest route..."):
            route_data = routing_api.get_optimal_route(
                (start_lat, start_lon),
                (end_lat, end_lon)
            )
            
            if route_data:
                st.success("✓ Route calculated successfully!")
                
                # Display route metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Distance", f"{route_data['distance']:.2f} km")
                with col2:
                    st.metric("Estimated Time", f"{route_data['duration']:.1f} min")
                with col3:
                    st.metric("Route Type", "Fastest")
                
                # Display route map
                route_map = create_route_map(
                    (start_lat, start_lon),
                    (end_lat, end_lon),
                    route_data.get('coordinates')
                )
                folium_static(route_map, width=1000, height=500)
            else:
                st.warning("Route calculation unavailable. Showing direct path.")
                route_map = create_route_map((start_lat, start_lon), (end_lat, end_lon))
                folium_static(route_map, width=1000, height=500)

def show_analytics():
    """Display analytics and historical data"""
    st.header("📊 Emergency Analytics Dashboard")
    
    # Load sample historical data
    data_path = 'data/emergency_data.csv'
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        
        # Time series analysis
        st.subheader("Emergency Trends Over Time")
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            daily_counts = df.groupby(df['timestamp'].dt.date).size().reset_index()
            daily_counts.columns = ['date', 'count']
            
            fig = px.line(daily_counts, x='date', y='count', 
                         title='Daily Emergency Incidents',
                         labels={'count': 'Number of Incidents', 'date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Risk distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Emergency Type Distribution")
            if 'emergency_type' in df.columns:
                type_counts = df['emergency_type'].value_counts()
                fig = px.pie(values=type_counts.values, names=type_counts.index,
                           title='Emergency Types')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Weather Conditions")
            if 'temperature' in df.columns:
                fig = px.histogram(df, x='temperature', nbins=30,
                                 title='Temperature Distribution',
                                 labels={'temperature': 'Temperature (°C)'})
                st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap of incidents by hour and day
        st.subheader("Incident Heatmap")
        if 'timestamp' in df.columns:
            df['hour'] = df['timestamp'].dt.hour
            df['day'] = df['timestamp'].dt.day_name()
            
            heatmap_data = df.groupby(['day', 'hour']).size().reset_index()
            heatmap_data.columns = ['day', 'hour', 'count']
            
            pivot_data = heatmap_data.pivot(index='day', columns='hour', values='count').fillna(0)
            
            fig = px.imshow(pivot_data, 
                          labels=dict(x="Hour of Day", y="Day of Week", color="Incidents"),
                          title="Emergency Incidents by Time",
                          color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No historical data available. Generate sample data in Model Training page.")

def show_model_training():
    """Display model training interface"""
    st.header("🤖 Model Training")
    
    st.subheader("Train Emergency Prediction Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Training Parameters**")
        test_size = st.slider("Test Set Size", 0.1, 0.4, 0.2)
        random_state = st.number_input("Random State", value=42, step=1)
        model_type = st.selectbox("Model Type", 
                                  ["Random Forest", "Gradient Boosting", "Neural Network"])
    
    with col2:
        st.write("**Model Status**")
        model_path = 'models/emergency_model.pkl'
        if os.path.exists(model_path):
            st.success("✓ Trained model exists")
            model_date = datetime.fromtimestamp(os.path.getmtime(model_path))
            st.info(f"Last trained: {model_date.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.warning("⚠ No trained model found")
    
    if st.button("Generate Sample Data"):
        from data.data_generator import generate_sample_data
        with st.spinner("Generating sample emergency data..."):
            generate_sample_data(num_samples=1000)
            st.success("✓ Sample data generated successfully!")
            st.info("Data saved to data/emergency_data.csv")
    
    if st.button("Train Model"):
        from models.train_model import train_emergency_model
        
        with st.spinner("Training model... This may take a few minutes."):
            results = train_emergency_model(
                test_size=test_size,
                random_state=random_state,
                model_type=model_type
            )
            
            if results:
                st.success("✓ Model trained successfully!")
                
                # Display metrics
                st.subheader("Model Performance")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Accuracy", f"{results['accuracy']:.2%}")
                with col2:
                    st.metric("Precision", f"{results['precision']:.2%}")
                with col3:
                    st.metric("Recall", f"{results['recall']:.2%}")
                with col4:
                    st.metric("F1 Score", f"{results['f1_score']:.2%}")
                
                # Feature importance
                if 'feature_importance' in results:
                    st.subheader("Feature Importance")
                    importance_df = pd.DataFrame({
                        'Feature': results['feature_names'],
                        'Importance': results['feature_importance']
                    }).sort_values('Importance', ascending=False)
                    
                    fig = px.bar(importance_df, x='Importance', y='Feature',
                               orientation='h',
                               title='Feature Importance in Prediction')
                    st.plotly_chart(fig, use_container_width=True)