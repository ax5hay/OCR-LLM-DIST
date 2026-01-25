#!/usr/bin/env python3
"""
Final verification script for OCR-LLM project transformation.
Run this to verify all files are in place.
"""

import os
from pathlib import Pathib import Pathib import Pathib import Path

def verify_transformation():
    """Verify that all expected files exist."""
    
    project_root = Path(__file__).parent
    
    # Expected files
    expected_files = {
        'Documentation': [
            'README.md',
            'QUICKSTART.md', 
            'API.md',
            'PROJECT_STRUCTURE.md',
            'CONTRIBUTING.md',
            'DOCUMENTATION_INDEX.md',
            'CHANGELOG.md',
            'TRANSFORMATION_SUMMARY.md',
            'GET_STARTED.md',
            'COMPLETION_REPORT.md',
            'MASTER_CHECKLIST.md',
        ],
        'Configuration': [
            'config.py',
            '.env.example',
            '.gitignore',
            'setup.py',
            'pytest.ini',
            '.bandit',
        ],
        'Deployment': [
            'Dockerfile',
            'docker-compose.yml',
            'setup.sh',
            'setup.bat',
        ],
        'Dependencies': [
            'requirements.txt',
            'requirements-dev.txt',
        ],
        'Python Code': [
            'app.py',
            'run_app.py',
            'services/ollama_service.py',
            'services/model_service.py',
            'services/__init__.py',
            'utils/file_utils.py',
            'utils/logging_config.py',
            'utils/__init__.py',
        ],
    }
    
    results = {}
    total_found = 0
    total_expected = 0
    
    for category, files in expected_files.items():
        results[category] = {}
        for filename in files:
            filepath = project_root / filename
            exists = filepath.exists()
            results[category][filename] = exists
            total_expected += 1
            if exists:
                total_found += 1
    
    # Print results
    print("\n🔍 TRANSFORMATION VERIFICATION REPORT")
    print("=" * 60)
    
    for category, files in results.items():
        print(f"\n📁 {category}:")
        found = sum(1 for v in files.values() if v)
        total = len(files)
        status = "✅" if found == total else "⚠️"
        print(f"   {status} {found}/{total} files present")
        
        for filename, exists in files.items():
            symbol = "✅" if exists else "❌"
            print(f"      {symbol} {filename}")
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {total_found}/{total_expected} files present")
    
    if total_found == total_expected:
        print("\n🎉 TRANSFORMATION COMPLETE!")
        print("✨ All files are in place and ready for production!")
        return True
    else:
        print(f"\n⚠️  {total_expected - total_found} files are missing")
        return False

if __name__ == "__main__":
    success = verify_transformation()
    exit(0 if success else 1)
