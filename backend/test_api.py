"""
Test Script for Chemical Equipment Parameter Visualizer
Run this after starting the backend server
"""

import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000/api"
access_token = None

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_register():
    """Test user registration"""
    print_section("TEST 1: User Registration")
    
    url = f"{BASE_URL}/auth/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print("✅ Registration successful!")
            result = response.json()
            print(f"   User ID: {result['user']['id']}")
            print(f"   Username: {result['user']['username']}")
            print(f"   Token received: {result['access'][:20]}...")
            return result['access']
        else:
            print(f"⚠️  Registration response: {response.status_code}")
            print(f"   (User may already exist)")
            return None
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        return None

def test_login():
    """Test user login"""
    print_section("TEST 2: User Login")
    
    url = f"{BASE_URL}/auth/login/"
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("✅ Login successful!")
            result = response.json()
            print(f"   Username: {result['user']['username']}")
            print(f"   Email: {result['user']['email']}")
            print(f"   Access token: {result['access'][:20]}...")
            return result['access']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_profile(token):
    """Test get user profile"""
    print_section("TEST 3: Get User Profile")
    
    url = f"{BASE_URL}/auth/profile/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ Profile retrieved successfully!")
            result = response.json()
            print(f"   ID: {result['id']}")
            print(f"   Username: {result['username']}")
            print(f"   Email: {result['email']}")
            print(f"   Name: {result.get('first_name', '')} {result.get('last_name', '')}")
        else:
            print(f"❌ Profile retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Profile error: {e}")

def test_csv_upload(token):
    """Test CSV file upload"""
    print_section("TEST 4: CSV Upload")
    
    url = f"{BASE_URL}/datasets/upload/"
    headers = {"Authorization": f"Bearer {token}"}
    
    csv_path = os.path.join(os.path.dirname(__file__), "..", "sample_equipment_data.csv")
    
    if not os.path.exists(csv_path):
        print(f"❌ Sample CSV not found at: {csv_path}")
        return None
    
    try:
        with open(csv_path, 'rb') as f:
            files = {'file': ('sample_equipment_data.csv', f, 'text/csv')}
            response = requests.post(url, files=files, headers=headers)
        
        if response.status_code == 201:
            print("✅ CSV uploaded successfully!")
            result = response.json()
            print(f"   Dataset ID: {result['id']}")
            print(f"   Filename: {result['filename']}")
            print(f"   Total Count: {result['total_count']}")
            print(f"   Avg Flowrate: {result['avg_flowrate']:.2f}")
            print(f"   Avg Pressure: {result['avg_pressure']:.2f}")
            print(f"   Avg Temperature: {result['avg_temperature']:.2f}")
            print(f"   Equipment Types: {result['equipment_types']}")
            return result['id']
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   {response.text}")
            return None
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def test_get_datasets(token):
    """Test get all datasets"""
    print_section("TEST 5: Get All Datasets")
    
    url = f"{BASE_URL}/datasets/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ Datasets retrieved successfully!")
            datasets = response.json()
            print(f"   Total datasets: {len(datasets)}")
            for ds in datasets:
                print(f"   - {ds['filename']} (ID: {ds['id']}, Count: {ds['total_count']})")
            return datasets
        else:
            print(f"❌ Failed to get datasets: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def test_get_dataset_detail(token, dataset_id):
    """Test get dataset details"""
    print_section("TEST 6: Get Dataset Details")
    
    url = f"{BASE_URL}/datasets/{dataset_id}/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ Dataset details retrieved!")
            result = response.json()
            print(f"   ID: {result['id']}")
            print(f"   Filename: {result['filename']}")
            print(f"   Records: {len(result['records'])}")
            print(f"   First record: {result['records'][0]['equipment_name']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_download_report(token, dataset_id):
    """Test PDF report download"""
    print_section("TEST 7: Download PDF Report")
    
    url = f"{BASE_URL}/datasets/{dataset_id}/report/"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            filename = f"test_report_{dataset_id}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print("✅ PDF report downloaded successfully!")
            print(f"   Saved as: {filename}")
            print(f"   Size: {len(response.content)} bytes")
        else:
            print(f"❌ Download failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_all_tests():
    """Run all API tests"""
    print("\n" + "🧪"*30)
    print("CHEMICAL EQUIPMENT PARAMETER VISUALIZER")
    print("API Test Suite")
    print("🧪"*30)
    
    # Test 1: Register (or skip if exists)
    token = test_register()
    
    # Test 2: Login
    if not token:
        token = test_login()
    
    if not token:
        print("\n❌ Cannot proceed without authentication")
        return
    
    # Test 3: Get Profile
    test_profile(token)
    
    # Test 4: Upload CSV
    dataset_id = test_csv_upload(token)
    
    # Test 5: Get All Datasets
    datasets = test_get_datasets(token)
    
    if not dataset_id and datasets:
        dataset_id = datasets[0]['id']
    
    if dataset_id:
        # Test 6: Get Dataset Details
        test_get_dataset_detail(token, dataset_id)
        
        # Test 7: Download PDF Report
        test_download_report(token, dataset_id)
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60)
    print("\nNext steps:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Register/Login with: testuser / testpass123")
    print("3. Upload sample_equipment_data.csv")
    print("4. View visualizations and download reports")
    print("5. Test the PyQt5 desktop app")
    print("="*60)

if __name__ == "__main__":
    run_all_tests()
