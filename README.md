# 🏠 AI Real Estate Flyer Generator

**4-Hour Hackathon Project** - Generate professional property marketing flyers instantly using AI and the Freepik API.

Link: https://real-estate-ai-marketer.onrender.com/

## 🎯 Project Goal
Create an AI agent that transforms basic listing data (address, price, bedrooms, bathrooms) into professional property marketing flyers in under 30 seconds.

## ✨ Features
- **Instant Flyer Generation**: Professional flyers in seconds
- **Freepik API Integration**: High-quality real estate images
- **Smart Fallback System**: Unsplash images if API fails
- **Modern UI**: Clean, responsive web interface
- **Demo Examples**: Quick-fill buttons for testing

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Open Browser**
   Navigate to `http://127.0.0.1:5000`

4. **Generate Flyers**
   - Fill in property details
   - Click "Generate Professional Flyer"
   - Download your flyer!

## 🛠 Technical Stack
- **Backend**: Python 3.12, Flask
- **Image Processing**: Pillow (PIL)
- **API**: Freepik API for property images
- **Frontend**: HTML5, CSS3, JavaScript
- **Fallback**: Unsplash for backup images

## 📁 Project Structure
```
real-estate-flyer-generator/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Web interface
├── generated/          # Output flyers (auto-created)
├── .env               # API keys
├── requirements.txt   # Dependencies
└── README.md         # This file
```

## 🎨 Demo Examples
The app includes three pre-filled examples:
- **Luxury Villa**: $2.85M Beverly Hills property
- **Modern Condo**: $895K Downtown LA unit  
- **Family Home**: $1.25M Pasadena house

## 🔧 Configuration
Add your Freepik API key to `.env`:
```
FREEPIK_API_KEY=your_api_key_here
```

## 🏆 Hackathon Success Metrics
- ✅ Generate flyers in under 30 seconds
- ✅ Professional design quality
- ✅ Error handling and fallbacks
- ✅ Demo-ready interface
- ✅ Multiple property examples

## 🚀 Future Enhancements
- Multiple flyer templates
- Custom branding options
- Bulk property processing
- PDF export functionality
- Social media optimization

---
*Built for hackathon success! 🏆*
