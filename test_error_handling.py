"""
Quick test script for single sample processing with error handling
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.analysis.vm_behavior_analyzer import VMBehaviorAnalyzer
import os

def test_single_sample():
    """Test processing a single sample with error handling"""
    
    analyzer = VMBehaviorAnalyzer()
    
    if not analyzer.vm_available:
        print("❌ VM not available for testing")
        return
    
    # Test with one malware sample
    malware_dir = r"c:\Users\sayha\Final Year Project\Raw_dataset\malignant"
    benign_dir = r"c:\Users\sayha\Final Year Project\Raw_dataset\benign"
    
    # Get first sample from each directory
    test_files = []
    
    if os.path.exists(malware_dir):
        malware_files = list(Path(malware_dir).glob("*.exe"))
        if malware_files:
            test_files.append((str(malware_files[0]), "malware"))
    
    if os.path.exists(benign_dir):
        benign_files = list(Path(benign_dir).glob("*.exe"))
        if benign_files:
            test_files.append((str(benign_files[0]), "benign"))
    
    if not test_files:
        print("❌ No test files found")
        return
    
    print("🧪 Testing Enhanced Error Handling")
    print("=" * 50)
    
    for file_path, file_type in test_files:
        print(f"\n🔬 Testing {file_type}: {os.path.basename(file_path)}")
        
        try:
            result = analyzer.process_sample_for_ml(file_path)
            
            if result.get("success"):
                print(f"✅ SUCCESS: Sample processed successfully")
                features = result.get("ml_features", {})
                print(f"   Features extracted: {len(features)}")
                if "malware_risk_score" in features:
                    print(f"   Risk score: {features['malware_risk_score']:.2f}")
            else:
                print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"💥 EXCEPTION: {e}")
        
        print("-" * 30)
    
    print("\n✅ Error handling test completed!")

if __name__ == "__main__":
    test_single_sample()
