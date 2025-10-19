"""
Automated Setup Script for Smart Emergency Response Predictor
Handles initial project setup, data generation, and model training
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(step_num, text):
    """Print step information"""
    print(f"\n[Step {step_num}] {text}")
    print("-" * 70)

def check_python_version():
    """Check if Python version is 3.8+"""
    print_step(1, "Checking Python Version")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✓ Python version: {sys.version.split()[0]}")

def create_directories():
    """Create necessary project directories"""
    print_step(2, "Creating Project Directories")
    
    directories = [
        'data',
        'models',
        'api',
        'app',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created/verified directory: {directory}/")
    
    # Create __init__.py files
    init_files = [
        'data/__init__.py',
        'models/__init__.py',
        'api/__init__.py',
        'app/__init__.py'
    ]
    
    for init_file in init_files:
        Path(init_file).touch(exist_ok=True)
    
    print("✓ All directories created successfully")

def install_dependencies():
    """Install required Python packages"""
    print_step(3, "Installing Dependencies")
    
    print("Installing packages from requirements.txt...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("\n✓ All dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("\n❌ Error installing dependencies")
        print("   Try manual installation: pip install -r requirements.txt")
        sys.exit(1)

def setup_env_file():
    """Create .env file from template"""
    print_step(4, "Setting Up Environment Variables")
    
    if os.path.exists('.env'):
        print("⚠ .env file already exists, skipping creation")
        return
    
    if os.path.exists('.env.example'):
        with open('.env.example', 'r') as src:
            content = src.read()
        
        with open('.env', 'w') as dst:
            dst.write(content)
        
        print("✓ Created .env file from template")
        print("  → Edit .env to add your API keys (optional)")
    else:
        print("⚠ .env.example not found, skipping")

def generate_data():
    """Generate sample training data"""
    print_step(5, "Generating Sample Data")
    
    try:
        from data.data_generator import generate_sample_data
        
        data_path = 'data/emergency_data.csv'
        
        if os.path.exists(data_path):
            response = input(f"\n{data_path} already exists. Overwrite? (y/n): ")
            if response.lower() != 'y':
                print("Skipping data generation")
                return
        
        print("\nGenerating 1000 sample emergency records...")
        generate_sample_data(num_samples=1000, output_path=data_path)
        print("\n✓ Sample data generated successfully")
        
    except Exception as e:
        print(f"\n❌ Error generating data: {e}")
        print("   You can generate data later by running:")