from PIL import Image, ImageDraw, ImageFont
import os

class FlyerGenerator:
    def __init__(self):
        self.social_formats = {
            "flyer": (800, 1000),
            "instagram": (1080, 1920),
            "facebook": (1200, 630),
            "linkedin": (1200, 627)
        }
        
        self.templates = {
            "modern": {
                "colors": {"primary": "#667eea", "accent": "#FFD700", "text": "white"},
                "banner_color": (102, 126, 234),
                "gradient": True
            },
            "luxury": {
                "colors": {"primary": "#2c3e50", "accent": "#f39c12", "text": "#ecf0f1"},
                "banner_color": (243, 156, 18),
                "gradient": False
            },
            "classic": {
                "colors": {"primary": "#34495e", "accent": "#e74c3c", "text": "white"},
                "banner_color": (231, 76, 60),
                "gradient": True
            }
        }
    
    def create_flyer(self, bg_image, address, price, bedrooms, bathrooms, template="modern", format_type="flyer", neighborhood_data=None, mortgage_data=None):
        flyer_width, flyer_height = self.social_formats.get(format_type, (800, 1000))
        template_config = self.templates.get(template, self.templates["modern"])
        bg_image = bg_image.resize((flyer_width, flyer_height))
        
        overlay = Image.new('RGBA', (flyer_width, flyer_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Template-based background
        text_bg_height = min(250, flyer_height // 4)
        if template_config["gradient"]:
            for i in range(text_bg_height):
                alpha = int(200 * (i / text_bg_height))
                draw.rectangle([(0, flyer_height - text_bg_height + i), (flyer_width, flyer_height - text_bg_height + i + 1)], 
                              fill=(0, 0, 0, alpha))
        else:
            draw.rectangle([(0, flyer_height - text_bg_height), (flyer_width, flyer_height)], 
                          fill=(44, 62, 80, 180))
        
        # Load fonts
        scale = min(flyer_width / 800, flyer_height / 1000)
        try:
            font_price = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", int(42 * scale))
            font_address = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", int(28 * scale))
            font_details = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", int(24 * scale))
            font_banner = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", int(20 * scale))
        except:
            font_price = font_address = font_details = font_banner = ImageFont.load_default()
        
        # Format price
        try:
            price_num = float(price.replace(',', '').replace('$', ''))
            if price_num >= 1000000:
                price_display = f"${price_num/1000000:.1f}M"
            elif price_num >= 1000:
                price_display = f"${price_num/1000:.0f}K"
            else:
                price_display = f"${price_num:,.0f}"
        except:
            price_display = f"${price}"
        
        # Add content
        margin = int(30 * scale)
        y_pos = flyer_height - int(220 * scale)
        
        draw.text((margin, y_pos), price_display, fill=template_config["colors"]["accent"], font=font_price)
        y_pos += int(55 * scale)
        
        draw.text((margin, y_pos), address, fill=template_config["colors"]["text"], font=font_address)
        y_pos += int(40 * scale)
        
        details = f"🛏️ {bedrooms} Bedrooms  •  🛁 {bathrooms} Bathrooms"
        draw.text((margin, y_pos), details, fill='#E0E0E0', font=font_details)
        
        # Add AI neighborhood story if available
        if neighborhood_data and neighborhood_data.get('story') and format_type in ['flyer', 'linkedin']:
            y_pos += int(35 * scale)
            
            story = neighborhood_data['story']
            story_text = story.get('headline', '')
            
            # Use smaller font for story
            try:
                font_story = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", int(20 * scale))
            except:
                font_story = font_details
            
            draw.text((margin, y_pos), story_text, fill='#FFD700', font=font_story)
        
        # Add insights if available and space permits
        elif neighborhood_data and mortgage_data and format_type in ['flyer', 'linkedin']:
            y_pos += int(35 * scale)
            
            # Key insights line
            insights = f"🚶 Walk Score: {neighborhood_data['walkability_score']} • 💰 ${mortgage_data['monthly_payment']:,}/mo • 🏫 {neighborhood_data['schools_nearby']} Schools"
            
            # Use smaller font for insights
            try:
                font_insights = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", int(18 * scale))
            except:
                font_insights = font_details
            
            draw.text((margin, y_pos), insights, fill='#C0C0C0', font=font_insights)
        
        # Banner
        banner_width, banner_height = int(180 * scale), int(50 * scale)
        banner_x = flyer_width - banner_width - int(20 * scale)
        draw.rectangle([(banner_x, int(30 * scale)), (banner_x + banner_width, int(30 * scale) + banner_height)], 
                      fill=template_config["banner_color"])
        
        bbox = draw.textbbox((0, 0), "FOR SALE", font=font_banner)
        text_width = bbox[2] - bbox[0]
        text_x = banner_x + (banner_width - text_width) // 2
        draw.text((text_x, int(42 * scale)), "FOR SALE", fill='white', font=font_banner)
        
        # Add top school for social formats
        if neighborhood_data and format_type in ['instagram', 'facebook']:
            school_text = f"📍 Near {neighborhood_data['top_school']}"
            draw.text((margin, flyer_height - int(70 * scale)), school_text, fill='#D0D0D0', font=font_details)
        
        draw.text((margin, flyer_height - int(40 * scale)), "Contact: Your Real Estate Agent", fill='#B0B0B0', font=font_details)
        
        final_image = Image.alpha_composite(bg_image.convert('RGBA'), overlay)
        
        os.makedirs('generated', exist_ok=True)
        output_path = f'generated/{format_type}_{template}.png'
        final_image.convert('RGB').save(output_path, quality=95)
        
        return output_path