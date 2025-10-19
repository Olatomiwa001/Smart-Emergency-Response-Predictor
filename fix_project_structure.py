"""
Automatic Project Structure Fixer
This script reorganizes files into the correct folder structure
"""

import os
import shutil
from pathlib import Path

def print_step(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")

def create_folders():
    """Create necessary folders"""
    folders = ['app', 'models', 'api', 'data', 'logs']
    
    print_step("Creating Folders")
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        print(f"✓ Created/verified: {folder}/")
    
    return folders

def create_init_files(folders):
    """Create __init__.py files in each folder"""
    print_step("Creating __init__.py Files")
    
    for folder in folders:
        init_path = Path(folder) / '__init__.py'
        if not init_path.exists():
            init_path.write_text(f'"""{folder.capitalize()} package"""\n')
            print(f"✓ Created: {init_path}")
        else:
            print(f"  Exists: {init_path}")

def reorganize_files():
    """Move and rename files to correct locations"""
    print_step("Reorganizing Files")
    
    # Define file mappings: {current_name: (target_folder, target_name)}
    file_mappings = {
        # Data files
        'data.data_generator.py': ('data', 'data_generator.py'),
        'data_generator.py': ('data', 'data_generator.py'),
        
        # API files
        'Weather_api.py': ('api', 'weather_api.py'),
        'weather_api.py': ('api', 'weather_api.py'),
        'routing_api.py': ('api', 'routing_api.py'),
        'api.routing_api.py': ('api', 'routing_api.py'),
        'api.weather_api.py': ('api', 'weather_api.py'),
        
        # Model files
        'train_model.py': ('models', 'train_model.py'),
        'models.train_model.py': ('models', 'train_model.py'),
        'predictor.py': ('models', 'predictor.py'),
        'models.predictor.py': ('models', 'predictor.py'),
        
        # App files
        'dashboard.py': ('app', 'dashboard.py'),
        'app.dashboard.py': ('app', 'dashboard.py'),
    }
    
    for source_file, (target_folder, target_name) in file_mappings.items():
        source_path = Path(source_file)
        
        if source_path.exists():
            target_path = Path(target_folder) / target_name
            
            # Don't move if already in correct location
            if source_path.resolve() == target_path.resolve():
                print(f"  Already correct: {target_path}")
                continue
            
            # Check if target already exists
            if target_path.exists():
                response = input(f"\n{target_path} exists. Overwrite? (y/n): ")
                if response.lower() != 'y':
                    print(f"  Skipped: {source_file}")
                    continue
            
            # Move and rename
            shutil.move(str(source_path), str(target_path))
            print(f"✓ Moved: {source_file} → {target_path}")

def create_missing_files():
    """Create any missing essential files"""
    print_step("Checking for Missing Files")
    
    essential_files = {
        'main.py': True,
        'requirements.txt': True,
        '.env.example': True,
        'README.md': True,
        '.gitignore': True,
        'models/predictor.py': False,
        'app/dashboard.py': False,
        'api/weather_api.py': False,
        'api/routing_api.py': False,
        'data/data_generator.py': False,
    }
    
    missing = []
    for file_path, is_essential in essential_files.items():
        if not Path(file_path).exists():
            if is_essential:
                missing.append(file_path)
                print(f"⚠ Missing essential file: {file_path}")
            else:
                print(f"  Missing optional file: {file_path}")
    
    if missing:
        print(f"\n⚠ {len(missing)} essential files are missing.")
        print("  Please create them or copy from the artifacts.")
    else:
        print("\n✓ All essential files present!")

def verify_structure():
    """Verify the final structure"""
    print_step("Verifying Project Structure")
    
    expected_structure = {
        'app': ['__init__.py', 'dashboard.py'],
        'models': ['__init__.py', 'predictor.py', 'train_model.py'],
        'api': ['__init__.py', 'weather_api.py', 'routing_api.py'],
        'data': ['__init__.py', 'data_generator.py'],
    }
    
    all_good = True
    
    for folder, files in expected_structure.items():
        folder_path = Path(folder)
        print(f"\n{folder}/")
        
        if not folder_path.exists():
            print(f"  ❌ Folder doesn't exist!")
            all_good = False
            continue
        
        for file in files:
            file_path = folder_path / file
            if file_path.exists():
                print(f"  ✓ {file}")
            else:
                print(f"  ❌ Missing: {file}")
                all_good = False
    
    return all_good

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("  SMART EMERGENCY PREDICTOR - STRUCTURE FIXER")
    print("="*60)
    print("\nThis script will reorganize your project files into")
    print("the correct folder structure.")
    print("\nCurrent directory:", os.getcwd())
    
    response = input("\nContinue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    # Step 1: Create folders
    folders = create_folders()
    
    # Step 2: Create __init__.py files
    create_init_files(folders)
    
    # Step 3: Reorganize files
    reorganize_files()
    
    # Step 4: Check for missing files
    create_missing_files()
    
    # Step 5: Verify structure
    structure_ok = verify_structure()
    
    # Final message
    print_step("COMPLETE!")
    
    if structure_ok:
        print("\n✓ Project structure is now correct!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Generate data: python -m data.data_generator")
        print("3. Train model: python -m models.train_model")
        print("4. Run app: streamlit run main.py")
    else:
        print("\n⚠ Some files are still missing.")
        print("Please copy the missing files from the artifacts I provided.")
        print("\nThen try running this script again.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please fix the error and try again.")