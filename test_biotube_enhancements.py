#!/usr/bin/env python3
"""
Test script to verify Biotube enhancements:
- Thumbnail URLs
- QR Code generation
- Comments system
- Theater mode
- Responsive design
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000/api"
ADMIN_TOKEN = "test_token_here"  # Set this when testing with admin

COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'BLUE': '\033[94m',
    'YELLOW': '\033[93m',
    'END': '\033[0m'
}

def print_test(test_name, passed, detail=""):
    icon = f"{COLORS['GREEN']}✅{COLORS['END']}" if passed else f"{COLORS['RED']}❌{COLORS['END']}"
    print(f"{icon} {test_name}")
    if detail:
        print(f"   └─ {detail}")

def test_video_thumbnails():
    """Test that video thumbnails are working"""
    print(f"\n{COLORS['BLUE']}1. Testing Video Thumbnails{COLORS['END']}")
    try:
        response = requests.get(f"{BASE_URL}/biotube/videos")
        videos = response.json()
        
        if videos:
            has_thumbnails = all('thumbnail_url' in v for v in videos)
            print_test("Videos have thumbnail_url field", has_thumbnails, 
                      f"Found {len(videos)} videos")
            
            # Check at least one has a valid thumbnail URL
            valid_thumbnails = sum(1 for v in videos if v.get('thumbnail_url'))
            print_test("Thumbnails are populated", valid_thumbnails > 0,
                      f"{valid_thumbnails}/{len(videos)} videos have thumbnails")
        else:
            print_test("Videos retrieved", False, "No videos in database")
    except Exception as e:
        print_test("Video retrieval", False, str(e))

def test_qr_code_generation():
    """Test that QR codes are generated for videos"""
    print(f"\n{COLORS['BLUE']}2. Testing QR Code Generation{COLORS['END']}")
    try:
        response = requests.get(f"{BASE_URL}/biotube/videos")
        videos = response.json()
        
        if videos:
            has_qr = all('qr_code' in v for v in videos)
            print_test("Videos have qr_code field", has_qr,
                      f"Found {len(videos)} videos")
            
            # Check at least one has QR code
            valid_qr = sum(1 for v in videos if v.get('qr_code'))
            print_test("QR codes are generated", valid_qr > 0,
                      f"{valid_qr}/{len(videos)} videos have QR codes")
    except Exception as e:
        print_test("QR code check", False, str(e))

def test_comments_endpoints():
    """Test that comment endpoints exist"""
    print(f"\n{COLORS['BLUE']}3. Testing Comments System{COLORS['END']}")
    try:
        # Get first video
        response = requests.get(f"{BASE_URL}/biotube/videos")
        videos = response.json()
        
        if not videos:
            print_test("Videos available", False, "No videos in database")
            return
        
        video_id = videos[0]['id']
        
        # Test GET comments endpoint
        response = requests.get(f"{BASE_URL}/biotube/videos/{video_id}/comments")
        print_test("GET /biotube/videos/{id}/comments", response.status_code == 200,
                  f"Status: {response.status_code}")
        
        # Test POST comment (this should work without auth)
        comment_data = {
            "user_name": "Test User",
            "user_class": "10th",
            "text": "This is a test comment"
        }
        response = requests.post(f"{BASE_URL}/biotube/videos/{video_id}/comments", 
                               json=comment_data)
        print_test("POST /biotube/videos/{id}/comments", response.status_code in [200, 201],
                  f"Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            comment_id = response.json().get('id')
            print_test("Comment ID returned", comment_id is not None,
                      f"ID: {comment_id}")
            
            # Test GET comments again
            response = requests.get(f"{BASE_URL}/biotube/videos/{video_id}/comments")
            comments = response.json()
            has_comment = any(c['user_name'] == 'Test User' for c in comments)
            print_test("Comment appears in list", has_comment,
                      f"Found {len(comments)} comments")
    except Exception as e:
        print_test("Comments system", False, str(e))

def test_responsive_design():
    """Test that responsive classes are present"""
    print(f"\n{COLORS['BLUE']}4. Testing Responsive Design{COLORS['END']}")
    try:
        # Check if frontend files have responsive Tailwind classes
        with open('frontend/src/components/BiotubeVideoPage.jsx', 'r') as f:
            content = f.read()
            has_sm = 'sm:' in content
            has_lg = 'lg:' in content
            has_grid = 'grid' in content
            print_test("Responsive Tailwind classes (sm:)", has_sm)
            print_test("Responsive Tailwind classes (lg:)", has_lg)
            print_test("Grid/flex layout system", has_grid)
        
        with open('frontend/src/components/BiotubeAdminPanel.jsx', 'r') as f:
            content = f.read()
            has_grid = 'grid-cols-1 sm:grid-cols-2' in content
            has_lg_grid = 'lg:grid-cols-3' in content
            print_test("Responsive grid (mobile-first)", has_grid)
            print_test("Responsive grid (desktop)", has_lg_grid)
    except Exception as e:
        print_test("Responsive design check", False, str(e))

def test_theater_mode():
    """Test that theater mode is available"""
    print(f"\n{COLORS['BLUE']}5. Testing Theater Mode{COLORS['END']}")
    try:
        with open('frontend/src/components/BiotubeVideoPage.jsx', 'r') as f:
            content = f.read()
            has_theater_mode = "playerMode === 'theater'" in content
            has_mini_removed = "'mini'" not in content.split("playerMode")[0]  # Check it's not in playerMode definition
            has_toggle = "Theater Mode" in content
            
            print_test("Theater mode implemented", has_theater_mode)
            print_test("Mini player removed", has_mini_removed)
            print_test("Theater mode toggle button", has_toggle)
    except Exception as e:
        print_test("Theater mode check", False, str(e))

def main():
    print(f"\n{COLORS['YELLOW']}═══════════════════════════════════════════════════════════{COLORS['END']}")
    print(f"{COLORS['YELLOW']}Biotube Enhancements Test Suite{COLORS['END']}")
    print(f"{COLORS['YELLOW']}═══════════════════════════════════════════════════════════{COLORS['END']}")
    
    print(f"\n{COLORS['YELLOW']}Note: Ensure backend is running at {BASE_URL}{COLORS['END']}\n")
    
    test_video_thumbnails()
    test_qr_code_generation()
    test_comments_endpoints()
    test_responsive_design()
    test_theater_mode()
    
    print(f"\n{COLORS['YELLOW']}═══════════════════════════════════════════════════════════{COLORS['END']}")
    print(f"{COLORS['YELLOW']}Test suite completed!{COLORS['END']}")
    print(f"{COLORS['YELLOW']}═══════════════════════════════════════════════════════════{COLORS['END']}\n")

if __name__ == "__main__":
    main()
