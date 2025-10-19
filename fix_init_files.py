"""
Fix __init__.py files to remove circular imports
"""

from pathlib import Path

def fix_init_files():
    """Create simple __init__.py files without imports"""
    
    init_files = {
        'app/__init__.py': '''"""Application package"""
''',
        'models/__init__.py': '''"""Models package"""
''',
        'api/__init__.py': '''"""API package"""
''',
        'data/__init__.py': '''"""Data package"""
''',
        'logs/__init__.py': '''"""Logs package"""
'''
    }
    
    print("Fixing __init__.py files...\n")
    
    for file_path, content in init_files.items():
        path = Path(file_path)
        if path.exists():
            path.write_text(content)
            print(f"✓ Fixed: {file_path}")
        else:
            print(f"⚠ Not found: {file_path}")
    
    print("\n✓ All __init__.py files fixed!")
    print("\nThese files are now simple and won't cause import errors.")

if __name__ == "__main__":
    fix_init_files()