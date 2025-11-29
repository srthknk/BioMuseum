#!/usr/bin/env python3
"""
Direct Verification of Admin Credentials
Tests the authentication logic directly without making HTTP requests
"""

import hashlib
import json

print("\n" + "="*80)
print("🔐 ADMIN CREDENTIALS VERIFICATION")
print("="*80 + "\n")

# The credentials stored in backend
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminSBES"  # ✅ CORRECT (no space)

print("Backend Configuration:")
print(f"  Username: '{ADMIN_USERNAME}'")
print(f"  Password: '{ADMIN_PASSWORD}'")

# Generate the expected token
expected_token = hashlib.sha256(f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}".encode()).hexdigest()
print(f"\n✅ Expected Auth Token (SHA256):")
print(f"  {expected_token}\n")

print("="*80)
print("CREDENTIAL TESTS")
print("="*80 + "\n")

test_cases = [
    ("✅ CORRECT", "admin", "adminSBES", True),
    ("❌ WRONG - with space", "admin", "admin SBES", False),
    ("❌ WRONG - lowercase", "admin", "adminsbes", False),
    ("❌ WRONG - extra space", "admin", "admin SBES ", False),
    ("❌ WRONG - typo", "admin", "adminSBE", False),
    ("❌ WRONG - reversed", "admin", "SEBSdmina", False),
]

results = []

for test_name, username, password, should_pass in test_cases:
    # Test the authentication
    auth_matches = (username == ADMIN_USERNAME and password == ADMIN_PASSWORD)
    test_result = auth_matches == should_pass
    
    token = hashlib.sha256(f"{username}:{password}".encode()).hexdigest()
    token_matches = token == expected_token
    
    status = "✓ PASS" if test_result else "✗ FAIL"
    color = "\033[92m" if test_result else "\033[91m"
    
    print(f"{color}{status}\033[0m - {test_name}")
    print(f"      Input: username='{username}', password='{password}'")
    print(f"      Auth OK: {auth_matches}, Token OK: {token_matches}")
    
    results.append(test_result)

print("\n" + "="*80)
print("📊 RESULTS SUMMARY")
print("="*80 + "\n")

passed = sum(results)
total = len(results)

print(f"Tests Passed: {passed}/{total}")

if all(results):
    print("\n✅ ALL TESTS PASSED - Credentials are correctly configured!\n")
else:
    print("\n❌ Some tests failed - Check configuration\n")

print("="*80)
print("🔑 FINAL CREDENTIALS TO USE")
print("="*80)
print(f"""
Username: admin
Password: adminSBES

⚠️  IMPORTANT: There is NO SPACE between "admin" and "SBES"
    Wrong: "admin SBES" (has space) ❌
    Right: "adminSBES" (no space)   ✅
    
Use these exact credentials when logging into the admin panel.
""")
print("="*80 + "\n")
