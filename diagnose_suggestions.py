#!/usr/bin/env python3
"""
Comprehensive test for checking MongoDB and API setup
Run this to diagnose Biotube suggestions issues
"""

import sys
import subprocess

print("""
╔════════════════════════════════════════════════════════════════╗
║        BIOTUBE SUGGESTIONS DIAGNOSTIC TOOL                      ║
║        Check MongoDB, Backend, and API configuration            ║
╚════════════════════════════════════════════════════════════════╝
""")

print("\n1️⃣  Checking Python Installation...")
try:
    result = subprocess.run(["python", "--version"], capture_output=True, text=True)
    print(f"   ✅ Python: {result.stdout.strip()}")
except:
    print("   ❌ Python not found")
    sys.exit(1)

print("\n2️⃣  Checking if MongoDB is running...")
try:
    # Try to connect to MongoDB
    from pymongo import MongoClient
    import os
    
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
    # Force a connection test
    client.admin.command('ping')
    print(f"   ✅ MongoDB connected at {mongo_uri}")
    
    # Check if our database exists
    db = client['BioMuseumDB']
    collections = db.list_collection_names()
    print(f"   ✅ Collections in database: {', '.join(collections)}")
    
    # Check for video_suggestions collection
    if 'video_suggestions' in collections:
        count = db['video_suggestions'].count_documents({})
        print(f"   ✅ video_suggestions collection exists with {count} documents")
        
        if count > 0:
            sample = db['video_suggestions'].find_one()
            print(f"   📋 Sample suggestion:")
            print(f"      - User: {sample.get('user_name', 'N/A')}")
            print(f"      - Title: {sample.get('video_title', 'N/A')}")
            print(f"      - Status: {sample.get('status', 'N/A')}")
    else:
        print(f"   ⚠️  video_suggestions collection NOT found")
        print(f"      Collections: {collections}")
    
    client.close()
except ImportError:
    print("   ⚠️  pymongo not installed, skipping MongoDB check")
except Exception as e:
    print(f"   ❌ MongoDB Error: {e}")
    print("      Make sure MongoDB is running and accessible")

print("\n3️⃣  Checking Backend API...")
try:
    import requests
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"   ✅ Backend is running at http://localhost:8000")
except Exception as e:
    print(f"   ❌ Backend not responding: {e}")
    print("      Run 'python backend/server.py' to start backend")

print("\n4️⃣  Testing Biotube Endpoints...")
print("""
   To test the suggestions endpoint manually:
   
   1. Open browser DevTools (F12)
   2. Go to Admin Panel
   3. Click Biotube → Suggestions tab
   4. Check Console for errors
   5. Check Network tab for API requests
   
   Looking for:
   - GET /api/admin/biotube/suggestions
   - Status: 200 (success) or 401/403 (auth error)
   - Response should show array of suggestions
""")

print("""
5️⃣  Quick Troubleshooting Steps:

   If you see "No suggestions yet":
   
   a) Check if suggestions exist:
      - Go to Biotube home page
      - Click "💡 Suggest Video"
      - Fill and submit a suggestion
      - Go back to Admin → Biotube → Suggestions
      
   b) Check browser console for errors:
      - Press F12 to open DevTools
      - Click Console tab
      - Look for any red error messages
      - Copy full error message if present
      
   c) Verify authentication:
      - Make sure you're logged in as admin
      - Check if token is being sent in Authorization header
      - In DevTools Network tab, check request headers
      
   d) Check backend logs:
      - Look at terminal running 'python server.py'
      - Look for any error messages
      - Check that suggestions are being stored
      
   e) Verify database:
      - MongoDB must be running
      - Database name must be 'BioMuseumDB'
      - Collection must be named 'video_suggestions'

6️⃣  Testing Suggestions Creation:

   Frontend test (no coding needed):
   1. Open http://localhost:3000/biotube
   2. Click "💡 Suggest Video"
   3. Fill in form with:
      Name: Test User
      Class: 12th
      Video: Test Video
      Description: Test Description
   4. Click Submit
   5. Watch for success message
   6. Check Admin → Biotube → Suggestions
   
   API test (if requests is installed):
   python test_api.py

7️⃣  Files to Check:

   Backend: d:\\BioMuseum\\backend\\server.py
   - Search for: "@api_router.post('/biotube/suggest-video')"
   - Search for: "@api_router.get('/admin/biotube/suggestions')"
   
   Frontend: d:\\BioMuseum\\frontend\\src\\components\\BiotubeAdminPanel.jsx
   - Should have fetchData() with suggestions tab handling
   - Should have handleUpdateSuggestionStatus() function

═════════════════════════════════════════════════════════════════

Need more help? Check these logs:
- Browser DevTools Console (F12)
- Backend terminal output
- MongoDB connection status

═════════════════════════════════════════════════════════════════
""")
