import requests
import os
from typing import Dict, List

class AIMarketingAgent:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
    def generate_property_descriptions(self, property_data: Dict) -> Dict[str, str]:
        """Generate 4 targeted property descriptions"""
        
        base_info = f"""
        Address: {property_data.get('address', 'N/A')}
        Price: ${property_data.get('price', 'N/A')}
        Bedrooms: {property_data.get('bedrooms', 'N/A')}
        Bathrooms: {property_data.get('bathrooms', 'N/A')}
        Square Feet: {property_data.get('livingArea', 'N/A')}
        """
        
        descriptions = {}
        
        # MLS Description
        descriptions['mls'] = self._call_openai(
            f"{base_info}\nWrite a professional MLS listing description (150-200 words). Focus on key features, location benefits, and selling points. Use real estate industry language."
        )
        
        # Luxury Marketing Copy
        descriptions['luxury'] = self._call_openai(
            f"{base_info}\nWrite luxury marketing copy emphasizing exclusivity, premium features, and sophisticated lifestyle. Use elegant, upscale language that appeals to affluent buyers."
        )
        
        # Family-Focused Copy
        descriptions['family'] = self._call_openai(
            f"{base_info}\nWrite family-focused copy highlighting safety, schools, community, and family-friendly features. Emphasize comfort, space, and neighborhood benefits for families."
        )
        
        # Investment Property Copy
        descriptions['investment'] = self._call_openai(
            f"{base_info}\nWrite investment-focused copy emphasizing ROI potential, rental income, market appreciation, and financial benefits. Use data-driven language for investors."
        )
        
        return descriptions
    
    def generate_social_media_content(self, property_data: Dict) -> Dict[str, Dict]:
        """Generate platform-specific social media content"""
        
        base_info = f"""
        Property: {property_data.get('address', 'N/A')}
        Price: ${property_data.get('price', 'N/A')}
        Features: {property_data.get('bedrooms', 'N/A')}BR/{property_data.get('bathrooms', 'N/A')}BA
        """
        
        social_content = {}
        
        # Instagram Content
        instagram_post = self._call_openai(
            f"{base_info}\nCreate an engaging Instagram post with emojis and relevant hashtags. Make it visually appealing and shareable. Include call-to-action."
        )
        
        instagram_story = self._call_openai(
            f"{base_info}\nCreate Instagram story text that's short, engaging, and encourages swipe-ups or DMs. Use casual, friendly tone."
        )
        
        social_content['instagram'] = {
            'post': instagram_post,
            'story': instagram_story,
            'hashtags': '#JustListed #RealEstate #DreamHome #NewListing #PropertyForSale'
        }
        
        # Facebook Content
        facebook_post = self._call_openai(
            f"{base_info}\nCreate a Facebook post that tells a story about this property. Make it engaging for homebuyers and include neighborhood benefits."
        )
        
        social_content['facebook'] = {
            'post': facebook_post,
            'marketplace': f"{property_data.get('bedrooms', 'N/A')}BR/{property_data.get('bathrooms', 'N/A')}BA - Move-in ready - Great location"
        }
        
        # LinkedIn Content
        linkedin_post = self._call_openai(
            f"{base_info}\nCreate a professional LinkedIn post focusing on market insights, investment potential, and professional real estate analysis."
        )
        
        social_content['linkedin'] = {
            'post': linkedin_post
        }
        
        return social_content
    
    def generate_cma_analysis(self, property_data: Dict, comparables: List[Dict]) -> Dict:
        """Generate Comparative Market Analysis"""
        
        if not comparables:
            return {'error': 'No comparable properties found'}
        
        # Format comparables for analysis
        comp_summary = "\n".join([
            f"- {comp.get('address', 'N/A')}: ${comp.get('price', 'N/A')} | {comp.get('bedrooms', 'N/A')}BR/{comp.get('bathrooms', 'N/A')}BA | {comp.get('livingArea', 'N/A')} sqft"
            for comp in comparables[:5]
        ])
        
        prompt = f"""
        Subject Property: {property_data.get('address', 'N/A')} - ${property_data.get('price', 'N/A')}
        
        Comparable Sales:
        {comp_summary}
        
        Generate a professional CMA analysis including:
        1. Market position assessment
        2. Price per square foot analysis  
        3. Competitive advantages/disadvantages
        4. Pricing recommendation
        5. Days on market prediction
        
        Format as a structured report suitable for client presentation.
        """
        
        analysis = self._call_openai(prompt)
        
        # Calculate basic metrics
        try:
            subject_sqft = float(property_data.get('livingArea', 0))
            subject_price = float(property_data.get('price', 0))
            
            if subject_sqft > 0:
                price_per_sqft = subject_price / subject_sqft
            else:
                price_per_sqft = 0
                
            # Calculate average comp price per sqft
            comp_prices_per_sqft = []
            for comp in comparables[:3]:
                comp_sqft = float(comp.get('livingArea', 0))
                comp_price = float(comp.get('price', 0))
                if comp_sqft > 0:
                    comp_prices_per_sqft.append(comp_price / comp_sqft)
            
            avg_comp_price_per_sqft = sum(comp_prices_per_sqft) / len(comp_prices_per_sqft) if comp_prices_per_sqft else 0
            
        except (ValueError, TypeError):
            price_per_sqft = 0
            avg_comp_price_per_sqft = 0
        
        return {
            'subject_property': property_data,
            'comparables': comparables[:5],
            'analysis': analysis,
            'metrics': {
                'price_per_sqft': f'${price_per_sqft:.0f}',
                'market_average': f'${avg_comp_price_per_sqft:.0f}',
                'position': 'Above market' if price_per_sqft > avg_comp_price_per_sqft else 'Below market'
            }
        }
    
    def _call_openai(self, prompt: str) -> str:
        """Make OpenAI API call with error handling"""
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.openai_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [
                        {'role': 'system', 'content': 'You are a professional real estate marketing expert and agent.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'max_tokens': 400,
                    'temperature': 0.7
                }
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
            else:
                return f"Error generating content: {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"