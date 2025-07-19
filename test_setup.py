#!/usr/bin/env python3
"""
Test script to verify the project setup and dependencies.
Run this script to check if everything is configured correctly.
"""

import sys
import subprocess
import importlib
import json
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Need Python 3.8+")
        return False


def check_dependencies():
    """Check if all required dependencies are available."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'meteostat', 
        'pandas',
        'matplotlib',
        'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages


def check_project_files():
    """Check if all required project files exist."""
    print("\n📁 Checking project files...")
    
    required_files = [
        'weather_gui.py',
        'cities.json',
        'pyproject.toml',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} is missing")
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files


def check_cities_data():
    """Check if cities.json is valid."""
    print("\n🌍 Checking cities data...")
    
    try:
        with open('cities.json', 'r', encoding='utf-8') as f:
            cities_data = json.load(f)
        
        if not cities_data:
            print("❌ cities.json is empty")
            return False
        
        # Check if cities have required fields
        for city_name, city_info in cities_data.items():
            if 'lat' not in city_info or 'lon' not in city_info:
                print(f"❌ City {city_name} missing lat/lon coordinates")
                return False
        
        print(f"✅ cities.json is valid with {len(cities_data)} cities")
        return True
        
    except FileNotFoundError:
        print("❌ cities.json not found")
        return False
    except json.JSONDecodeError:
        print("❌ cities.json is not valid JSON")
        return False
    except Exception as e:
        print(f"❌ Error reading cities.json: {e}")
        return False


def check_uv_installation():
    """Check if uv is installed and working."""
    print("\n⚡ Checking uv installation...")
    
    try:
        result = subprocess.run(['uv', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ uv is installed: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ uv is not installed or not in PATH")
        return False
    except subprocess.CalledProcessError:
        print("❌ uv is installed but not working correctly")
        return False


def check_virtual_environment():
    """Check if virtual environment exists and is activated."""
    print("\n🔧 Checking virtual environment...")
    
    venv_path = Path('.venv')
    if venv_path.exists():
        print("✅ Virtual environment (.venv) exists")
        
        # Check if we're in the virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("✅ Virtual environment is activated")
            return True
        else:
            print("⚠️  Virtual environment exists but is not activated")
            return True
    else:
        print("❌ Virtual environment (.venv) not found")
        return False


def run_basic_import_test():
    """Test basic imports from the main application."""
    print("\n🧪 Running basic import test...")
    
    try:
        # Test importing the main modules used in weather_gui.py
        import streamlit
        import meteostat
        import pandas
        import matplotlib.pyplot
        import seaborn
        import json
        import os
        from datetime import datetime
        
        print("✅ All basic imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def main():
    """Run all checks and provide summary."""
    print("🌡️  Temperature Trends Viz - Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Project Files", lambda: check_project_files()[0]),
        ("Cities Data", check_cities_data),
        ("UV Installation", check_uv_installation),
        ("Virtual Environment", check_virtual_environment),
        ("Dependencies", lambda: check_dependencies()[0]),
        ("Basic Imports", run_basic_import_test),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error running {check_name} check: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your setup is ready.")
        print("\nTo start the application, run:")
        print("  uv run streamlit run weather_gui.py")
        print("  or")
        print("  ./run.sh  (Linux/macOS)")
        print("  run.bat   (Windows)")
    else:
        print(f"\n⚠️  {total - passed} checks failed. Please fix the issues above.")
        print("\nFor help, see SETUP.md or README.md")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
