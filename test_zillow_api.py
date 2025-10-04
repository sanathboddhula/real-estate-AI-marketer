import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def test_zillow_api():
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }
    
    # Test with Staten Island Zillow listing
    address = "179 Mann Ave Staten Island NY 10314"
    zpid = "32289888"  # From the Zillow URL
    
    try:
        # Try property details endpoint with ZPID
        print("=== Testing Property Details by ZPID ===")
        search_url = "https://zillow-com1.p.rapidapi.com/property"
        search_params = {"zpid": zpid}
        
        response = requests.get(search_url, headers=headers, params=search_params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            print(f"Sample data: {json.dumps(data, indent=2)[:1500]}...")
        else:
            print(f"Error: {response.text}")
            
        # Try search by address
        print("\n=== Testing Address Search ===")
        search_url2 = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
        search_params2 = {"location": address}
        
        response2 = requests.get(search_url2, headers=headers, params=search_params2)
        print(f"Status Code: {response2.status_code}")
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"Response keys: {list(data2.keys())}")
            print(f"Sample data: {json.dumps(data2, indent=2)[:1500]}...")
        else:
            print(f"Error: {response2.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_zillow_api()