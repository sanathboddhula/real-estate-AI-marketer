import os
import requests
import base64

class BufferService:
    def __init__(self):
        self.access_token = os.getenv('BUFFER_ACCESS_TOKEN')
        self.base_url = 'https://api.bufferapp.com/1'
        
    def get_profiles(self):
        """Get user's social media profiles"""
        try:
            response = requests.get(
                f'{self.base_url}/profiles.json',
                params={'access_token': self.access_token}
            )
            return response.json()
        except Exception as e:
            print(f"Buffer profiles error: {e}")
            return []
    
    def upload_media(self, image_path):
        """Upload image to Buffer"""
        try:
            with open(image_path, 'rb') as image_file:
                files = {'media': image_file}
                data = {'access_token': self.access_token}
                
                response = requests.post(
                    f'{self.base_url}/updates/create.json',
                    files=files,
                    data=data
                )
                return response.json()
        except Exception as e:
            print(f"Buffer upload error: {e}")
            return None
    
    def create_post(self, text, image_path, profile_ids=None):
        """Create a post with image"""
        try:
            # Get profiles if not specified
            if not profile_ids:
                profiles = self.get_profiles()
                profile_ids = [p['id'] for p in profiles if p.get('service') in ['facebook', 'linkedin', 'instagram']]
            
            # Convert image to base64 for Buffer API
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode()
            
            data = {
                'access_token': self.access_token,
                'text': text,
                'profile_ids[]': profile_ids,
                'media[photo]': f'data:image/png;base64,{image_data}',
                'now': True  # Post immediately
            }
            
            response = requests.post(
                f'{self.base_url}/updates/create.json',
                data=data
            )
            
            return response.json()
            
        except Exception as e:
            print(f"Buffer post error: {e}")
            return {'error': str(e)}
    
    def schedule_post(self, text, image_path, schedule_time, profile_ids=None):
        """Schedule a post for later"""
        try:
            if not profile_ids:
                profiles = self.get_profiles()
                profile_ids = [p['id'] for p in profiles if p.get('service') in ['facebook', 'linkedin', 'instagram']]
            
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode()
            
            data = {
                'access_token': self.access_token,
                'text': text,
                'profile_ids[]': profile_ids,
                'media[photo]': f'data:image/png;base64,{image_data}',
                'scheduled_at': schedule_time  # Unix timestamp
            }
            
            response = requests.post(
                f'{self.base_url}/updates/create.json',
                data=data
            )
            
            return response.json()
            
        except Exception as e:
            print(f"Buffer schedule error: {e}")
            return {'error': str(e)}
    
    def get_analytics(self, profile_id):
        """Get analytics for a profile"""
        try:
            response = requests.get(
                f'{self.base_url}/profiles/{profile_id}/updates.json',
                params={'access_token': self.access_token}
            )
            return response.json()
        except Exception as e:
            print(f"Buffer analytics error: {e}")
            return {}
    
    def is_connected(self):
        """Check if Buffer is properly configured"""
        return bool(self.access_token and self.get_profiles())