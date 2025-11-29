#!/usr/bin/env python3
"""
Simple test script for the AI organism endpoint
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

def test_ai_organism():
    print("=" * 80)
    print("🤖 Testing AI Organism Generation Endpoint")
    print("=" * 80)
    
    # Test organism names
    test_organisms = [
        "Lion",
        "Honeybee",
        "Dolphin"
    ]
    
    for organism_name in test_organisms:
        print(f"\n📝 Testing: {organism_name}")
        print("-" * 40)
        
        try:
            response = requests.post(
                f"{API_URL}/admin/organisms/ai-complete",
                json={"organism_name": organism_name},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    organism_data = data.get("data", {})
                    print(f"✅ Success!")
                    print(f"   Name: {organism_data.get('name')}")
                    print(f"   Scientific Name: {organism_data.get('scientific_name')}")
                    print(f"   Kingdom: {organism_data.get('classification', {}).get('kingdom')}")
                    print(f"   Morphology: {organism_data.get('morphology', '')[:100]}...")
                else:
                    print(f"❌ Request failed: {data}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            print(f"❌ Timeout - AI response took too long")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        time.sleep(2)  # Rate limiting

if __name__ == "__main__":
    print("\nWaiting for backend to be ready...")
    time.sleep(5)
    test_ai_organism()
