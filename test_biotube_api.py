#!/usr/bin/env python3
"""
Test Biotube API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_endpoints():
    print("\n" + "="*70)
    print("🧪 BIOTUBE API ENDPOINT TEST")
    print("="*70 + "\n")
    
    # Colors
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    
    def print_test(name, status, details=""):
        icon = f"{GREEN}✅{END}" if status else f"{RED}❌{END}"
        print(f"{icon} {name}")
        if details:
            print(f"   {details}")
    
    # Test 1: Health check
    print("1️⃣  Testing Backend Connection")
    try:
        response = requests.get(f"{BASE_URL}/health" if hasattr(requests, 'health') else f"{BASE_URL}/biotube/videos?limit=1", timeout=5)
        print_test("Backend is responding", response.status_code < 500, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Backend is responding", False, f"Error: {e}")
        print("\n⚠️  Backend not running. Start it with: python backend/server.py")
        return
    
    print("\n2️⃣  Testing Public Biotube Endpoints")
    
    # Test 2: List videos
    try:
        response = requests.get(f"{BASE_URL}/biotube/videos", timeout=5)
        videos = response.json()
        print_test("GET /biotube/videos", response.status_code == 200, f"Found {len(videos)} videos")
    except Exception as e:
        print_test("GET /biotube/videos", False, f"Error: {e}")
    
    # Test 3: Get filters
    try:
        response = requests.get(f"{BASE_URL}/biotube/filters", timeout=5)
        filters = response.json()
        print_test("GET /biotube/filters", response.status_code == 200, f"Filter keys: {list(filters.keys())}")
    except Exception as e:
        print_test("GET /biotube/filters", False, f"Error: {e}")
    
    # Test 4: Submit suggestion
    print("\n3️⃣  Testing Suggestion Submission")
    suggestion_data = {
        "user_name": f"Test User {datetime.now().strftime('%H%M%S')}",
        "user_class": "12th",
        "video_title": "Test Video",
        "video_description": "Testing suggestion system"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/biotube/suggest-video", json=suggestion_data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print_test("POST /biotube/suggest-video", True, f"ID: {result.get('id')}")
            suggestion_id = result.get('id')
        else:
            print_test("POST /biotube/suggest-video", False, f"Status: {response.status_code}")
            print(f"   Response: {response.text}")
            suggestion_id = None
    except Exception as e:
        print_test("POST /biotube/suggest-video", False, f"Error: {e}")
        suggestion_id = None
    
    print("\n4️⃣  Testing Admin Endpoints (Admin Auth Required)")
    
    # For testing, we need a token - get from browser or environment
    token = input("\n⚠️  Admin authentication required.\nEnter your admin token (from browser cookies/localStorage): ").strip()
    
    if not token:
        print("\n❌ No token provided. Skipping admin endpoint tests.")
        print("   To get token: Open browser DevTools (F12) → Console → localStorage.getItem('token')")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 5: Get dashboard
    try:
        response = requests.get(f"{BASE_URL}/admin/biotube/dashboard", headers=headers, timeout=5)
        if response.status_code == 200:
            dashboard = response.json()
            print_test("GET /admin/biotube/dashboard", True, 
                      f"Videos: {dashboard.get('total_videos')}, Pending: {dashboard.get('pending_suggestions')}")
        else:
            print_test("GET /admin/biotube/dashboard", False, f"Status: {response.status_code}")
            if response.status_code == 401:
                print("   Token expired or invalid. Try a fresh token.")
    except Exception as e:
        print_test("GET /admin/biotube/dashboard", False, f"Error: {e}")
    
    # Test 6: Get suggestions
    print("\n5️⃣  Testing Suggestions Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/admin/biotube/suggestions", headers=headers, timeout=5)
        if response.status_code == 200:
            suggestions = response.json()
            print_test("GET /admin/biotube/suggestions", True, f"Found {len(suggestions)} suggestions")
            
            if suggestions:
                print(f"\n   First suggestion:")
                sugg = suggestions[0]
                print(f"      - Title: {sugg.get('video_title')}")
                print(f"      - User: {sugg.get('user_name')} ({sugg.get('user_class')})")
                print(f"      - Status: {sugg.get('status')}")
            else:
                print(f"\n   ⚠️  No suggestions found.")
                print(f"      Go to /biotube page and submit a suggestion first.")
        else:
            print_test("GET /admin/biotube/suggestions", False, f"Status: {response.status_code}")
            try:
                print(f"   Response: {response.json()}")
            except:
                print(f"   Response: {response.text}")
    except Exception as e:
        print_test("GET /admin/biotube/suggestions", False, f"Error: {e}")
    
    # Test 7: Get user history
    try:
        response = requests.get(f"{BASE_URL}/admin/biotube/user-history", headers=headers, timeout=5)
        if response.status_code == 200:
            history = response.json()
            print_test("GET /admin/biotube/user-history", True, f"Found {len(history)} users")
        else:
            print_test("GET /admin/biotube/user-history", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("GET /admin/biotube/user-history", False, f"Error: {e}")
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETE")
    print("="*70 + "\n")
    
    print("📊 Summary:")
    print("   - Public endpoints should return 200")
    print("   - Admin endpoints require valid token")
    print("   - Suggestions should appear if data exists in database")
    print()

if __name__ == "__main__":
    test_endpoints()
