"""
Check if all required files exist and are in the correct locations
"""

from pathlib import Path
import os

def check_files():
    """Check all required files"""
    
    required_files = {
        'Main files': [
            'main.py',
            'requirements.txt',
        ],
        'app/': [
            'app/__init__.py',
            'app/dashboard.py',
        ],
        'models/': [
            'models/__init__.py',
            'models/predictor.py',
            'models/train_model.py',
        ],
        'api/': [
            'api/__init__.py',
            'api/weather_api.py',
            'api/routing_api.py',
        ],
        'data/': [
            'data/__init__.py',
            'data/data_generator.py',
        ],
    }
    
    print("Checking required files...\n")
    print("="*60)
    
    all_present = True
    missing_files = []
    
    for category, files in required_files.items():
        print(f"\n{category}")
        print("-"*60)
        for file_path in files:
            path = Path(file_path)
            if path.exists():
                size = path.stat().st_size
                print(f"  ✓ {file_path} ({size} bytes)")
            else:
                print(f"  ❌ MISSING: {file_path}")
                all_present = False
                missing_files.append(file_path)
    
    print("\n" + "="*60)
    
    if all_present:
        print("\n✓ All required files are present!")
    else:
        print(f"\n❌ {len(missing_files)} file(s) missing:")
        for f in missing_files:
            print(f"   - {f}")
        
        print("\nFiles that need to be created:")
        for f in missing_files:
            if 'weather_api.py' in f:
                print(f"\n{f}: Copy from artifact 'api/weather_api.py - Weather API Integration'")
            elif 'routing_api.py' in f:
                print(f"\n{f}: Copy from artifact 'api/routing_api.py - Routing API Integration'")
            elif 'dashboard.py' in f:
                print(f"\n{f}: Copy from artifact 'app/dashboard.py - Interactive Dashboard'")
            elif 'predictor.py' in f:
                print(f"\n{f}: Copy from artifact 'models/predictor.py - Emergency Predictor'")
            elif 'train_model.py' in f:
                print(f"\n{f}: Copy from artifact 'models/train_model.py - Model Training'")
    
    # Check for files in wrong locations
    print("\n" + "="*60)
    print("Checking for misplaced files...")
    print("="*60)
    
    root_files = [f for f in os.listdir('.') if f.endswith('.py') and f not in ['main.py', 'setup.py', 'fix_project_structure.py', 'fix_init_files.py', 'check_files.py', 'create_missing_files.py']]
    
    if root_files:
        print("\n⚠ Found Python files in root that should be in folders:")
        for f in root_files:
            print(f"   - {f}")
            if 'weather' in f.lower():
                print(f"     → Should be in api/ folder")
            elif 'routing' in f.lower():
                print(f"     → Should be in api/ folder")
            elif 'dashboard' in f.lower():
                print(f"     → Should be in app/ folder")
            elif 'predictor' in f.lower():
                print(f"     → Should be in models/ folder")
            elif 'train' in f.lower():
                print(f"     → Should be in models/ folder")
            elif 'data' in f.lower() and 'generator' in f.lower():
                print(f"     → Should be in data/ folder")
    else:
        print("\n✓ No misplaced files found")
    
    return all_present

if __name__ == "__main__":
    check_files()