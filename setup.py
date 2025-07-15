#!/usr/bin/env python3
"""
Setup script for Reddit Persona Analyzer
=========================================

This script helps set up the environment and dependencies for the Reddit Persona Analyzer.
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
        return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🔍 Testing imports...")
    
    required_modules = [
        "requests",
        "json",
        "time",
        "re",
        "os",
        "sys",
        "datetime",
        "typing",
        "dataclasses",
        "argparse",
        "urllib.parse",
        "logging"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All required modules imported successfully")
        return True

def run_help_test():
    """Test if the main script runs and shows help"""
    print("\n🧪 Testing main script...")
    
    try:
        result = subprocess.run([
            sys.executable, 
            "reddit_persona_analyzer.py", 
            "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "Reddit profile URL" in result.stdout:
            print("✅ Main script is working correctly")
            return True
        else:
            print("❌ Main script failed basic test")
            print(f"Return code: {result.returncode}")
            print(f"Output: {result.stdout[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error testing main script: {e}")
        return False

def main():
    """Main setup function"""
    print("Reddit Persona Analyzer - Setup")
    print("================================")
    print("Setting up the environment for the Reddit Persona Analyzer...\n")
    
    setup_steps = [
        ("Checking Python version", check_python_version),
        ("Installing requirements", install_requirements),
        ("Testing imports", test_imports),
        ("Testing main script", run_help_test)
    ]
    
    success_count = 0
    
    for step_name, step_function in setup_steps:
        print(f"\n{step_name}...")
        print("-" * len(step_name))
        
        if step_function():
            success_count += 1
        else:
            print(f"\n❌ Setup failed at step: {step_name}")
            print("Please resolve the issues above and run setup again.")
            return False
    
    print(f"\n{'='*50}")
    print("🎉 SETUP COMPLETE!")
    print(f"{'='*50}")
    print("The Reddit Persona Analyzer is ready to use!")
    print("\nQuick start:")
    print("python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/")
    print("\nFor help:")
    print("python reddit_persona_analyzer.py --help")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
