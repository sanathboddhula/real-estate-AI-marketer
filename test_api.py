import requests
import os
from dotenv import load_dotenv

load_dotenv()

FREEPIK_API_KEY = os.getenv('FREEPIK_API_KEY')
print(f"API Key: {FREEPIK_API_KEY}")

headers = {
    'X-Freepik-API-Key': FREEPIK_API_KEY,
    'Content-Type': 'application/json'
}

params = {
    'q': 'modern house exterior real estate',
    'limit': 1,
    'order': 'latest'
}

try:
    response = requests.get('https://api.freepik.com/v1/resources', headers=headers, params=params)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")