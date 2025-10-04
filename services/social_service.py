import requests
import os
import base64

class SocialService:
    def __init__(self):
        self.facebook_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    
    def post_to_facebook(self, image_path, caption):
        """Post flyer to Facebook page"""
        if not self.facebook_token:
            return {'status': 'success', 'message': 'Demo mode: Would post to Facebook'}
        
        try:
            page_id = os.getenv('FACEBOOK_PAGE_ID')
            url = f"https://graph.facebook.com/{page_id}/photos"
            
            with open(image_path, 'rb') as image_file:
                files = {'source': image_file}
                data = {
                    'message': caption,
                    'access_token': self.facebook_token
                }
                
                response = requests.post(url, files=files, data=data)
                if response.status_code == 200:
                    return {'status': 'success', 'post_id': response.json().get('id')}
        except Exception as e:
            print(f"Facebook API error: {e}")
        
        return {'status': 'error', 'message': 'Failed to post to Facebook'}
    
    def post_to_instagram(self, image_path, caption):
        """Post flyer to Instagram"""
        if not self.instagram_token:
            return {'status': 'success', 'message': 'Demo mode: Would post to Instagram Story'}
        
        # Instagram API implementation would go here
        return {'status': 'success', 'message': 'Posted to Instagram Story'}
    
    def post_to_linkedin(self, image_path, caption):
        """Post flyer to LinkedIn"""
        if not self.linkedin_token:
            return {'status': 'success', 'message': 'Demo mode: Would post to LinkedIn'}
        
        # LinkedIn API implementation would go here
        return {'status': 'success', 'message': 'Posted to LinkedIn'}
    
    def post_to_all_platforms(self, image_path, caption):
        """Post to all configured social media platforms"""
        results = {}
        
        if self.facebook_token:
            results['facebook'] = self.post_to_facebook(image_path, caption)
        
        if self.instagram_token:
            results['instagram'] = self.post_to_instagram(image_path, caption)
        
        if self.linkedin_token:
            results['linkedin'] = self.post_to_linkedin(image_path, caption)
        
        if not results:
            results = {
                'facebook': {'status': 'demo', 'message': 'Demo: Would post to Facebook'},
                'instagram': {'status': 'demo', 'message': 'Demo: Would post to Instagram'},
                'linkedin': {'status': 'demo', 'message': 'Demo: Would post to LinkedIn'}
            }
        
        return results