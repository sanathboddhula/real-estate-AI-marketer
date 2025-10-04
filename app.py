from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from PIL import Image
import base64
from dotenv import load_dotenv
from services.image_service import ImageService
from services.flyer_generator import FlyerGenerator
from services.property_service import PropertyService
from services.maps_service import MapsService
from services.mortgage_service import MortgageService
from services.social_service import SocialService
from services.social_share_service import SocialShareService
from services.zillow_storytelling_service import ZillowStorytellingService
from services.ai_marketing_agent import AIMarketingAgent


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize services
image_service = ImageService(os.getenv('FREEPIK_API_KEY'))
flyer_generator = FlyerGenerator()
property_service = PropertyService()
maps_service = MapsService()
mortgage_service = MortgageService()
social_service = SocialService()
social_share_service = SocialShareService()
zillow_storytelling_service = ZillowStorytellingService()
ai_marketing_agent = AIMarketingAgent()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-flyer', methods=['POST'])
def generate_flyer():
    try:
        # Handle both form data (with file upload) and JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            address = request.form.get('address', 'Beautiful Property')
            price = request.form.get('price', '0')
            bedrooms = request.form.get('bedrooms', '0')
            bathrooms = request.form.get('bathrooms', '0')
            template = request.form.get('template', 'modern')
            format_type = request.form.get('format', 'flyer')
            
            # Check for uploaded image first, then Zillow image, then fallback
            uploaded_file = request.files.get('property_image')
            zillow_image_url = request.form.get('zillow_image_url')
            
            if uploaded_file:
                bg_image = Image.open(uploaded_file)
            elif zillow_image_url:
                try:
                    bg_image = image_service.get_image_from_url(zillow_image_url)
                except:
                    property_type = property_service.detect_property_type(price, bedrooms)
                    image_url = image_service.search_freepik_image(property_type) or image_service.get_fallback_image()
                    bg_image = image_service.get_image_from_url(image_url)
            else:
                # Detect property type and search Freepik
                property_type = property_service.detect_property_type(price, bedrooms)
                image_url = image_service.search_freepik_image(property_type) or image_service.get_fallback_image()
                bg_image = image_service.get_image_from_url(image_url)
        else:
            # Existing JSON handling
            data = request.json
            address = data.get('address', 'Beautiful Property')
            price = data.get('price', '0')
            bedrooms = data.get('bedrooms', '0')
            bathrooms = data.get('bathrooms', '0')
            template = data.get('template', 'modern')
            format_type = data.get('format', 'flyer')
            zillow_image_url = data.get('zillow_image_url')
            
            # Use Zillow image if available, otherwise fallback to Freepik/Unsplash
            if zillow_image_url:
                try:
                    bg_image = image_service.get_image_from_url(zillow_image_url)
                except:
                    property_type = property_service.detect_property_type(price, bedrooms)
                    image_url = image_service.search_freepik_image(property_type) or image_service.get_fallback_image()
                    bg_image = image_service.get_image_from_url(image_url)
            else:
                property_type = property_service.detect_property_type(price, bedrooms)
                image_url = image_service.search_freepik_image(property_type) or image_service.get_fallback_image()
                bg_image = image_service.get_image_from_url(image_url)
        
        # Get additional data
        neighborhood_data = maps_service.get_neighborhood_insights(address)
        mortgage_data = mortgage_service.calculate_mortgage(price)
        property_insights = zillow_storytelling_service.get_property_insights(address)
        
        # Generate AI neighborhood story
        neighborhood_story = zillow_storytelling_service.generate_neighborhood_story(address)
        neighborhood_data['story'] = neighborhood_story
        
        flyer_path = flyer_generator.create_flyer(bg_image, address, price, bedrooms, bathrooms, template, format_type, neighborhood_data, mortgage_data)
        
        with open(flyer_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}',
            'neighborhood': neighborhood_data,
            'mortgage': mortgage_data,
            'property_insights': property_insights,
            'flyer_path': flyer_path
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to generate flyer. Please try again.'}), 500



@app.route('/download-flyer/<path:filename>')
def download_flyer(filename):
    return send_from_directory('generated', filename, as_attachment=True)

@app.route('/get-social-captions', methods=['POST'])
def get_social_captions():
    try:
        data = request.json
        property_info = {
            'address': data.get('address', 'Beautiful Property'),
            'price': data.get('price', ''),
            'bedrooms': data.get('bedrooms', ''),
            'bathrooms': data.get('bathrooms', '')
        }
        
        captions = social_share_service.generate_social_captions(property_info)
        
        return jsonify({
            'success': True,
            'captions': captions
        })
        
    except Exception as e:
        print(f"Caption generation error: {e}")
        return jsonify({'error': 'Failed to generate captions'}), 500

@app.route('/email-flyer', methods=['POST'])
def email_flyer():
    try:
        data = request.json
        flyer_path = data.get('flyer_path')
        recipient_email = data.get('email')
        property_info = {
            'address': data.get('address', 'Beautiful Property'),
            'price': data.get('price', ''),
            'bedrooms': data.get('bedrooms', ''),
            'bathrooms': data.get('bathrooms', '')
        }
        
        if social_share_service.is_email_configured():
            result = social_share_service.send_flyer_email(recipient_email, flyer_path, property_info)
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'error': 'Email not configured. Add EMAIL_USER and EMAIL_PASSWORD to .env'
            })
        
    except Exception as e:
        print(f"Email error: {e}")
        return jsonify({'error': 'Failed to send email'}), 500

