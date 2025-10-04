import requests
import os

class MapsService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GOOGLE_MAPS_API_KEY')
        self.nominatim_url = 'https://nominatim.openstreetmap.org'
        self.overpass_url = 'https://overpass-api.de/api/interpreter'
    
    def get_neighborhood_insights(self, address):
        """Get neighborhood data using free OpenStreetMap APIs"""
        try:
            # Use Nominatim for geocoding (free)
            geocode_url = f"{self.nominatim_url}/search"
            params = {
                'q': address,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            headers = {'User-Agent': 'RealEstateFlyerGenerator/1.0'}
            
            response = requests.get(geocode_url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    
                    # Get nearby amenities using Overpass API (free)
                    return self._get_overpass_data(lat, lon)
        except Exception as e:
            print(f"OpenStreetMap API error: {e}")
        
        return self._get_realistic_data(address)
    
    def _get_overpass_data(self, lat, lon):
        try:
            query = f"""
            [out:json][timeout:25];
            (
              node["amenity"="school"](around:2000,{lat},{lon});
              node["amenity"="restaurant"](around:2000,{lat},{lon});
              node["leisure"="park"](around:2000,{lat},{lon});
            );
            out geom;
            """
            
            response = requests.post(self.overpass_url, data=query)
            
            if response.status_code == 200:
                data = response.json()
                elements = data.get('elements', [])
                
                schools = [e for e in elements if e.get('tags', {}).get('amenity') == 'school']
                restaurants = [e for e in elements if e.get('tags', {}).get('amenity') == 'restaurant']
                parks = [e for e in elements if e.get('tags', {}).get('leisure') == 'park']
                
                return {
                    'walkability_score': min(95, len(restaurants) * 3 + len(parks) * 5 + 40),
                    'schools_nearby': len(schools),
                    'restaurants_nearby': len(restaurants),
                    'parks_nearby': len(parks),
                    'top_school': schools[0]['tags'].get('name', 'Local School') if schools else 'Schools in area'
                }
        except Exception as e:
            print(f"Overpass API error: {e}")
        
        return self._get_realistic_data()
    
    def _get_realistic_data(self, address=None):
        return {
            'walkability_score': 'Data unavailable',
            'schools_nearby': 'Data unavailable',
            'restaurants_nearby': 'Data unavailable', 
            'parks_nearby': 'Data unavailable',
            'top_school': 'Contact local schools for information'
        }