import requests
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

class ZillowStorytellingService:
    def __init__(self):
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
    def parse_zillow_url(self, zillow_url):
        """Extract property ID and get full data from Zillow URL"""
        # Extract property ID from URL patterns
        patterns = [
            r'/homedetails/[^/]+/(\d+)_zpid',
            r'/b/([^/]+)',
            r'zpid=(\d+)'
        ]
        
        property_id = None
        for pattern in patterns:
            match = re.search(pattern, zillow_url)
            if match:
                property_id = match.group(1)
                break
        
        if not property_id:
            raise ValueError("Invalid Zillow URL")
        
        return self.get_property_by_id(property_id)

    def get_property_by_id(self, property_id):
        """Get property data using Zillow property ID"""
        if not self.rapidapi_key:
            return self._get_mock_property_data("Sample Address")
            
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
        }
        
        try:
            url = f"https://zillow-com1.p.rapidapi.com/property"
            params = {"zpid": property_id}
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return self._format_property_data(response.json())
        except Exception as e:
            print(f"Zillow API error: {e}")
        
        return self._get_mock_property_data("Sample Address")
        
    def get_neighborhood_data(self, address):
        """Get neighborhood data from Zillow via RapidAPI"""
        if not self.rapidapi_key:
            return self._get_mock_neighborhood_data(address)
            
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
        }
        
        try:
            search_url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
            search_params = {"location": address, "status_type": "ForSale"}
            
            response = requests.get(search_url, headers=headers, params=search_params)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('props'):
                    return self._extract_neighborhood_insights(data['props'][0])
            
        except Exception as e:
            print(f"Zillow API error: {e}")
            
        return self._get_mock_neighborhood_data(address)
    
    def _extract_neighborhood_insights(self, property_data):
        """Extract neighborhood insights from Zillow property data"""
        return {
            'neighborhood_name': property_data.get('address', {}).get('neighborhood', 'Great Neighborhood'),
            'walkability': property_data.get('walkScore', 85),
            'schools': property_data.get('schools', ['Excellent Schools']),
            'year_built': property_data.get('yearBuilt', '2010')
        }
    
    def _get_mock_neighborhood_data(self, address):
        """Fallback mock data"""
        # city = address.split(',')[1].strip() if ',' in address else 'Great City'
        # return {
        #     'neighborhood_name': f'{city} Heights',
        #     'walkability': 85,
        #     'schools': ['Top-Rated Elementary', 'Excellent High School'],
        #     'year_built': '2015'
        # }
        return {
            'neighborhood_name': 'Great Neighborhood',
            'walkability': 75,
            'schools': ['Local Schools'],
            'year_built': '2010'
        }
    
    def generate_neighborhood_story(self, address, story_type='balanced'):
        """AI generates compelling neighborhood narrative with variations"""
        neighborhood_data = self.get_neighborhood_data(address)
        
        if not self.openai_api_key:
            return self._generate_mock_story(neighborhood_data)
        
        story_styles = {
            'family': 'Focus on schools, safety, community activities, and family-friendly amenities',
            'luxury': 'Emphasize prestige, exclusivity, high-end amenities, and status appeal',
            'investment': 'Highlight ROI potential, market trends, rental income, and appreciation',
            'lifestyle': 'Focus on convenience, entertainment, dining, and urban living',
            'balanced': 'Create well-rounded appeal covering lifestyle, investment, and community'
        }
        

        
        prompt = f"""
Create a compelling neighborhood story for a real estate flyer:

Neighborhood: {neighborhood_data['neighborhood_name']}
Walkability Score: {neighborhood_data['walkability']}/100
Schools: {', '.join(neighborhood_data['schools'][:2])}

Style: {story_styles[story_type]}

Generate JSON with:
1. headline (max 6 words, catchy and memorable)
2. lifestyle_copy (2 engaging sentences with specific benefits)
3. investment_angle (1 compelling sentence about value/potential)
4. emotional_hook (1 sentence that creates desire)
"""
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.openai_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 250,
                    'temperature': 0.8
                }
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                return json.loads(content)
            else:
                print(f"OpenAI API error: {response.status_code}")
                return self._generate_mock_story(neighborhood_data)
                
        except Exception as e:
            print(f"OpenAI error: {e}")
        return self._generate_mock_story(neighborhood_data)
    
    def _generate_mock_story(self, neighborhood_data):
        """Fallback story generation"""
        return {
            'headline': "",
            'lifestyle_copy': "",
            'investment_angle': "",
            'emotional_hook': ""
        }
    
    def generate_story_variations(self, address):
        """Generate multiple story variations for A/B testing"""
        variations = {}
        story_types = ['family', 'luxury', 'investment', 'lifestyle']
        
        for story_type in story_types:
            variations[story_type] = self.generate_neighborhood_story(address, story_type)
        
        return variations
    
    def get_property_data(self, address):
        """Get detailed property data for AI agent"""
        if not self.rapidapi_key:
            return self._get_mock_property_data(address)
            
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
        }
        
        try:
            search_url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
            search_params = {"location": address, "status_type": "ForSale"}
            
            response = requests.get(search_url, headers=headers, params=search_params)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('props'):
                    return self._format_property_data(data['props'][0])
            
        except Exception as e:
            print(f"Zillow API error: {e}")
            
        return self._get_mock_property_data(address)
    
    def get_comparable_properties(self, address):
        """Get comparable properties for CMA analysis"""
        if not self.rapidapi_key:
            return self._get_mock_comparables(address)
            
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
        }
        
        try:
            search_url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
            search_params = {"location": address, "status_type": "RecentlySold"}
            
            response = requests.get(search_url, headers=headers, params=search_params)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('props'):
                    return [self._format_property_data(prop) for prop in data['props'][:5]]
            
        except Exception as e:
            print(f"Zillow API error: {e}")
            
        return self._get_mock_comparables(address)
    
    def _format_property_data(self, raw_data):
        """Format raw Zillow data for AI agent"""
        # Handle case where raw_data is not a dict
        if not isinstance(raw_data, dict):
            return self._get_mock_property_data("Sample Address")
        
        # Extract main property image
        main_image_url = self._extract_main_image(raw_data)
        
        # Extract address from various possible fields
        address = self._extract_address(raw_data)
        
        return {
            'address': address,
            'price': raw_data.get('price', 0),
            'bedrooms': raw_data.get('bedrooms', 0),
            'bathrooms': raw_data.get('bathrooms', 0),
            'livingArea': raw_data.get('livingArea', 0),
            'lotSize': raw_data.get('lotSize', 0),
            'yearBuilt': raw_data.get('yearBuilt', 'N/A'),
            'propertyType': raw_data.get('propertyType', 'Single Family'),
            'main_image_url': main_image_url
        }
    
    def _extract_address(self, property_data):
        """Extract formatted address from Zillow property data"""
        # Handle case where property_data is not a dict
        if not isinstance(property_data, dict):
            return 'Address Not Available'
        
        # Try different address field formats
        address_sources = [
            property_data.get('address'),
            property_data.get('streetAddress'),
            property_data.get('fullAddress'),
            property_data.get('formattedAddress')
        ]
        
        for address in address_sources:
            if isinstance(address, str) and address and address != 'N/A':
                return address
            elif isinstance(address, dict):
                # Handle structured address object
                parts = []
                if address.get('streetNumber'):
                    parts.append(str(address.get('streetNumber')))
                if address.get('streetName'):
                    parts.append(address.get('streetName'))
                if address.get('city'):
                    parts.append(address.get('city'))
                if address.get('state'):
                    parts.append(address.get('state'))
                if address.get('zipcode'):
                    parts.append(str(address.get('zipcode')))
                
                if parts:
                    return ', '.join(parts)
        
        # Fallback: try to construct from individual fields
        street_parts = []
        if property_data.get('streetNumber'):
            street_parts.append(str(property_data.get('streetNumber')))
        if property_data.get('streetName'):
            street_parts.append(property_data.get('streetName'))
        
        location_parts = []
        if property_data.get('city'):
            location_parts.append(property_data.get('city'))
        if property_data.get('state'):
            location_parts.append(property_data.get('state'))
        if property_data.get('zipcode'):
            location_parts.append(str(property_data.get('zipcode')))
        
        if street_parts and location_parts:
            return f"{' '.join(street_parts)}, {', '.join(location_parts)}"
        elif street_parts:
            return ' '.join(street_parts)
        
        return 'Address Not Available'
    
    def _extract_main_image(self, property_data):
        """Extract the main property image from Zillow data"""
        # Handle case where property_data is not a dict
        if not isinstance(property_data, dict):
            return None
        
        # Try different possible image fields from Zillow API
        image_sources = [
            property_data.get('photos', []),
            property_data.get('images', []),
            property_data.get('imgSrc'),
            property_data.get('image'),
            property_data.get('primaryPhoto', {}).get('url') if isinstance(property_data.get('primaryPhoto'), dict) else None
        ]
        
        for source in image_sources:
            if isinstance(source, list) and source:
                # Get first/main image from array
                first_image = source[0]
                if isinstance(first_image, dict):
                    return first_image.get('url') or first_image.get('src')
                elif isinstance(first_image, str):
                    return first_image
            elif isinstance(source, str) and source:
                return source
        
        return None
    
    def _get_mock_property_data(self, address):
        """Mock property data for testing"""
        return {
            'address': address,
            'price': 850000,
            'bedrooms': 4,
            'bathrooms': 3,
            'livingArea': 2200,
            'lotSize': 7500,
            'yearBuilt': '2015',
            'propertyType': 'Single Family',
            'main_image_url': None
        }
    
    def get_property_insights(self, address):
        """Get enhanced property insights for UI display"""
        if not self.rapidapi_key:
            return self._get_mock_insights()
            
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
        }
        
        try:
            search_url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
            search_params = {"location": address}
            
            response = requests.get(search_url, headers=headers, params=search_params)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('zpid'):
                    # Get detailed property data
                    detail_url = "https://zillow-com1.p.rapidapi.com/property"
                    detail_params = {"zpid": data['zpid']}
                    
                    detail_response = requests.get(detail_url, headers=headers, params=detail_params)
                    
                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()
                        return self._extract_insights(detail_data)
            
        except Exception as e:
            print(f"Zillow insights error: {e}")
            
        return self._get_mock_insights()
    
    def _extract_insights(self, data):
        """Extract key insights from Zillow property data"""
        price = data.get('price', 0)
        living_area = data.get('livingArea', 1)
        
        return {
            'zestimate': data.get('zestimate', {}).get('value', 'N/A'),
            'page_views': data.get('pageViewCount', 'N/A'),
            'days_on_market': data.get('timeOnZillow', 'N/A'),
            'price_per_sqft': round(price / living_area) if price and living_area else 'N/A',
            'annual_taxes': data.get('taxHistory', [{}])[0].get('taxPaid', 'N/A'),
            'school_rating': self._get_school_rating(data.get('schools', [])),
            'year_built': data.get('yearBuilt', 'N/A')
        }
    
    def _get_school_rating(self, schools):
        """Extract average school rating"""
        if not schools:
            return 'N/A'
        
        ratings = [s.get('rating', 0) for s in schools if s.get('rating')]
        return round(sum(ratings) / len(ratings)) if ratings else 'N/A'
    
    def _get_mock_insights(self):
        """Mock insights for testing"""
        return {
            'zestimate': 'Data unavailable',
            'page_views': 'Data unavailable',
            'days_on_market': 'Data unavailable',
            'price_per_sqft': 'Data unavailable',
            'annual_taxes': 'Data unavailable',
            'school_rating': 'Data unavailable',
            'year_built': 'Data unavailable'
        }
    
    def _get_mock_comparables(self, address):
        """Mock comparable properties for testing"""
        base_price = 850000
        return [
            {
                'address': f'123 Similar St, {address.split(",")[-1].strip()}',
                'price': base_price - 50000,
                'bedrooms': 3,
                'bathrooms': 2,
                'livingArea': 2000
            },
            {
                'address': f'456 Nearby Ave, {address.split(",")[-1].strip()}',
                'price': base_price + 25000,
                'bedrooms': 4,
                'bathrooms': 3,
                'livingArea': 2400
            }
        ]
