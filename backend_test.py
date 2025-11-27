#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for College Biology Museum
Tests all endpoints including public and admin functionality
"""

import requests
import json
import hashlib
import base64
from typing import Dict, Any, Optional
import sys

# Configuration
BACKEND_URL = "https://biomuseum-scan.preview.emergentagent.com/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin SBES"

class MuseumAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.admin_token = None
        self.test_organism_id = None
        self.test_qr_code_id = None
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }

    def log_result(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        
        if success:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
            self.results["errors"].append(f"{test_name}: {message}")

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_result("Root endpoint", True, f"Response: {data}")
                else:
                    self.log_result("Root endpoint", False, "Missing message field")
            else:
                self.log_result("Root endpoint", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Root endpoint", False, f"Exception: {str(e)}")

    def test_get_organisms(self):
        """Test GET /api/organisms endpoint"""
        try:
            response = requests.get(f"{self.base_url}/organisms")
            if response.status_code == 200:
                organisms = response.json()
                if isinstance(organisms, list):
                    self.log_result("GET organisms", True, f"Found {len(organisms)} organisms")
                    
                    # Validate organism structure if any exist
                    if organisms:
                        organism = organisms[0]
                        required_fields = ["id", "name", "scientific_name", "classification", 
                                         "morphology", "physiology", "qr_code_id", "qr_code_image"]
                        missing_fields = [field for field in required_fields if field not in organism]
                        
                        if missing_fields:
                            self.log_result("Organism structure validation", False, 
                                          f"Missing fields: {missing_fields}")
                        else:
                            self.log_result("Organism structure validation", True, 
                                          "All required fields present")
                            
                            # Store test data for other tests
                            self.test_organism_id = organism["id"]
                            self.test_qr_code_id = organism["qr_code_id"]
                            
                            # Validate QR code is base64 encoded
                            if organism["qr_code_image"] and organism["qr_code_image"].startswith("data:image/png;base64,"):
                                self.log_result("QR code format validation", True, "QR code is properly base64 encoded PNG")
                            else:
                                self.log_result("QR code format validation", False, "QR code format invalid")
                else:
                    self.log_result("GET organisms", False, "Response is not a list")
            else:
                self.log_result("GET organisms", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("GET organisms", False, f"Exception: {str(e)}")

    def test_get_organism_by_id(self):
        """Test GET /api/organisms/{id} endpoint"""
        if not self.test_organism_id:
            self.log_result("GET organism by ID", False, "No test organism ID available")
            return
            
        try:
            response = requests.get(f"{self.base_url}/organisms/{self.test_organism_id}")
            if response.status_code == 200:
                organism = response.json()
                if organism.get("id") == self.test_organism_id:
                    self.log_result("GET organism by ID", True, f"Retrieved organism: {organism['name']}")
                else:
                    self.log_result("GET organism by ID", False, "ID mismatch in response")
            elif response.status_code == 404:
                self.log_result("GET organism by ID", False, "Organism not found (404)")
            else:
                self.log_result("GET organism by ID", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("GET organism by ID", False, f"Exception: {str(e)}")

    def test_get_organism_by_qr(self):
        """Test GET /api/organisms/qr/{qr_code_id} endpoint"""
        if not self.test_qr_code_id:
            self.log_result("GET organism by QR", False, "No test QR code ID available")
            return
            
        try:
            response = requests.get(f"{self.base_url}/organisms/qr/{self.test_qr_code_id}")
            if response.status_code == 200:
                organism = response.json()
                if organism.get("qr_code_id") == self.test_qr_code_id:
                    self.log_result("GET organism by QR", True, f"Retrieved organism via QR: {organism['name']}")
                else:
                    self.log_result("GET organism by QR", False, "QR code ID mismatch in response")
            elif response.status_code == 404:
                self.log_result("GET organism by QR", False, "Organism not found via QR (404)")
            else:
                self.log_result("GET organism by QR", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("GET organism by QR", False, f"Exception: {str(e)}")

    def test_search_organisms(self):
        """Test GET /api/search endpoint"""
        test_queries = ["test", "organism", "bacteria"]
        
        for query in test_queries:
            try:
                response = requests.get(f"{self.base_url}/search", params={"q": query})
                if response.status_code == 200:
                    results = response.json()
                    if isinstance(results, list):
                        self.log_result(f"Search '{query}'", True, f"Found {len(results)} results")
                    else:
                        self.log_result(f"Search '{query}'", False, "Response is not a list")
                else:
                    self.log_result(f"Search '{query}'", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_result(f"Search '{query}'", False, f"Exception: {str(e)}")

    def test_admin_login(self):
        """Test POST /api/admin/login endpoint"""
        try:
            login_data = {
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
            response = requests.post(f"{self.base_url}/admin/login", json=login_data)
            
            if response.status_code == 200:
                token_data = response.json()
                if "access_token" in token_data:
                    self.admin_token = token_data["access_token"]
                    # Verify token matches expected SHA256 hash
                    expected_token = hashlib.sha256(f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}".encode()).hexdigest()
                    if self.admin_token == expected_token:
                        self.log_result("Admin login", True, "Token received and validated")
                    else:
                        self.log_result("Admin login", False, "Token doesn't match expected hash")
                else:
                    self.log_result("Admin login", False, "No access_token in response")
            else:
                self.log_result("Admin login", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_result("Admin login", False, f"Exception: {str(e)}")

    def test_admin_create_organism(self):
        """Test POST /api/admin/organisms endpoint"""
        if not self.admin_token:
            self.log_result("Admin create organism", False, "No admin token available")
            return
            
        try:
            test_organism = {
                "name": "Test Organism",
                "scientific_name": "Testus organismus",
                "classification": {"kingdom": "Testae", "phylum": "Testphylum"},
                "morphology": "Test morphology description",
                "physiology": "Test physiology description",
                "description": "Test organism for API testing"
            }
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.post(f"{self.base_url}/admin/organisms", json=test_organism, headers=headers)
            
            if response.status_code == 200:
                created_organism = response.json()
                if created_organism.get("name") == test_organism["name"]:
                    self.test_created_organism_id = created_organism["id"]
                    self.log_result("Admin create organism", True, f"Created organism: {created_organism['id']}")
                else:
                    self.log_result("Admin create organism", False, "Created organism data mismatch")
            else:
                self.log_result("Admin create organism", False, f"Status: {response.status_code}, Response: {response.text}")
                
        except Exception as e:
            self.log_result("Admin create organism", False, f"Exception: {str(e)}")

    def test_admin_update_organism(self):
        """Test PUT /api/admin/organisms/{id} endpoint"""
        if not self.admin_token:
            self.log_result("Admin update organism", False, "No admin token available")
            return
            
        if not hasattr(self, 'test_created_organism_id'):
            self.log_result("Admin update organism", False, "No test organism to update")
            return
            
        try:
            update_data = {
                "description": "Updated test description"
            }
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.put(f"{self.base_url}/admin/organisms/{self.test_created_organism_id}", 
                                  json=update_data, headers=headers)
            
            if response.status_code == 200:
                updated_organism = response.json()
                if updated_organism.get("description") == update_data["description"]:
                    self.log_result("Admin update organism", True, "Organism updated successfully")
                else:
                    self.log_result("Admin update organism", False, "Update data not reflected")
            else:
                self.log_result("Admin update organism", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_result("Admin update organism", False, f"Exception: {str(e)}")

    def test_admin_delete_organism(self):
        """Test DELETE /api/admin/organisms/{id} endpoint"""
        if not self.admin_token:
            self.log_result("Admin delete organism", False, "No admin token available")
            return
            
        if not hasattr(self, 'test_created_organism_id'):
            self.log_result("Admin delete organism", False, "No test organism to delete")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.delete(f"{self.base_url}/admin/organisms/{self.test_created_organism_id}", 
                                     headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if "message" in result:
                    self.log_result("Admin delete organism", True, "Organism deleted successfully")
                else:
                    self.log_result("Admin delete organism", False, "No confirmation message")
            else:
                self.log_result("Admin delete organism", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_result("Admin delete organism", False, f"Exception: {str(e)}")

    def test_unauthorized_admin_access(self):
        """Test that admin endpoints require authentication"""
        try:
            # Test without token
            response = requests.post(f"{self.base_url}/admin/organisms", json={})
            if response.status_code == 401:
                self.log_result("Unauthorized admin access", True, "Properly rejected unauthenticated request")
            else:
                self.log_result("Unauthorized admin access", False, f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_result("Unauthorized admin access", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("=" * 60)
        print("COLLEGE BIOLOGY MUSEUM - BACKEND API TESTING")
        print("=" * 60)
        print(f"Testing backend at: {self.base_url}")
        print()
        
        # Public endpoint tests
        print("🔍 Testing Public Endpoints...")
        self.test_root_endpoint()
        self.test_get_organisms()
        self.test_get_organism_by_id()
        self.test_get_organism_by_qr()
        self.test_search_organisms()
        
        print("\n🔐 Testing Admin Authentication...")
        self.test_admin_login()
        self.test_unauthorized_admin_access()
        
        print("\n⚙️ Testing Admin CRUD Operations...")
        self.test_admin_create_organism()
        self.test_admin_update_organism()
        self.test_admin_delete_organism()
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print("\n🚨 FAILED TESTS:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        print(f"\nOverall Success Rate: {self.results['passed']/(self.results['passed']+self.results['failed'])*100:.1f}%")
        
        return self.results['failed'] == 0

if __name__ == "__main__":
    tester = MuseumAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)