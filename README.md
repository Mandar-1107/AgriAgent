# 🌾 AgriChat - Agriculture Chatbot

An intelligent agriculture chatbot built with Streamlit and Google Gemini AI, designed to help farmers and agricultural professionals with crop management, pest control, and weather-based recommendations.

## Features

✨ **Core Features:**
- 🤖 AI-powered agriculture expert (Google Gemini)
- 📸 Image analysis for crop identification and health assessment
- 🌤️ Real-time weather integration (OpenWeatherMap)
- 🗺️ Location-based recommendations
- 💬 Continuous conversation with context awareness
- 🌾 Agriculture-focused responses (100-200 words)

## Setup Instructions

### 1. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. API Keys (Already Configured)
The app uses:
- **Gemini API Key**
- **OpenWeatherMap API Key**

### 3. Run the App
\`\`\`bash
streamlit run app.py
\`\`\`

The app will open at `http://localhost:8501`

## How to Use

### Text Questions
1. Type your agriculture question in the input field
2. Optionally enter a location for weather context
3. Get AI-powered recommendations

### Image Analysis
1. Click "Upload image" to select a crop/field photo
2. The AI will identify the crop and assess its health
3. Receive specific recommendations
4. Ask follow-up questions

### Weather Integration
1. Enter a city name in the location field
2. Current weather data is automatically fetched
3. Recommendations are tailored to weather conditions

## Example Questions

- "How do I prevent powdery mildew on my wheat?"
- "What's the best time to plant tomatoes in my region?"
- "My rice field has yellow spots, what could it be?"
- "How much water does corn need in summer?"
- "What fertilizer should I use for my soil?"

## Image Upload Examples

- Crop/plant photos for identification
- Field photos for health assessment
- Pest/disease close-ups for diagnosis
- Soil samples for analysis

## Architecture

\`\`\`
app.py
├── Streamlit UI (Perplexity-like design)
├── Google Gemini API (Text & Vision)
├── OpenWeatherMap API (Weather data)
└── Session State (Conversation history)
\`\`\`

## API Integration Details

### Gemini API
- Model: `gemini-2.0-flash`
- Capabilities: Text generation, image analysis
- Used for: Q&A, image identification, recommendations

### OpenWeatherMap API
- Endpoint: `/data/2.5/weather`
- Data: Temperature, humidity, wind speed, conditions
- Used for: Weather-based agricultural advice

## Customization

### Change Response Length
Edit line in `get_agriculture_response()`:
\`\`\`python
# Change "100-200 words" to your preferred length
\`\`\`

### Add More Weather Data
Modify `format_weather_context()` to include:
- Rainfall predictions
- UV index
- Soil moisture

### Customize System Prompt
Edit the `system_prompt` in `get_agriculture_response()` to add:
- Regional expertise
- Specific crop focus
- Organic farming emphasis

## Troubleshooting

**Image not analyzing?**
- Ensure image is clear and well-lit
- Try JPG or PNG format
- Check file size (< 20MB)

**Weather not showing?**
- Verify location spelling
- Check internet connection
- Ensure API key is valid

**Slow responses?**
- Reduce image size
- Simplify questions
- Check API rate limits

## Future Enhancements

- 🌾 Crop calendar integration
- 📊 Historical weather data
- 🗺️ Interactive farm maps
- 📱 Mobile app version
- 🌐 Multi-language support
- 💾 Conversation export
- 📈 Yield prediction

## Support

For issues or questions, check:
1. API keys are correctly configured
2. Internet connection is stable
3. Image files are valid
4. Location names are correct

---

**Built with ❤️ for farmers and agricultural professionals**
