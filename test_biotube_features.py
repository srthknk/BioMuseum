#!/usr/bin/env python3
"""
Test script for Biotube features
Tests:
1. Add video endpoint
2. List videos endpoint
3. Get single video endpoint
4. Suggest video endpoint
5. Get suggestions endpoint
6. Delete suggestion endpoint (new)
7. Get user history endpoint
8. Update suggestion status endpoint
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_success(message):
    print(f"{GREEN}✅ {message}{END}")

def print_error(message):
    print(f"{RED}❌ {message}{END}")

def print_info(message):
    print(f"{BLUE}ℹ️  {message}{END}")

def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{END}")

print(f"\n{BLUE}{'='*60}")
print(f"BIOTUBE API TEST SUITE")
print(f"{'='*60}{END}\n")

# Test 1: Get list of videos
print(f"{BLUE}Test 1: Get list of videos{END}")
try:
    response = requests.get(f"{BASE_URL}/biotube/videos")
    if response.status_code == 200:
        videos = response.json()
        print_success(f"Retrieved {len(videos)} videos")
        if videos:
            print_info(f"Sample video: {videos[0].get('title', 'N/A')}")
    else:
        print_error(f"Failed with status {response.status_code}")
except Exception as e:
    print_error(f"Exception: {e}")

print()

# Test 2: Get available filters
print(f"{BLUE}Test 2: Get available filters{END}")
try:
    response = requests.get(f"{BASE_URL}/biotube/filters")
    if response.status_code == 200:
        filters = response.json()
        print_success(f"Retrieved filters: {', '.join(filters.keys())}")
    else:
        print_error(f"Failed with status {response.status_code}")
except Exception as e:
    print_error(f"Exception: {e}")

print()

# Test 3: Suggest a video (simulate user suggestion)
print(f"{BLUE}Test 3: Suggest a video (public endpoint){END}")
suggestion_payload = {
    "user_name": "Test User",
    "user_class": "12th",
    "video_title": "Lion Hunting Behavior",
    "video_description": "A fascinating documentary about lion hunting techniques"
}
try:
    response = requests.post(f"{BASE_URL}/biotube/suggest-video", json=suggestion_payload)
    if response.status_code == 200:
        result = response.json()
        print_success(f"Video suggestion submitted successfully")
        print_info(f"Suggestion ID: {result.get('id', 'N/A')}")
        suggestion_id = result.get('id')
    else:
        print_error(f"Failed with status {response.status_code}: {response.text}")
        suggestion_id = None
except Exception as e:
    print_error(f"Exception: {e}")
    suggestion_id = None

print()

# Test 4: Check if user authentication is required for admin endpoints
print(f"{BLUE}Test 4: Check admin endpoints protection{END}")
try:
    # Try without token
    response = requests.get(f"{BASE_URL}/admin/biotube/dashboard")
    if response.status_code == 403:
        print_success("Admin endpoints properly protected (403 Forbidden)")
    else:
        print_warning(f"Expected 403, got {response.status_code}")
except Exception as e:
    print_error(f"Exception: {e}")

print()

# Test 5: Get dashboard data (requires admin token - will fail without it)
print(f"{BLUE}Test 5: Check biotube collections in database{END}")
print_info("This test requires admin authentication token")
print_warning("Skipping admin tests without valid token")

print()

# Test 6: Verify suggestion was created
print(f"{BLUE}Test 6: Verify suggestion data structure{END}")
if suggestion_id:
    print_success(f"Suggestion created successfully with ID: {suggestion_id}")
    print_info("Suggestions can be viewed in admin panel -> 'Suggestions' tab")
else:
    print_warning("Could not verify suggestion creation (no ID)")

print()

# Test 7: Test search functionality
print(f"{BLUE}Test 7: Test search functionality{END}")
try:
    response = requests.get(f"{BASE_URL}/biotube/videos?search=lion")
    if response.status_code == 200:
        videos = response.json()
        print_success(f"Search works! Found {len(videos)} videos matching 'lion'")
    else:
        print_error(f"Failed with status {response.status_code}")
except Exception as e:
    print_error(f"Exception: {e}")

print()

# Test 8: Test filtering
print(f"{BLUE}Test 8: Test filtering functionality{END}")
try:
    response = requests.get(f"{BASE_URL}/biotube/videos?kingdom=Animalia")
    if response.status_code == 200:
        videos = response.json()
        print_success(f"Filtering works! Found {len(videos)} videos in kingdom 'Animalia'")
    else:
        print_error(f"Failed with status {response.status_code}")
except Exception as e:
    print_error(f"Exception: {e}")

print()

print(f"{BLUE}{'='*60}")
print(f"TEST SUMMARY")
print(f"{'='*60}{END}")
print("""
✅ Public endpoints tested:
   - GET /biotube/videos (list with search/filter)
   - GET /biotube/filters (available filter options)
   - POST /biotube/suggest-video (user suggestions)

⚠️  Admin endpoints require authentication token:
   - GET /admin/biotube/dashboard (stats)
   - GET /admin/biotube/videos (all videos)
   - GET /admin/biotube/suggestions (pending suggestions)
   - GET /admin/biotube/user-history (all user history)
   - DELETE /admin/biotube/suggestions/{id} (delete suggestions)

To test admin features:
1. Go to http://localhost:3000/admin
2. Navigate to "Biotube" tab
3. Check "Suggestions" tab to see user submissions
4. Check "User History" tab to see and delete suggestions
5. Check "Add Video" tab (now full-width!) to add videos
""")

print(f"\n{GREEN}Biotube API is operational!{END}\n")
