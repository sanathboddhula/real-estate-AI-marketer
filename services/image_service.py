import requests
import random
from PIL import Image
import io

class ImageService:
    def __init__(self, freepik_api_key=None):
        self.freepik_api_key = freepik_api_key
        self.freepik_base_url = 'https://api.freepik.com/v1'
        self.fallback_images = [
            'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&h=1000&fit=crop&crop=center',
            'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=1000&fit=crop&crop=center',
            'https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=800&h=1000&fit=crop&crop=center',
            'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=1000&fit=crop&crop=center',
            'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=800&h=1000&fit=crop&crop=center'
        ]
    
    def search_freepik_image(self, property_type="house"):
        if not self.freepik_api_key:
            return None
            
        headers = {'X-Freepik-API-Key': self.freepik_api_key}
        search_terms = {
            "luxury": "luxury house exterior real estate",
            "modern": "modern house exterior architecture", 
            "family": "suburban house exterior real estate"
        }
        
        params = {
            'q': search_terms.get(property_type, "house exterior real estate"),
            'limit': 1,
            'filters[content_type]': 'photo',
            'filters[orientation]': 'vertical'
        }
        
        try:
            response = requests.get(f'{self.freepik_base_url}/resources', headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    file_id = data['data'][0]['id']
                    download_response = requests.get(f'{self.freepik_base_url}/file/{file_id}', headers=headers)
                    if download_response.status_code == 200:
                        return download_response.json().get('url')
        except Exception as e:
            print(f"Freepik error: {e}")
        
        return None
    
    def get_fallback_image(self):
        return random.choice(self.fallback_images)
    
    def get_image_from_url(self, url):
        response = requests.get(url, timeout=10)
        return Image.open(io.BytesIO(response.content))