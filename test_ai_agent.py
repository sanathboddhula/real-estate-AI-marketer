#!/usr/bin/env python3

import requests
import json

def test_ai_marketing_agent():
    """Test the AI Marketing Agent endpoints"""
    
    base_url = "http://127.0.0.1:5001"
    test_address = "1234 Sunset Boulevard, Beverly Hills, CA 90210"
    
    print("🤖 Testing AI Marketing Agent...")
    print(f"Address: {test_address}")
    print("-" * 50)
    
    # Test 1: Complete AI Marketing Agent
    print("\n1️⃣ Testing Complete AI Marketing Agent...")
    try:
        response = requests.post(f"{base_url}/ai-marketing-agent", 
                               json={"address": test_address})
        
        if response.status_code == 200:
            data = response.json()
            print("✅ AI Marketing Agent - SUCCESS")
            print(f"   Property: {data['property_data']['address']}")
            print(f"   Descriptions: {len(data['descriptions'])} types generated")
            print(f"   Social Content: {len(data['social_content'])} platforms")
            print(f"   CMA Analysis: {'✅' if 'analysis' in data['cma_analysis'] else '❌'}")
        else:
            print(f"❌ AI Marketing Agent - FAILED ({response.status_code})")
            
    except Exception as e:
        print(f"❌ AI Marketing Agent - ERROR: {e}")
    
    # Test 2: Property Descriptions Only
    print("\n2️⃣ Testing Property Descriptions Generator...")
    try:
        response = requests.post(f"{base_url}/generate-descriptions", 
                               json={"address": test_address})
        
        if response.status_code == 200:
            data = response.json()
            descriptions = data['descriptions']
            print("✅ Property Descriptions - SUCCESS")
            print(f"   MLS: {descriptions['mls'][:50]}...")
            print(f"   Luxury: {descriptions['luxury'][:50]}...")
            print(f"   Family: {descriptions['family'][:50]}...")
            print(f"   Investment: {descriptions['investment'][:50]}...")
        else:
            print(f"❌ Property Descriptions - FAILED ({response.status_code})")
            
    except Exception as e:
        print(f"❌ Property Descriptions - ERROR: {e}")
    
    # Test 3: Social Media Content
    print("\n3️⃣ Testing Social Media Content Generator...")
    try:
        response = requests.post(f"{base_url}/generate-social-content", 
                               json={"address": test_address})
        
        if response.status_code == 200:
            data = response.json()
            social = data['social_content']
            print("✅ Social Media Content - SUCCESS")
            print(f"   Instagram Post: {social['instagram']['post'][:50]}...")
            print(f"   Facebook Post: {social['facebook']['post'][:50]}...")
            print(f"   LinkedIn Post: {social['linkedin']['post'][:50]}...")
        else:
            print(f"❌ Social Media Content - FAILED ({response.status_code})")
            
    except Exception as e:
        print(f"❌ Social Media Content - ERROR: {e}")
    
    # Test 4: CMA Analysis
    print("\n4️⃣ Testing CMA Analysis Generator...")
    try:
        response = requests.post(f"{base_url}/generate-cma", 
                               json={"address": test_address})
        
        if response.status_code == 200:
            data = response.json()
            cma = data['cma_analysis']
            print("✅ CMA Analysis - SUCCESS")
            print(f"   Analysis: {cma['analysis'][:100]}...")
            print(f"   Price/SqFt: {cma['metrics']['price_per_sqft']}")
            print(f"   Market Position: {cma['metrics']['position']}")
        else:
            print(f"❌ CMA Analysis - FAILED ({response.status_code})")
            
    except Exception as e:
        print(f"❌ CMA Analysis - ERROR: {e}")
    
    print("\n" + "="*50)
    print("🎯 AI Marketing Agent Test Complete!")
    print("Start your Flask app with: python app.py")
    print("Then test in browser at: http://127.0.0.1:5001")

if __name__ == "__main__":
    test_ai_marketing_agent()