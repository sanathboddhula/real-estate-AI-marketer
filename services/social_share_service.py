import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class SocialShareService:
    def __init__(self):
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        
    def send_flyer_email(self, recipient_email, flyer_path, property_info):
        """Send flyer via email for manual social media posting"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = recipient_email
            msg['Subject'] = f"New Property Flyer: {property_info.get('address', 'Property')}"
            
            # Email body
            body = f"""
            Your property flyer is ready!
            
            Property: {property_info.get('address', 'N/A')}
            Price: ${property_info.get('price', 'N/A')}
            Bedrooms: {property_info.get('bedrooms', 'N/A')}
            Bathrooms: {property_info.get('bathrooms', 'N/A')}
            
            The flyer is attached. You can now post it to your social media platforms.
            
            Suggested caption:
            🏠 NEW LISTING: {property_info.get('address', 'Beautiful Property')}
            💰 Price: ${property_info.get('price', '')}
            #RealEstate #ForSale #PropertyListing
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach flyer image
            with open(flyer_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', filename='property_flyer.png')
                msg.attach(img)
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
            server.quit()
            
            return {'success': True, 'message': 'Flyer sent via email!'}
            
        except Exception as e:
            print(f"Email error: {e}")
            return {'error': str(e)}
    
    def generate_social_captions(self, property_info):
        """Generate platform-specific captions"""
        address = property_info.get('address', 'Beautiful Property')
        price = property_info.get('price', '')
        
        return {
            'facebook': f"🏠 NEW LISTING ALERT!\n\n📍 {address}\n💰 ${price}\n\nDM for details or schedule a showing!\n\n#RealEstate #NewListing #DreamHome #ForSale",
            'instagram': f"🏠✨ NEW LISTING ✨\n\n📍 {address}\n💰 ${price}\n\nSwipe for details! DM to schedule 📱\n\n#RealEstate #NewListing #PropertyForSale #DreamHome #Realtor",
            'linkedin': f"🏠 Professional Real Estate Opportunity\n\nProperty: {address}\nListing Price: ${price}\n\nExcellent investment opportunity in a prime location. Contact me for detailed information and viewing arrangements.\n\n#RealEstate #Investment #PropertyListing"
        }
    
    def create_download_package(self, flyer_path, property_info):
        """Create a package with flyer and social media templates"""
        captions = self.generate_social_captions(property_info)
        
        return {
            'flyer_path': flyer_path,
            'captions': captions,
            'instructions': {
                'facebook': 'Post to your Facebook business page with the Facebook caption',
                'instagram': 'Upload to Instagram Stories or Feed with the Instagram caption',
                'linkedin': 'Share on your LinkedIn profile with the LinkedIn caption'
            }
        }
    
    def is_email_configured(self):
        """Check if email is configured"""
        return bool(self.email_user and self.email_password)