@app.route('/get-insights', methods=['POST'])
def get_insights():
    try:
        data = request.json
        address = data.get('address')
        price = data.get('price')
        
        neighborhood_data = maps_service.get_neighborhood_insights(address)
        mortgage_data = mortgage_service.calculate_mortgage(price)
        
        # Add AI neighborhood story
        neighborhood_story = zillow_storytelling_service.generate_neighborhood_story(address)
        neighborhood_data['story'] = neighborhood_story
        
        return jsonify({
            'success': True,
            'neighborhood': neighborhood_data,
            'mortgage': mortgage_data
        })
        
    except Exception as e:
        print(f"Insights error: {e}")
        return jsonify({'error': 'Failed to get insights'}), 500

@app.route('/get-neighborhood-story', methods=['POST'])
def get_neighborhood_story():
    try:
        data = request.json
        address = data.get('address')
        
        story = zillow_storytelling_service.generate_neighborhood_story(address)
        
        return jsonify({
            'success': True,
            'story': story
        })
        
    except Exception as e:
        print(f"Story generation error: {e}")
        return jsonify({'error': 'Failed to generate story'}), 500

@app.route('/ai-marketing-agent', methods=['POST'])
def ai_marketing_agent_endpoint():
    try:
        data = request.json
        address = data.get('address')
        
        # Get property data from Zillow
        property_data = zillow_storytelling_service.get_property_data(address)
        
        if not property_data:
            return jsonify({'error': 'Property not found'}), 404
        
        # Get comparables for CMA
        comparables = zillow_storytelling_service.get_comparable_properties(address)
        
        # Generate all AI marketing content
        descriptions = ai_marketing_agent.generate_property_descriptions(property_data)
        social_content = ai_marketing_agent.generate_social_media_content(property_data)
        cma_analysis = ai_marketing_agent.generate_cma_analysis(property_data, comparables)
        
        return jsonify({
            'success': True,
            'property_data': property_data,
            'descriptions': descriptions,
            'social_content': social_content,
            'cma_analysis': cma_analysis
        })
        
    except Exception as e:
        print(f"AI Marketing Agent error: {e}")
        return jsonify({'error': 'Failed to generate marketing content'}), 500

@app.route('/generate-descriptions', methods=['POST'])
def generate_descriptions():
    try:
        data = request.json
        address = data.get('address')
        
        # Get property data
        property_data = zillow_storytelling_service.get_property_data(address)
        
        if not property_data:
            return jsonify({'error': 'Property not found'}), 404
        
        descriptions = ai_marketing_agent.generate_property_descriptions(property_data)
        
        return jsonify({
            'success': True,
            'descriptions': descriptions
        })
        
    except Exception as e:
        print(f"Description generation error: {e}")
        return jsonify({'error': 'Failed to generate descriptions'}), 500

@app.route('/generate-social-content', methods=['POST'])
def generate_social_content():
    try:
        data = request.json
        address = data.get('address')
        
        # Get property data
        property_data = zillow_storytelling_service.get_property_data(address)
        
        if not property_data:
            return jsonify({'error': 'Property not found'}), 404
        
        social_content = ai_marketing_agent.generate_social_media_content(property_data)
        
        return jsonify({
            'success': True,
            'social_content': social_content
        })
        
    except Exception as e:
        print(f"Social content generation error: {e}")
        return jsonify({'error': 'Failed to generate social content'}), 500

@app.route('/generate-cma', methods=['POST'])
def generate_cma():
    try:
        data = request.json
        address = data.get('address')
        
        # Get property data and comparables
        property_data = zillow_storytelling_service.get_property_data(address)
        comparables = zillow_storytelling_service.get_comparable_properties(address)
        
        if not property_data:
            return jsonify({'error': 'Property not found'}), 404
        
        cma_analysis = ai_marketing_agent.generate_cma_analysis(property_data, comparables)
        
        return jsonify({
            'success': True,
            'cma_analysis': cma_analysis
        })
        
    except Exception as e:
        print(f"CMA generation error: {e}")
        return jsonify({'error': 'Failed to generate CMA'}), 500

@app.route('/api/parse-zillow', methods=['POST'])
def parse_zillow():
    try:
        data = request.json
        zillow_url = data.get('zillow_url')
        
        if not zillow_url:
            return jsonify({'error': 'Zillow URL is required'}), 400
        
        property_data = zillow_storytelling_service.parse_zillow_url(zillow_url)
        
        # Extract and validate main image URL
        main_image_url = property_data.get('main_image_url')
        if main_image_url:
            try:
                # Test if image is accessible
                test_image = image_service.get_image_from_url(main_image_url)
                property_data['image_available'] = True
            except:
                property_data['image_available'] = False
                property_data['main_image_url'] = None
        else:
            property_data['image_available'] = False
        
        return jsonify({
            'success': True,
            'property_data': property_data
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Zillow parsing error: {e}")
        return jsonify({'error': 'Failed to parse Zillow URL'}), 500

@app.route('/get-property-data', methods=['POST'])
def get_property_data():
    try:
        data = request.json
        address = data.get('address')
        
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        
        # Get property data from Zillow
        property_data = zillow_storytelling_service.get_property_data(address)
        
        if not property_data:
            return jsonify({'error': 'Property not found'}), 404
        
        return jsonify({
            'success': True,
            'property_data': property_data
        })
        
    except Exception as e:
        print(f"Property data error: {e}")
        return jsonify({'error': 'Failed to get property data'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)