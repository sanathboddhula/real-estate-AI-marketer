import os
import requests
from urllib.parse import urlencode
from flask import session, url_for
import json

class OAuthService:
    def __init__(self):
        self.facebook_client_id = os.getenv('FACEBOOK_CLIENT_ID')
        self.facebook_client_secret = os.getenv('FACEBOOK_CLIENT_SECRET')
        self.linkedin_client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.linkedin_client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        
    def get_facebook_auth_url(self, redirect_uri):
        """Generate Facebook OAuth authorization URL"""
        params = {
            'client_id': self.facebook_client_id,
            'redirect_uri': redirect_uri,
            'scope': 'pages_manage_posts,pages_read_engagement,instagram_basic,instagram_content_publish',
            'response_type': 'code'
        }
        return f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}"
    
    def get_linkedin_auth_url(self, redirect_uri):
        """Generate LinkedIn OAuth authorization URL"""
        params = {
            'client_id': self.linkedin_client_id,
            'redirect_uri': redirect_uri,
            'scope': 'w_member_social',
            'response_type': 'code'
        }
        return f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
    
    def exchange_facebook_code(self, code, redirect_uri):
        """Exchange Facebook authorization code for access token"""
        try:
            response = requests.post('https://graph.facebook.com/v18.0/oauth/access_token', data={
                'client_id': self.facebook_client_id,
                'client_secret': self.facebook_client_secret,
                'redirect_uri': redirect_uri,
                'code': code
            })
            return response.json()
        except Exception as e:
            print(f"Facebook token exchange error: {e}")
            return None
    
    def exchange_linkedin_code(self, code, redirect_uri):
        """Exchange LinkedIn authorization code for access token"""
        try:
            response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': redirect_uri,
                'client_id': self.linkedin_client_id,
                'client_secret': self.linkedin_client_secret
            })
            return response.json()
        except Exception as e:
            print(f"LinkedIn token exchange error: {e}")
            return None
    
    def get_facebook_pages(self, access_token):
        """Get user's Facebook pages"""
        try:
            response = requests.get(f'https://graph.facebook.com/v18.0/me/accounts?access_token={access_token}')
            return response.json().get('data', [])
        except Exception as e:
            print(f"Facebook pages error: {e}")
            return []
    
    def post_to_facebook_page(self, page_id, page_access_token, message, image_path):
        """Post to Facebook page with image"""
        try:
            # Upload photo
            with open(image_path, 'rb') as image_file:
                response = requests.post(
                    f'https://graph.facebook.com/v18.0/{page_id}/photos',
                    data={'message': message},
                    files={'source': image_file},
                    params={'access_token': page_access_token}
                )
            return response.json()
        except Exception as e:
            print(f"Facebook post error: {e}")
            return {'error': str(e)}
    
    def post_to_linkedin(self, access_token, message, image_path):
        """Post to LinkedIn with image"""
        try:
            # Get user profile
            profile_response = requests.get(
                'https://api.linkedin.com/v2/people/~',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            person_urn = profile_response.json().get('id')
            
            # Upload image (simplified - real implementation needs multi-step upload)
            post_data = {
                'author': f'urn:li:person:{person_urn}',
                'lifecycleState': 'PUBLISHED',
                'specificContent': {
                    'com.linkedin.ugc.ShareContent': {
                        'shareCommentary': {'text': message},
                        'shareMediaCategory': 'IMAGE'
                    }
                },
                'visibility': {'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'}
            }
            
            response = requests.post(
                'https://api.linkedin.com/v2/ugcPosts',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                },
                json=post_data
            )
            return response.json()
        except Exception as e:
            print(f"LinkedIn post error: {e}")
            return {'error': str(e)}
    
    def save_tokens(self, platform, tokens):
        """Save OAuth tokens to session"""
        if 'oauth_tokens' not in session:
            session['oauth_tokens'] = {}
        session['oauth_tokens'][platform] = tokens
    
    def get_tokens(self, platform):
        """Get OAuth tokens from session"""
        return session.get('oauth_tokens', {}).get(platform)
    
    def is_connected(self, platform):
        """Check if platform is connected"""
        tokens = self.get_tokens(platform)
        return tokens and 'access_token' in tokens