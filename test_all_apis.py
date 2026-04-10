#!/usr/bin/env python3
"""
Comprehensive API Testing Suite for Restaurant Management System
Tests all endpoints: GET, POST, DELETE
"""

import urllib.request
import json
import sys

BASE_URL = "http://localhost:8000/api"

class APITester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.issues = []
    
    def test(self, name, method, endpoint, data=None, expected_status=200):
        """Test an API endpoint"""
        url = f"{BASE_URL}{endpoint}"
        try:
            if method == "GET":
                response = urllib.request.urlopen(url)
            elif method == "POST":
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode(),
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req)
            elif method == "DELETE":
                req = urllib.request.Request(
                    url,
                    method='DELETE',
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req)
            
            result = json.loads(response.read().decode())
            status = response.status
            
            if status == expected_status:
                print(f"✅ {method} {endpoint} - PASS")
                self.passed += 1
                return result
            else:
                print(f"❌ {method} {endpoint} - Status: {status} (expected {expected_status})")
                self.failed += 1
                self.issues.append(f"{method} {endpoint}: Wrong status code")
                return result
        except Exception as e:
            print(f"❌ {method} {endpoint} - ERROR: {str(e)}")
            self.failed += 1
            self.issues.append(f"{method} {endpoint}: {str(e)}")
            return None
    
    def report(self):
        print("\n" + "="*60)
        print(f"RESULTS: {self.passed} PASSED, {self.failed} FAILED")
        if self.issues:
            print("\nISSUES FOUND:")
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue}")
        print("="*60)

print("Starting API Test Suite...\n")
tester = APITester()

# ==================== GET ENDPOINTS ====================
print("📋 Testing GET Endpoints:")
print("-" * 40)

health = tester.test("Health Check", "GET", "", expected_status=200)
cuisines_data = tester.test("Get Cuisines", "GET", "/cuisines", expected_status=200)
items_data = tester.test("Get Items", "GET", "/items", expected_status=200)
orders_data = tester.test("Get Orders", "GET", "/orders", expected_status=200)

# ==================== POST ENDPOINTS ====================
print("\n📝 Testing POST Endpoints:")
print("-" * 40)

# Add cuisine
new_cuisine = {
    "name": "TEST_CUISINE_DO_NOT_USE",
    "description": "Testing cuisine"
}
cuisine_response = tester.test("Add Cuisine", "POST", "/cuisines", new_cuisine, expected_status=201)
if cuisine_response and "cuisine" in cuisine_response:
    test_cuisine_id = cuisine_response["cuisine"]["_id"]
    print(f"   Created cuisine ID: {test_cuisine_id}")
else:
    print("   WARNING: Could not extract cuisine ID")
    test_cuisine_id = None

# Add food item
new_item = {
    "name": "TEST_ITEM_DO_NOT_USE",
    "price": 999,
    "cuisine_id": 1,
    "description": "Testing item",
    "dietary_info": "Veg"
}
item_response = tester.test("Add Food Item", "POST", "/items", new_item, expected_status=201)
if item_response and "item" in item_response:
    test_item_id = item_response["item"]["_id"]
    print(f"   Created item ID: {test_item_id}")
else:
    print("   WARNING: Could not extract item ID")
    test_item_id = None

# Create order
new_order = {
    "customer_phone": "9876543210",
    "items": [1, 2],
    "total_amount": 500,
    "order_type": "delivery",
    "delivery_address": "123 Test St"
}
order_response = tester.test("Create Order", "POST", "/orders/create", new_order, expected_status=201)
if order_response and "tracking_id" in order_response:
    print(f"   Created order with tracking ID: {order_response['tracking_id']}")

# ==================== DELETE ENDPOINTS ====================
print("\n🗑️  Testing DELETE Endpoints:")
print("-" * 40)

if test_item_id:
    tester.test("Delete Food Item", "DELETE", f"/items/{test_item_id}", expected_status=200)
else:
    print("⚠️  Skipping item deletion (no test item created)")

if test_cuisine_id:
    tester.test("Delete Cuisine", "DELETE", f"/cuisines/{test_cuisine_id}", expected_status=200)
else:
    print("⚠️  Skipping cuisine deletion (no test cuisine created)")

# ==================== VERIFICATION ====================
print("\n✔️  Verification Checks:")
print("-" * 40)

# Verify items count changed
items_after_delete = tester.test("Get Items After Delete", "GET", "/items", expected_status=200)
if items_data and items_after_delete:
    initial_count = len(items_data)
    final_count = len(items_after_delete)
    if final_count == initial_count - 1:
        print(f"✅ Item correctly deleted (count: {initial_count} → {final_count})")
    else:
        print(f"⚠️  Item count mismatch (count: {initial_count} → {final_count})")

# Generate report
tester.report()

sys.exit(0 if tester.failed == 0 else 1)
