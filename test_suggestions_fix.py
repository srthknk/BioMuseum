#!/usr/bin/env python3
"""
Test script to verify that user suggestions are now properly displayed
in the admin panel Users History tab.
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminSBES"

def test_suggestions_endpoint():
    """Test the suggestions endpoint"""
    
    print("\n" + "="*60)
    print("Testing User Suggestions Fix")
    print("="*60)
    
    # Step 1: Login as admin
    print("\n[Step 1] Logging in as admin...")
    try:
        login_response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
            timeout=10
        )
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
        
        token_data = login_response.json()
        token = token_data.get('access_token')
        
        if not token:
            print("❌ No token received from login")
            return False
        
        print(f"✅ Login successful. Token: {token[:20]}...")
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return False
    
    # Step 2: Fetch all suggestions
    print("\n[Step 2] Fetching all suggestions from /admin/suggestions...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        suggestions_response = requests.get(
            f"{API_URL}/admin/suggestions",
            headers=headers,
            timeout=10
        )
        
        print(f"Response Status: {suggestions_response.status_code}")
        
        if suggestions_response.status_code != 200:
            print(f"❌ Failed to fetch suggestions: {suggestions_response.status_code}")
            print(f"Response: {suggestions_response.text}")
            return False
        
        suggestions_data = suggestions_response.json()
        
        print(f"✅ Successfully fetched suggestions")
        print(f"📊 Total suggestions: {len(suggestions_data)}")
        
        if len(suggestions_data) > 0:
            print("\n📋 First suggestion details:")
            first_sugg = suggestions_data[0]
            for key, value in first_sugg.items():
                if key not in ['_id']:
                    print(f"  • {key}: {value}")
        else:
            print("⚠️  No suggestions found in database")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fetching suggestions: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print(f"\n🧪 Starting test at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 API URL: {API_URL}")
    
    success = test_suggestions_endpoint()
    
    print("\n" + "="*60)
    if success:
        print("✅ TEST PASSED - Suggestions endpoint is working!")
    else:
        print("❌ TEST FAILED - Issues found with suggestions endpoint")
    print("="*60 + "\n")
    
    sys.exit(0 if success else 1)
