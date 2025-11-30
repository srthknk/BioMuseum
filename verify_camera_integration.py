#!/usr/bin/env python3
"""
Verify Camera Feature Integration
Checks that all components are properly connected
"""

import os
import re
from pathlib import Path

def check_file_exists(path, description):
    """Check if file exists"""
    exists = Path(path).exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {path}")
    return exists

def check_file_content(path, pattern, description):
    """Check if file contains pattern"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            found = re.search(pattern, content, re.IGNORECASE)
            status = "✓" if found else "✗"
            print(f"  {status} {description}")
            return found is not None
    except Exception as e:
        print(f"  ✗ {description} (Error: {e})")
        return False

def main():
    print("\n" + "="*70)
    print("  CAMERA IDENTIFICATION FEATURE - INTEGRATION VERIFICATION")
    print("="*70 + "\n")
    
    checks = []
    
    # 1. Backend endpoint
    print("1. Backend Endpoint (server.py)")
    checks.append(check_file_content(
        "d:\\BioMuseum\\backend\\server.py",
        r"@api_router\.post\(\"/admin/identify-organism\"\)",
        "Endpoint route defined"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\backend\\server.py",
        r"Gemini.*Vision|genai\.GenerativeModel",
        "Gemini Vision AI integration"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\backend\\server.py",
        r"confidence.*<.*40|confidence.*>=.*40",
        "Confidence threshold validation"
    ))
    
    # 2. Frontend component
    print("\n2. Frontend Component (AdminCameraTab)")
    checks.append(check_file_exists(
        "d:\\BioMuseum\\frontend\\src\\components\\AdminCameraTab.jsx",
        "Component file exists"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\frontend\\src\\components\\AdminCameraTab.jsx",
        r"const AdminCameraTab",
        "Component definition"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\frontend\\src\\components\\AdminCameraTab.jsx",
        r"navigator\.mediaDevices\.getUserMedia",
        "Camera API integration"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\frontend\\src\\components\\AdminCameraTab.jsx",
        r"canvasRef\.current\.getContext",
        "Image capture (canvas)"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\frontend\\src\\components\\AdminCameraTab.jsx",
        r"admin/identify-organism|identifyOrganism",
        "API endpoint call"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\frontend\\src\\components\\AdminCameraTab.jsx",
        r"sm:|md:|lg:",
        "Responsive Tailwind classes"
    ))
    
    # 3. App.js integration
    print("\n3. App.js Integration")
    checks.append(check_file_content(
        "d:\\BioMuseum\\frontend\\src\\App.js",
        r"import.*AdminCameraTab",
        "Component import"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\frontend\\src\\App.js",
        r"📸.*Camera",
        "Camera tab navigation"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\frontend\\src\\App.js",
        r"activeView === 'camera'",
        "Camera view rendering"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\frontend\\src\\App.js",
        r"<AdminCameraTab",
        "Component instantiation"
    ))
    checks.append(check_file_content(
        "d:\\BioMuseum\\frontend\\src\\App.js",
        r"onIdentificationSuccess=\{handleApprovalSuccess\}",
        "Callback connection"
    ))
    
    # 4. Tests
    print("\n4. Testing")
    checks.append(check_file_exists(
        "d:\\BioMuseum\\test_camera_feature.py",
        "Test suite"
    ))
    
    # 5. Documentation
    print("\n5. Documentation")
    checks.append(check_file_exists(
        "d:\\BioMuseum\\CAMERA_IDENTIFICATION_FEATURE.md",
        "Feature documentation"
    ))
    
    # Summary
    print("\n" + "="*70)
    total = len(checks)
    passed = sum(checks)
    status = "✓ READY" if passed == total else "⚠ INCOMPLETE"
    print(f"\nSummary: {passed}/{total} checks passed - {status}")
    
    if passed == total:
        print("\n✓ All components are properly integrated!")
        print("\n📋 Next Steps:")
        print("  1. Start backend: python backend/server.py")
        print("  2. Start frontend: npm start (in frontend directory)")
        print("  3. Login as admin")
        print("  4. Click '📸 Camera ID' tab")
        print("  5. Test with a real organism image")
        print("  6. Verify form auto-fills")
        print("  7. Test on mobile device")
        return 0
    else:
        print("\n⚠ Some components are missing!")
        print("   Please review the failed checks above.")
        return 1

if __name__ == "__main__":
    exit(main())
