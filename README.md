# AI-Driven Malware Sandboxing System

An automated malware behavior analysis system that combines Cuckoo Sandbox with machine learning for enhanced threat detection.

## 🎯 Project Overview

This system implements an AI-driven approach to malware analysis by:
- Executing malware samples in a controlled Cuckoo Sandbox environment
- Extracting behavioral features from system calls, network activity, and file operations
- Using machine learning models (SVM, Random Forest) to classify malware vs benign software
- Providing automated threat analysis reports for cybersecurity professionals

## 🏗️ Project Structure

```
AI-Malware-Sandbox/
├── src/                          # Source code
│   ├── data_processing/          # Data handling and preprocessing
│   ├── feature_extraction/       # Feature engineering modules
│   ├── ml_models/               # Machine learning implementations
│   ├── cuckoo_integration/      # Cuckoo Sandbox API integration
│   └── utils/                   # Utility functions and helpers
├── data/                        # Dataset storage
│   ├── raw/                     # Raw malware/benign samples
│   ├── processed/               # Processed datasets
│   └── features/                # Extracted feature vectors
├── models/                      # Trained ML models
│   ├── trained/                 # Final trained models
│   └── checkpoints/             # Model checkpoints
├── reports/                     # Analysis reports and results
│   ├── analysis/                # Individual sample reports
│   └── performance/             # Model performance reports
├── config/                      # Configuration files
├── logs/                        # System and analysis logs
├── notebooks/                   # Jupyter notebooks for analysis
└── temp/                        # Temporary files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- VirtualBox or VMware
- Windows 7 VM (for Cuckoo Sandbox)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AI-Malware-Sandbox
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your specific settings
   ```

### Cuckoo Sandbox Setup

1. **Install Cuckoo Sandbox:**
   ```bash
   pip install cuckoo
   ```

2. **Initialize Cuckoo:**
   ```bash
   cuckoo init
   ```

3. **Configure VM:**
   - Set up Windows 7 VM in VirtualBox
   - Install required software and Python agent
   - Configure networking and snapshots

4. **Start Cuckoo services:**
   ```bash
   # Terminal 1: Start Cuckoo daemon
   cuckoo
   
   # Terminal 2: Start web interface
   cuckoo web runserver
   
   # Terminal 3: Start API server
   cuckoo api
   ```

## 📊 Usage

### Basic Analysis Workflow

1. **Submit samples for analysis:**
   ```python
   from src.cuckoo_integration import CuckooSubmitter
   
   submitter = CuckooSubmitter()
   task_id = submitter.submit_file("path/to/malware.exe")
   ```

2. **Extract features:**
   ```python
   from src.feature_extraction import FeatureExtractor
   
   extractor = FeatureExtractor()
   features = extractor.extract_from_report(task_id)
   ```

3. **Classify sample:**
   ```python
   from src.ml_models import MalwareClassifier
   
   classifier = MalwareClassifier()
   prediction = classifier.predict(features)
   ```

### Batch Processing

```python
from src.data_processing import BatchProcessor

processor = BatchProcessor()
processor.process_directory("data/raw/malignant/")
```

## 🔧 Configuration

Edit `config/config.yaml` to customize:

- Cuckoo Sandbox connection settings
- Machine learning parameters
- Feature extraction options
- Dataset paths and splits
- Logging configuration

## 📈 Model Performance

The system uses multiple evaluation metrics:

- **Accuracy**: Overall classification correctness
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)  
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under the ROC curve

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
flake8 src/
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes in appropriate module
3. Add tests for new functionality
4. Update documentation
5. Submit pull request

## 📁 Dataset Organization

```
Raw_dataset/
├── malignant/          # Malware samples
│   ├── *.exe          # Executable files
│   └── *.dll          # Dynamic link libraries
└── benign/            # Benign software
    ├── *.exe          # Clean executable files
    └── *.dll          # Clean libraries
```

## 🔒 Security Considerations

- **Isolated Environment**: All malware analysis is performed in isolated VMs
- **Network Isolation**: Sandbox VMs have controlled network access
- **Safe Handling**: Automated sample handling minimizes exposure risk
- **Access Control**: Restricted access to malware samples and analysis tools

## 🐛 Troubleshooting

### Common Issues

1. **Cuckoo Connection Failed:**
   - Check if Cuckoo services are running
   - Verify API endpoint in configuration
   - Check firewall settings

2. **VM Analysis Timeout:**
   - Increase timeout in config.yaml
   - Check VM resource allocation
   - Verify VM snapshot is clean

3. **Feature Extraction Errors:**
   - Ensure Cuckoo reports are complete
   - Check file permissions
   - Verify JSON report format

### Getting Help

- Check the logs in `logs/` directory
- Review configuration settings
- Consult Cuckoo Sandbox documentation
- Submit issues with detailed error messages

## 📚 References

- [Cuckoo Sandbox Documentation](https://cuckoo.readthedocs.io/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Malware Analysis Techniques](https://www.sans.org/white-papers/)

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dr. Vazeerudeen Hameed (Project Supervisor)
- Asia Pacific University of Technology and Innovation
- Cuckoo Sandbox Community
- Open Source Security Community

---

**Author:** Sayhan Basharat  
**Project:** Final Year Project - B.Sc. (Hons) Computer Science (Cyber Security)  
**Institution:** Asia Pacific University of Technology and Innovation  
**Year:** 2024-2025
