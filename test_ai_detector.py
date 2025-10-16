"""
AI Malware Detection System Test with Retrained Model
Tests the newly retrained model that uses all 37 features
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.detection.ai_malware_tester import MalwareDetector

def test_retrained_model():
    """Test the retrained AI detector with known malware and benign samples"""
    
    print("🤖 AI Malware Detection System Test (Retrained Model)")
    print("=" * 60)
    print("📈 Model Info: 245 samples, 37 features, 98% accuracy, 100% malware detection")
    print()
    
    # Initialize the detector
    detector = MalwareDetector()
    
    # Test files - including the one that was misclassified before
    test_files = [
        {
            "path": r"c:\Users\sayha\Final Year Project\Raw_dataset\benign\calc.exe",
            "expected": "BENIGN",
            "description": "Windows Calculator (Benign)"
        },
        {
            "path": r"c:\Users\sayha\Final Year Project\Raw_dataset\malignant\fake_dropper copy 2.exe",
            "expected": "MALWARE", 
            "description": "Fake Dropper (Malware - previously misclassified)"
        },
        {
            "path": r"c:\Users\sayha\Final Year Project\Raw_dataset\malignant\fake_dropper copy 3.exe",
            "expected": "MALWARE",
            "description": "Another Fake Dropper (Malware)"
        }
    ]
    
    correct_predictions = 0
    total_tests = 0
    
    for test_case in test_files:
        test_file = test_case["path"]
        expected = test_case["expected"]
        description = test_case["description"]
        
        if Path(test_file).exists():
            total_tests += 1
            print(f"🔬 Testing: {description}")
            print(f"   File: {Path(test_file).name}")
            print(f"   Expected: {expected}")
            print("-" * 50)
            
            result = detector.test_file(test_file, save_report=False)
            
            if result["success"]:
                prediction = result["prediction"]
                risk_score = result["risk_score"]
                
                # Check if prediction is correct
                is_correct = prediction == expected
                if is_correct:
                    correct_predictions += 1
                    status_icon = "✅"
                else:
                    status_icon = "❌"
                
                if prediction == "MALWARE":
                    print(f"{status_icon} RESULT: 🚨 {prediction} (Risk: {risk_score:.1f}%)")
                else:
                    print(f"{status_icon} RESULT: ✅ {prediction} (Risk: {risk_score:.1f}%)")
                
                if not is_correct:
                    print(f"   ⚠️  INCORRECT! Expected {expected}, got {prediction}")
                else:
                    print(f"   ✅ CORRECT! Model properly classified this sample")
                    
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                
            print()
        else:
            print(f"⚠️  File not found: {test_file}")
            print()
    
    # Show final results
    print("🎯 FINAL RESULTS")
    print("=" * 60)
    print(f"Total tests: {total_tests}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Accuracy: {(correct_predictions/total_tests)*100:.1f}%" if total_tests > 0 else "No tests completed")
    
    if correct_predictions == total_tests and total_tests > 0:
        print("� PERFECT! All samples correctly classified!")
        print("✅ The retrained model is working properly!")
    elif correct_predictions > 0:
        print("⚠️  Some samples were misclassified - model may need further tuning")
    else:
        print("❌ All samples were misclassified - check model training")

if __name__ == "__main__":
    test_retrained_model()
