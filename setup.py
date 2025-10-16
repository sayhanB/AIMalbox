#!/usr/bin/env python3
"""
AI-Driven Malware Sandboxing System - Setup Script
Author: Sayhan Basharat
Description: Initial setup and configuration script for the malware analysis system
"""

import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path
import yaml

def setup_logging():
    """Setup basic logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('setup.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        raise RuntimeError("Python 3.8 or higher is required")
    return True

def create_virtual_environment(venv_path="venv"):
    """Create Python virtual environment"""
    logger = logging.getLogger(__name__)
    
    if os.path.exists(venv_path):
        logger.info(f"Virtual environment already exists at {venv_path}")
        return True
    
    try:
        logger.info("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        logger.info("Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create virtual environment: {e}")
        return False

def install_requirements():
    """Install required Python packages"""
    logger = logging.getLogger(__name__)
    
    # Determine the correct pip executable based on OS
    if os.name == 'nt':  # Windows
        pip_executable = "venv\\Scripts\\pip.exe"
        python_executable = "venv\\Scripts\\python.exe"
    else:  # Unix-like systems
        pip_executable = "venv/bin/pip"
        python_executable = "venv/bin/python"
    
    if not os.path.exists(pip_executable):
        logger.error("Virtual environment not found or not activated")
        return False
    
    try:
        logger.info("Installing required packages...")
        subprocess.run([
            pip_executable, "install", "--upgrade", "pip"
        ], check=True)
        
        subprocess.run([
            pip_executable, "install", "-r", "requirements.txt"
        ], check=True)
        
        logger.info("All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install packages: {e}")
        return False

def create_project_structure():
    """Create necessary project directories"""
    logger = logging.getLogger(__name__)
    
    directories = [
        "src/data_processing",
        "src/feature_extraction", 
        "src/ml_models",
        "src/cuckoo_integration",
        "src/utils",
        "data/raw",
        "data/processed",
        "data/features",
        "models/trained",
        "models/checkpoints",
        "reports/analysis",
        "reports/performance",
        "logs/system",
        "logs/analysis",
        "temp",
        "notebooks"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    # Create __init__.py files for Python packages
    init_files = [
        "src/__init__.py",
        "src/data_processing/__init__.py",
        "src/feature_extraction/__init__.py",
        "src/ml_models/__init__.py",
        "src/cuckoo_integration/__init__.py",
        "src/utils/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch(exist_ok=True)
        logger.info(f"Created __init__.py: {init_file}")

def setup_configuration():
    """Setup configuration files"""
    logger = logging.getLogger(__name__)
    
    # Copy environment file if it doesn't exist
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            logger.info("Created .env file from .env.example")
        else:
            logger.warning(".env.example not found")
    
    # Validate configuration file
    try:
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        logger.info("Configuration file validated successfully")
    except Exception as e:
        logger.error(f"Configuration file validation failed: {e}")
        return False
    
    return True

def check_system_requirements():
    """Check system requirements and dependencies"""
    logger = logging.getLogger(__name__)
    
    requirements = {
        "VirtualBox": ["VBoxManage", "--version"],
        "Git": ["git", "--version"]
    }
    
    missing_requirements = []
    
    for req_name, command in requirements.items():
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✓ {req_name} is installed")
            else:
                missing_requirements.append(req_name)
        except FileNotFoundError:
            missing_requirements.append(req_name)
            logger.warning(f"✗ {req_name} is not installed")
    
    if missing_requirements:
        logger.warning(f"Missing requirements: {', '.join(missing_requirements)}")
        logger.info("Please install the missing software before proceeding with Cuckoo Sandbox setup")
    
    return len(missing_requirements) == 0

def display_next_steps():
    """Display next steps for the user"""
    logger = logging.getLogger(__name__)
    
    next_steps = """
    
    ═══════════════════════════════════════════════════════════════════
    🎉 SETUP COMPLETED SUCCESSFULLY!
    ═══════════════════════════════════════════════════════════════════
    
    NEXT STEPS:
    
    1. Activate Virtual Environment:
       Windows: venv\\Scripts\\activate
       Linux/Mac: source venv/bin/activate
    
    2. Configure Environment Variables:
       - Edit .env file with your specific settings
       - Update Cuckoo Sandbox connection details
    
    3. Install Cuckoo Sandbox:
       - Follow the official Cuckoo installation guide
       - Configure Windows 7 VM for malware analysis
       - Test Cuckoo API connectivity
    
    4. Prepare Dataset:
       - Organize malware samples in data/raw/malignant/
       - Organize benign samples in data/raw/benign/
       - Ensure proper file permissions
    
    5. Run Initial Tests:
       - python src/utils/system_check.py
       - python src/cuckoo_integration/test_connection.py
    
    6. Start Development:
       - Review config/config.yaml settings
       - Begin with Phase 2: Data Collection & Feature Engineering
    
    ═══════════════════════════════════════════════════════════════════
    📖 Documentation: Check the README.md file for detailed instructions
    🐛 Issues: Report problems in the project repository
    ═══════════════════════════════════════════════════════════════════
    """
    
    logger.info(next_steps)

def main():
    """Main setup function"""
    logger = setup_logging()
    logger.info("Starting AI-Driven Malware Sandboxing System setup...")
    
    try:
        # Check Python version
        check_python_version()
        logger.info("✓ Python version check passed")
        
        # Create virtual environment
        if create_virtual_environment():
            logger.info("✓ Virtual environment setup completed")
        else:
            logger.error("✗ Virtual environment setup failed")
            return False
        
        # Install requirements
        if install_requirements():
            logger.info("✓ Package installation completed")
        else:
            logger.error("✗ Package installation failed")
            return False
        
        # Create project structure
        create_project_structure()
        logger.info("✓ Project structure created")
        
        # Setup configuration
        if setup_configuration():
            logger.info("✓ Configuration setup completed")
        else:
            logger.error("✗ Configuration setup failed")
            return False
        
        # Check system requirements
        check_system_requirements()
        
        # Display next steps
        display_next_steps()
        
        logger.info("Setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
