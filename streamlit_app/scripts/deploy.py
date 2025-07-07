#!/usr/bin/env python3
"""
Hotel Dashboard Deployment Script
Helps users deploy the dashboard to Streamlit Cloud
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'src/hotel_dashboard.py',
        'data/hotel_bookings.csv',
        'requirements.txt',
        'README.md',
        'app.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        import sklearn
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_dashboard():
    """Test if the dashboard runs locally"""
    try:
        print("🚀 Testing dashboard code syntax...")
        # Check if the main dashboard file can be imported
        import importlib.util
        spec = importlib.util.spec_from_file_location("hotel_dashboard", "src/hotel_dashboard.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("✅ Dashboard code is valid")
        return True
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def create_streamlit_config():
    """Create .streamlit/config.toml for deployment"""
    config_dir = Path('.streamlit')
    config_dir.mkdir(exist_ok=True)
    
    config_content = """[server]
headless = true
enableCORS = false
port = 8501

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
    
    config_file = config_dir / 'config.toml'
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print("✅ Created Streamlit configuration")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Data (if large)
*.csv
*.xlsx
*.json

# Logs
*.log
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Created .gitignore file")

def deployment_instructions():
    """Print deployment instructions"""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    
    print("\n📋 To deploy to Streamlit Cloud:")
    print("1. Push your code to GitHub:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git branch -M main")
    print("   git remote add origin <your-github-repo-url>")
    print("   git push -u origin main")
    
    print("\n2. Go to https://share.streamlit.io/")
    print("3. Sign in with GitHub")
    print("4. Click 'New app'")
    print("5. Select your repository")
    print("6. Set the path to: app.py")
    print("7. Click 'Deploy!'")
    
    print("\n📋 To run locally:")
    print("streamlit run app.py")
    
    print("\n📋 To run with custom port:")
    print("streamlit run app.py --server.port 8502")
    
    print("\n" + "="*60)

def main():
    """Main deployment script"""
    print("🏨 Hotel Dashboard Deployment Script")
    print("="*40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Test dashboard
    if not test_dashboard():
        sys.exit(1)
    
    # Create configuration files
    create_streamlit_config()
    create_gitignore()
    
    # Print deployment instructions
    deployment_instructions()
    
    print("\n✅ Deployment preparation complete!")
    print("🎉 Your dashboard is ready to deploy!")

if __name__ == "__main__":
    main() 