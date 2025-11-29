#!/usr/bin/env python3
"""
Comprehensive test for AI Organism Auto-Fill Feature
Tests the Gemini API integration with the BioMuseum backend
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8000"
AI_ENDPOINT = f"{BACKEND_URL}/api/admin/organisms/ai-complete"

# Test organisms
TEST_ORGANISMS = [
    "Lion",
    "Honeybee",
    "African Elephant",
    "Blue Whale",
    "Red Panda"
]

def test_ai_endpoint(organism_name):
    """Test the AI endpoint with a single organism"""
    print(f"\n{'='*70}")
    print(f"Testing: {organism_name}")
    print(f"{'='*70}")
    
    payload = {"organism_name": organism_name}
    
    try:
        response = requests.post(AI_ENDPOINT, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                organism_data = data.get("data", {})
                print(f"[PASS] AI successfully generated data for {organism_name}")
                print(f"\n  Name: {organism_data.get('name')}")
                print(f"  Scientific Name: {organism_data.get('scientific_name')}")
                print(f"  Kingdom: {organism_data.get('classification', {}).get('kingdom')}")
                print(f"  Phylum: {organism_data.get('classification', {}).get('phylum')}")
                print(f"  Class: {organism_data.get('classification', {}).get('class')}")
                print(f"  Source: {data.get('source')}")
                return True
            else:
                print(f"[FAIL] Response indicates failure: {data.get('message')}")
                return False
        else:
            print(f"[FAIL] HTTP {response.status_code}: {response.json()}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"[FAIL] Request timeout (60s)")
        return False
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] Connection error - Backend not responding")
        return False
    except Exception as e:
        print(f"[FAIL] Exception: {e}")
        return False

def test_ai_response_validation(organism_name):
    """Validate that AI response has all required fields"""
    print(f"\nValidating response structure for {organism_name}...")
    
    payload = {"organism_name": organism_name}
    response = requests.post(AI_ENDPOINT, json=payload, timeout=60)
    
    if response.status_code != 200:
        print(f"[FAIL] Invalid HTTP status: {response.status_code}")
        return False
    
    data = response.json()
    required_fields = ["success", "data", "source"]
    
    for field in required_fields:
        if field not in data:
            print(f"[FAIL] Missing top-level field: {field}")
            return False
    
    organism_data = data.get("data", {})
    required_data_fields = ["name", "scientific_name", "classification", 
                           "morphology", "physiology", "general_description"]
    
    for field in required_data_fields:
        if field not in organism_data:
            print(f"[FAIL] Missing data field: {field}")
            return False
    
    # Validate classification
    classification = organism_data.get("classification", {})
    required_classifications = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
    
    for field in required_classifications:
        if field not in classification:
            print(f"[FAIL] Missing classification field: {field}")
            return False
    
    print(f"[PASS] Response structure is valid")
    return True

def main():
    print("\n" + "="*70)
    print("AI ORGANISM AUTO-FILL FEATURE - COMPREHENSIVE TEST")
    print("="*70)
    
    # Check if backend is running
    print("\nChecking backend connectivity...")
    try:
        response = requests.get(f"{BACKEND_URL}/health" if False else f"{BACKEND_URL}/", timeout=5)
        print("[INFO] Backend is responsive")
    except:
        print("[WARN] Backend connection test skipped (health endpoint not available)")
    
    # Run tests
    passed = 0
    failed = 0
    
    print(f"\nTesting with {len(TEST_ORGANISMS)} organisms...")
    
    for i, organism in enumerate(TEST_ORGANISMS, 1):
        print(f"\n[{i}/{len(TEST_ORGANISMS)}] {organism}")
        
        # Test basic endpoint
        if test_ai_endpoint(organism):
            passed += 1
            
            # Test response validation
            time.sleep(1)  # Rate limiting for API
            if test_ai_response_validation(organism):
                print(f"[PASS] All validations passed for {organism}")
            else:
                print(f"[FAIL] Validation failed for {organism}")
                failed += 1
        else:
            failed += 1
        
        time.sleep(1)  # Polite rate limiting
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {len(TEST_ORGANISMS)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(TEST_ORGANISMS)*100):.1f}%")
    
    if failed == 0:
        print("\n[SUCCESS] All tests passed! AI feature is working correctly.")
        return 0
    else:
        print(f"\n[FAILURE] {failed} test(s) failed.")
        return 1

if __name__ == "__main__":
    exit(main())
