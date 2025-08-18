#!/usr/bin/env python3
"""
Setup script for CSRR Faculty Media Tracker
"""

import os
import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✓ Requirements installed successfully")

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = [
        "templates",
        "static",
        "data",
        "reports",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def setup_configuration():
    """Setup configuration file"""
    print("Setting up configuration...")
    if not os.path.exists("config.yaml"):
        print("⚠️  config.yaml not found. Please create it from the template.")
        return False
    
    # Check if configuration needs to be updated
    import yaml
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    if config['email']['sender_email'] == 'your_email@gmail.com':
        print("⚠️  Please update config.yaml with your email credentials")
        return False
    
    print("✓ Configuration file looks good")
    return True

def create_systemd_service():
    """Create systemd service file for Linux deployment"""
    if sys.platform != "linux":
        print("⚠️  Systemd service creation skipped (not on Linux)")
        return
    
    service_content = f"""[Unit]
Description=CSRR Faculty Media Tracker
After=network.target

[Service]
Type=simple
User=csrr
WorkingDirectory={os.getcwd()}
Environment=PATH={os.environ['PATH']}
ExecStart={sys.executable} csrr_media_tracker.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    try:
        with open("/tmp/csrr-media-tracker.service", "w") as f:
            f.write(service_content)
        print("✓ Systemd service file created at /tmp/csrr-media-tracker.service")
        print("  To install: sudo cp /tmp/csrr-media-tracker.service /etc/systemd/system/")
        print("  To enable: sudo systemctl enable csrr-media-tracker")
        print("  To start: sudo systemctl start csrr-media-tracker")
    except Exception as e:
        print(f"⚠️  Could not create systemd service: {e}")

def create_docker_files():
    """Create Docker files for containerized deployment"""
    print("Creating Docker files...")
    
    # Dockerfile
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "csrr_media_tracker.py"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # docker-compose.yml
    compose_content = """version: '3.8'

services:
  csrr-media-tracker:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./data:/app/data
      - ./reports:/app/reports
      - ./logs:/app/logs
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    
    print("✓ Docker files created (Dockerfile, docker-compose.yml)")

def create_launch_script():
    """Create launch script for easy startup"""
    script_content = f"""#!/bin/bash
# CSRR Media Tracker Launch Script

cd "{os.getcwd()}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update requirements
pip install -r requirements.txt

# Run the application
python csrr_media_tracker.py
"""
    
    with open("launch.sh", "w") as f:
        f.write(script_content)
    
    # Make executable
    os.chmod("launch.sh", 0o755)
    print("✓ Launch script created (launch.sh)")

def main():
    """Main setup function"""
    print("🚀 Setting up CSRR Faculty Media Tracker...")
    print("=" * 50)
    
    try:
        install_requirements()
        create_directories()
        config_ok = setup_configuration()
        create_systemd_service()
        create_docker_files()
        create_launch_script()
        
        print("\n" + "=" * 50)
        print("✅ Setup completed successfully!")
        
        if config_ok:
            print("\n📋 Next steps:")
            print("1. Update config.yaml with your email credentials")
            print("2. Run: python csrr_media_tracker.py")
            print("3. Open http://localhost:5000 in your browser")
        else:
            print("\n⚠️  Configuration needed:")
            print("1. Update config.yaml with your email credentials")
            print("2. Then run: python csrr_media_tracker.py")
        
        print("\n📚 Documentation:")
        print("- Web dashboard: http://localhost:5000")
        print("- API endpoints: /api/data, /api/search, /api/report")
        print("- Logs: logs/ directory")
        print("- Reports: reports/ directory")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
