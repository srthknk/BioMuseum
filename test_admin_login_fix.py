#!/usr/bin/env python3
"""
Admin Login Fix Verification Test
Verifies that the correct credentials work for admin login
"""

import requests
import json
import hashlib

print("\n" + "="*80)
print("🔐 ADMIN LOGIN FIX VERIFICATION TEST")
print("="*80 + "\n")

# Test with different backends
backends = [
    ("Local Dev", "http://localhost:8000/api"),
    ("Production (Render)", "https://biomuseum.onrender.com/api"),
]

# Test credentials
test_cases = [
    {
        "name": "✅ CORRECT",
        "username": "admin",
        "password": "adminSBES",
        "should_pass": True
    },
    {
        "name": "❌ WRONG (with space)",
        "username": "admin", 
        "password": "admin SBES",
        "should_pass": False
    },
    {
        "name": "❌ WRONG (case sensitive)",
        "username": "admin",
        "password": "adminsbes",
        "should_pass": False
    },
    {
        "name": "❌ WRONG (empty password)",
        "username": "admin",
        "password": "",
        "should_pass": False
    }
]

for backend_name, backend_url in backends:
    print(f"\n{backend_name}: {backend_url}")
    print("-" * 80)
    
    try:
        for test in test_cases:
            try:
                response = requests.post(
                    f"{backend_url}/admin/login",
                    json={"username": test["username"], "password": test["password"]},
                    timeout=5
                )
                
                success = response.status_code == 200
                expected = test["should_pass"]
                
                if success == expected:
                    status = "✓ PASS"
                    result_color = "\033[92m"  # Green
                else:
                    status = "✗ FAIL"
                    result_color = "\033[91m"  # Red
                
                print(f"{result_color}{status}\033[0m - {test['name']}")
                
                if success:
                    data = response.json()
                    token = data.get('access_token', '')
                    expected_token = hashlib.sha256("admin:adminSBES".encode()).hexdigest()
                    token_match = token == expected_token
                    print(f"       Token valid: {token_match}")
                else:
                    print(f"       Status: {response.status_code} (expected: 401)")
                    
            except requests.exceptions.Timeout:
                print(f"❌ TIMEOUT - {test['name']} (server not responding)")
            except requests.exceptions.ConnectionError:
                print(f"❌ CONNECTION ERROR - Backend not reachable")
                break
            except Exception as e:
                print(f"❌ ERROR - {test['name']}: {str(e)[:50]}")
        else:
            continue
        break
        
    except Exception as e:
        print(f"❌ Backend {backend_name} not available: {str(e)[:50]}")

print("\n" + "="*80)
print("📊 SUMMARY")
print("="*80 + "\n")

print("""
✅ CORRECT CREDENTIALS:
   Username: admin
   Password: adminSBES

❌ INCORRECT CREDENTIALS:
   • admin SBES (space) - WRONG
   • adminsbes (lowercase) - WRONG
   • other variations - WRONG

📝 NEXT STEPS:
1. If Local Dev test PASSED ✓
   - Backend is working correctly
   - Use these credentials to login
   
2. If Production (Render) test PASSED ✓
   - Admin panel is accessible on production
   - Use these credentials on https://bio-museum.vercel.app

3. If tests are PENDING or OFFLINE:
   - Server might not be running
   - Check Render deployment status
""")

print("="*80 + "\n")
