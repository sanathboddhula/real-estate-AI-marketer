#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_rapidapi():
    print("🏠 Testing RapidAPI (Zillow)...")
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    if not rapidapi_key:
        print("❌ RAPIDAPI_KEY not found")
        return False
    
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }
    
    try:
        response = requests.get(
            "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch",
            headers=headers,
            params={"location": "Beverly Hills, CA", "status_type": "ForSale"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ RapidAPI Success: Found {len(data.get('props', []))} properties")
            return True
        else:
            print(f"❌ RapidAPI Error: Status {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ RapidAPI Exception: {e}")
        return False

def test_openai():
    print("\n🤖 Testing OpenAI...")
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        return False
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': 'Say hello'}],
            'max_tokens': 5
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()['choices'][0]['message']['content']
            print(f"✅ OpenAI Success: '{result.strip()}'")
            return True
        else:
            print(f"❌ OpenAI Error: Status {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ OpenAI Exception: {e}")
        return False

def test_freepik():
    print("\n🎨 Testing Freepik...")
    api_key = os.getenv('FREEPIK_API_KEY')
    if not api_key:
        print("❌ FREEPIK_API_KEY not found")
        return False
    
    headers = {'X-Freepik-API-Key': api_key}
    params = {'q': 'house', 'limit': 1}
    
    try:
        response = requests.get(
            'https://api.freepik.com/v1/resources',
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('data', []))
            print(f"✅ Freepik Success: Found {count} images")
            return True
        else:
            print(f"❌ Freepik Error: Status {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Freepik Exception: {e}")
        return False

def main():
    print("🧪 API Connection Test Suite")
    print("=" * 40)
    
    results = {
        'RapidAPI': test_rapidapi(),
        'OpenAI': test_openai(),
        'Freepik': test_freepik()
    }
    
    print("\n📊 Test Results:")
    print("=" * 40)
    
    for api, success in results.items():
        status = "✅ WORKING" if success else "❌ FAILED"
        print(f"{api:<10}: {status}")
    
    working_count = sum(results.values())
    print(f"\n🎯 {working_count}/3 APIs are working")
    
    if working_count == 3:
        print("🎉 All APIs ready for production!")
    elif working_count >= 1:
        print("⚠️  Some APIs working - app will use fallbacks")
    else:
        print("🚨 No APIs working - check your .env file")

if __name__ == "__main__":
    main()