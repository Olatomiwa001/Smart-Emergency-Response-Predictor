"""
Smart Emergency Response Predictor - Main Entry Point
This is the main application file that runs the Streamlit dashboard.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add project directories to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.dashboard import run_dashboard

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Smart Emergency Response Predictor",
        page_icon="🚨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better UI
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #FF4B4B;
            text-align: center;
            padding: 1rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .risk-high {
            color: #FF4B4B;
            font-weight: bold;
        }
        .risk-medium {
            color: #FFA500;
            font-weight: bold;
        }
        .risk-low {
            color: #00CC00;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Run the dashboard
    run_dashboard()

if __name__ == "__main__":
    main()