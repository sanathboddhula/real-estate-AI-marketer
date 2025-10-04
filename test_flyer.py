#!/usr/bin/env python3
"""Quick test script for flyer generation"""

import requests
import json

def test_flyer_generation():
    url = 'http://127.0.0.1:5000/generate-flyer'
    
    test_data = {
        'address': '1234 Sunset Boulevard, Beverly Hills, CA 90210',
        'price': '2850000',
        'bedrooms': '5',
        'bathrooms': '4.5'
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Flyer generated successfully!")
                print(f"Image data length: {len(result.get('image', ''))}")
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure Flask app is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_flyer_generation()